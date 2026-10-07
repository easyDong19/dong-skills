#!/usr/bin/env python3
"""report.json → index.html (+ A4 PDF). 문체·구조 검사(lint)를 먼저 돌리고, 통과해야 빌드한다.

사용:
  python3 .claude/skills/qa-report/build.py <report.json> [--out DIR] [--pdf] [--lint-only]

- 캡처 경로는 report.json이 있는 폴더 기준 상대경로. base64로 임베드해 index.html 한 파일로 만든다.
- lint 오류가 하나라도 있으면 빌드하지 않는다(경고만 있으면 빌드한다).
- 표준 라이브러리만 쓴다.
"""
import argparse, base64, json, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE / "template.html"
STATUSES = {"pass", "fail", "blocked"}
ID_RE = re.compile(r"^[a-z][a-z0-9]*(\.[A-Za-z0-9-]+)+$")

# ── 문체 검사 ─────────────────────────────────────────────────────────
# 서술체 종결: 사람용 칸은 명사형으로 끝나야 한다. "~다 / ~요 / ~니다 / ~함." 등을 잡는다.
PROSE_END = re.compile(r"(다|니다|습니다|입니다|어요|아요|해요|예요|네요|죠)\s*[.。]?\s*$")
# 코드 식별자: 파일 경로·확장자·훅 이름·CSS 토큰·연산자·백틱. 사람용 칸에 들어오면 안 된다.
CODE_LIKE = [
    (re.compile(r"\b(apps|packages|src|docs)/"), "파일 경로"),
    (re.compile(r"\.(tsx?|jsx?|py|json|ya?ml|md)\b"), "파일 확장자"),
    (re.compile(r"\buse[A-Z]\w+"), "훅 이름"),
    (re.compile(r"\b(bg|text|border|gap|p|m|px|py)-[a-z0-9-]+"), "CSS 토큰"),
    (re.compile(r"===|!==|=>|\(\)|\bnull\b|\bundefined\b"), "코드 연산자"),
    (re.compile(r"`"), "백틱"),
    (re.compile(r"\b[a-z]+[A-Z][A-Za-z]+\b(?<!iPhone)"), "camelCase 식별자"),
]
LIMITS = {"title": 40, "pre": 40, "step": 30, "expect": 90, "actual": 90, "how": 50, "why": 40}
VAGUE = re.compile(r"(정상적으로|잘 |적절히|제대로|확인 필요|확인해야|추정|아마|것 같)")


def lint(rep, base):
    errors, warns = [], []
    E = lambda w, m: errors.append(f"{w}: {m}")
    W = lambda w, m: warns.append(f"{w}: {m}")

    def text(where, field, s, limit_key=None):
        if not isinstance(s, str) or not s.strip():
            E(where, f"{field} 비어 있음"); return
        if PROSE_END.search(s):
            E(where, f"{field} 서술체 종결 → 명사형으로: \"{s}\"")
        for rx, name in CODE_LIKE:
            if rx.search(s):
                E(where, f"{field}에 {name} 포함 → 사람이 보는 말로 바꾸거나 appendix로: \"{s}\"")
                break
        if VAGUE.search(s):
            E(where, f"{field}에 판단이 섞인 표현({VAGUE.search(s).group(0).strip()}) → 관찰한 사실만: \"{s}\"")
        lk = limit_key or field
        if lk in LIMITS and len(s) > LIMITS[lk]:
            W(where, f"{field} {len(s)}자 > {LIMITS[lk]}자 → 나누거나 줄이기")

    for k in ["id", "title", "product", "kind", "target", "run", "covers", "notCovers", "features", "unverified", "criteria", "appendix"]:
        if k not in rep:
            E("root", f"필수 필드 없음: {k}")
    if errors:
        return errors, warns
    for k in ["pr", "branch", "commit"]:
        if not rep["target"].get(k): E("target", f"{k} 없음")
    for k in ["at", "by", "env", "mode"]:
        if not rep["run"].get(k): E("run", f"{k} 없음")
    for k in ["covers", "notCovers"]:
        for i, s in enumerate(rep[k]): text(f"{k}[{i}]", "항목", s)
    if rep.get("note"): text("note", "note", rep["note"])

    ids, nos = set(), set()
    for fi, f in enumerate(rep["features"]):
        if not f.get("name"): E(f"features[{fi}]", "name 없음")
        if f.get("note"): text(f"features[{fi}]", "note", f["note"])
        if not f.get("cases"): E(f"features[{fi}]", "cases 비어 있음")
        for c in f.get("cases", []):
            w = f"case {c.get('no', '?')} ({c.get('id', '?')})"
            cid = c.get("id", "")
            if not ID_RE.match(cid): E(w, f"id는 '기능.시나리오' 꼴 고정 키여야 함 (예 notice.caseA): \"{cid}\"")
            if cid in ids: E(w, "id 중복")
            ids.add(cid)
            if c.get("no") in nos: E(w, "no 중복")
            nos.add(c.get("no"))
            if c.get("status") not in STATUSES: E(w, f"status는 pass|fail|blocked 중 하나: \"{c.get('status')}\"")
            text(w, "title", c.get("title"))
            text(w, "pre", c.get("pre"))
            steps = c.get("steps") or []
            if not steps: E(w, "steps 비어 있음")
            for i, s in enumerate(steps): text(w, f"steps[{i}]", s, "step")
            text(w, "expect", c.get("expect"))
            text(w, "actual", c.get("actual"))
            st = c.get("status")
            if st == "pass" and c.get("actual") != "기대와 동일":
                W(w, "pass인데 actual이 '기대와 동일'이 아님 → 통과면 그 문구로 고정")
            if st == "fail" and c.get("actual") == "기대와 동일":
                E(w, "fail인데 actual이 '기대와 동일'")
            if st == "fail" and not c.get("issue"):
                W(w, "fail에 issue 없음 → '이슈 미등록'이라도 적기")
            if st in ("pass", "fail") and not c.get("evidence"):
                E(w, f"{st}인데 evidence 없음 → 캡처 없이는 pass/fail을 줄 수 없다. 못 찍었으면 blocked")
            ev = c.get("evidence")
            if ev:
                p = base / ev.get("src", "")
                if not p.is_file(): E(w, f"캡처 파일 없음: {ev.get('src')}")
                if not ev.get("alt"): W(w, "evidence.alt 없음(캡션)")
            for k in ("checks", "notes"):
                if isinstance(c.get(k), list):
                    for i, s in enumerate(c[k]): text(w, f"{k}[{i}]", s, "how")
            if "notes" in c: W(w, "notes 필드는 템플릿이 그리지 않음 → checks 또는 appendix로")
    for u in rep["unverified"]:
        w = f"unverified {u.get('id', '?')}"
        for k in ("id", "title", "why", "how"):
            if not u.get(k): E(w, f"{k} 없음")
        text(w, "title", u.get("title", "")); text(w, "why", u.get("why", "")); text(w, "how", u.get("how", ""))
    for i, cr in enumerate(rep["criteria"]):
        if "text" not in cr or "auto" not in cr: E(f"criteria[{i}]", "text/auto 필요")
    return errors, warns


MIME = {".png": "image/png", ".gif": "image/gif", ".webp": "image/webp", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def build(rep, base, out, pdf):
    tpl = TEMPLATE.read_text(encoding="utf-8")
    rep = json.loads(json.dumps(rep))  # copy
    for f in rep["features"]:
        for c in f["cases"]:
            ev = c.get("evidence")
            if ev:
                p = base / ev["src"]
                mime = MIME.get(p.suffix.lower(), "image/jpeg")
                ev["src"] = f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()
    js = json.dumps(rep, ensure_ascii=False).replace("</", "<\\/")
    html = tpl.replace("<!--TITLE-->", f"{rep['title']} QA 리포트").replace("<!--REPORT_JSON-->", js)
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
    print(f"index.html  {len(html.encode()) // 1024} KB  → {out / 'index.html'}")
    if pdf:
        chrome = next((c for c in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", shutil.which("google-chrome"), shutil.which("chromium")] if c and pathlib.Path(c).exists()), None)
        if not chrome:
            print("PDF 건너뜀: Chrome 없음"); return
        target = out / "report-a4.pdf"
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={target}", f"file://{(out / 'index.html').resolve()}"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        print(f"report-a4.pdf  → {target}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--out", help="출력 폴더 (기본: report.json 폴더)")
    ap.add_argument("--pdf", action="store_true", help="A4 PDF도 만든다 (Chrome 필요)")
    ap.add_argument("--lint-only", action="store_true")
    a = ap.parse_args()
    src = pathlib.Path(a.report).resolve()
    rep = json.loads(src.read_text(encoding="utf-8"))
    base = src.parent
    errors, warns = lint(rep, base)
    for w in warns: print("WARN ", w)
    for e in errors: print("ERROR", e)
    n = sum(len(f["cases"]) for f in rep.get("features", [])) if not errors else 0
    if errors:
        print(f"\nlint 실패: 오류 {len(errors)} · 경고 {len(warns)}. 빌드하지 않음."); sys.exit(1)
    cnt = {s: 0 for s in STATUSES}
    for f in rep["features"]:
        for c in f["cases"]: cnt[c["status"]] += 1
    print(f"lint 통과: 케이스 {n} · 통과 {cnt['pass']} · 실패 {cnt['fail']} · 막힘 {cnt['blocked']} · 미검증 {len(rep['unverified'])} · 경고 {len(warns)}")
    if a.lint_only: return
    build(rep, base, pathlib.Path(a.out).resolve() if a.out else base, a.pdf)


if __name__ == "__main__":
    main()
