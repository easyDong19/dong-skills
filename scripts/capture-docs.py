"""docs 예시 이미지를 다시 만든다.

    python scripts/capture-docs.py qa      # qa-report 예시 캡처(가상 알림함) + 리포트 스크린샷·GIF
    python scripts/capture-docs.py study   # a4-study-sheet · study-explainer 스크린샷 (--a4, --explainer, --a4-fig 로 원본 지정)

필요: playwright(chromium), Pillow, Chrome(리포트 PDF), pdftoppm(PDF → PNG)
"""
import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
QA = ROOT / "skills/qa-report"
MOCK = ROOT / "scripts/fixtures/inbox-mock.html"
IMG = ROOT / "docs/images"


def save_png(img: Image.Image, path: pathlib.Path, width: int | None = None):
    if width and img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(path, optimize=True)
    print(f"  {path.relative_to(ROOT)}  {path.stat().st_size // 1024} KB")


def save_gif(frames, path: pathlib.Path, width: int | None = None):
    """frames: [(PIL.Image, 표시 시간 ms)]"""
    imgs, durs = [], []
    for im, ms in frames:
        if width and im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        imgs.append(im.convert("RGB").quantize(colors=128, method=Image.Quantize.MEDIANCUT))
        durs.append(max(20, int(ms)))
    path.parent.mkdir(parents=True, exist_ok=True)
    imgs[0].save(path, save_all=True, append_images=imgs[1:], duration=durs, loop=0, optimize=True, disposal=1)
    print(f"  {path.relative_to(ROOT)}  {len(imgs)}프레임  {path.stat().st_size // 1024} KB")


def shot(page, **kw) -> Image.Image:
    import io
    return Image.open(io.BytesIO(page.screenshot(**kw)))


def record(page, seconds: float, **kw):
    """seconds 동안 가능한 만큼 스크린샷을 찍고, 실제 간격을 프레임 시간으로 쓴다."""
    out, t0 = [], time.monotonic()
    last = t0
    while time.monotonic() - t0 < seconds:
        im = shot(page, **kw)
        now = time.monotonic()
        if out:
            out[-1] = (out[-1][0], (now - last) * 1000)
        out.append((im, 60))
        last = now
    return out


# ---------------------------------------------------------------- qa-report

def qa(p):
    print("qa-report 예시 캡처 (가상 알림함)")
    caps = QA / "example/captures"
    for old in caps.glob("*"):
        old.unlink()
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    for name, state in [("01-inbox-list", "list"), ("02-inbox-empty", "empty"), ("03-inbox-unread", "unread")]:
        page.goto(f"{MOCK.as_uri()}?state={state}")
        save_png(shot(page), caps / f"{name}.png")

    page.goto(f"{MOCK.as_uri()}?state=list")
    first = shot(page)
    page.evaluate("window.playSwipe(); 0")
    frames = [(first, 700)] + record(page, 1.5)
    frames[-1] = (frames[-1][0], 1600)
    save_gif(frames, caps / "04-inbox-swipe.gif")
    b.close()

    print("리포트 빌드")
    tmp = pathlib.Path(tempfile.mkdtemp())
    subprocess.run([sys.executable, str(QA / "build.py"), str(QA / "example/report.json"), "--out", str(tmp), "--pdf"], check=True)

    print("리포트 스크린샷")
    out = IMG / "qa-report"
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1100, "height": 760}, device_scale_factor=1)
    page.goto((tmp / "index.html").as_uri())
    page.wait_for_timeout(400)
    save_png(shot(page), out / "report-top.png")
    page.locator('.case[data-id="inbox.unread"]').screenshot(path=str(tmp / "c.png"))
    save_png(Image.open(tmp / "c.png"), out / "report-case-fail.png")

    # 동작 GIF: 캡처 확대 → GIF 캡처 재생 → 다음 → 닫기 → 전체 승인
    frames = [(shot(page), 1400)]
    page.locator('.case[data-id="inbox.unread"]').scroll_into_view_if_needed()
    page.evaluate("window.scrollBy(0, 200)")
    page.wait_for_timeout(150)
    frames.append((shot(page), 1300))
    page.locator('[data-zoom="inbox.unread"]').click()
    page.wait_for_timeout(200)
    frames.append((shot(page), 1300))
    page.locator("#lb-next").click()
    page.wait_for_timeout(100)
    frames += record(page, 2.8)
    page.locator("#lb-close").click()
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(150)
    frames.append((shot(page), 700))
    page.locator("#all-ok").click()
    page.wait_for_timeout(250)
    frames.append((shot(page), 2200))
    save_gif(frames, out / "report-demo.gif", width=880)

    page.reload()
    page.wait_for_timeout(300)
    page.locator('[data-zoom="inbox.unread"]').click()
    page.wait_for_timeout(300)
    save_png(shot(page), out / "report-lightbox.png")
    b.close()

    pdf = tmp / "report-a4.pdf"
    if pdf.exists() and shutil.which("pdftoppm"):
        subprocess.run(["pdftoppm", "-png", "-r", "80", "-f", "1", "-l", "2", str(pdf), str(tmp / "a4")], check=True)
        pages = [Image.open(f).convert("RGB") for f in sorted(tmp.glob("a4*.png"))]
        gap = 24
        sheet = Image.new("RGB", (sum(pg.width for pg in pages) + gap * (len(pages) + 1), pages[0].height + gap * 2), (232, 231, 226))
        x = gap
        for pg in pages:
            sheet.paste(pg, (x, gap)); x += pg.width + gap
        save_png(sheet, out / "report-a4.png")
    shutil.rmtree(tmp)


# ---------------------------------------------------------------- study

REDACT_JS = """words => {
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = w.nextNode());) for (const x of words) n.nodeValue = n.nodeValue.split(x).join("");
}"""


def a4_first_page(b, src: pathlib.Path, out: pathlib.Path, redact=()):
    page = b.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=1.5)
    page.goto(src.as_uri())
    if redact:
        page.evaluate(REDACT_JS, list(redact))
    page.emulate_media(media="print")
    page.wait_for_timeout(400)
    full = shot(page, full_page=True)
    save_png(full.crop((0, 0, full.width, min(full.height, round(1123 * 1.5)))), out, width=900)


def study(p, a4: pathlib.Path, explainer: pathlib.Path, a4_fig: pathlib.Path | None, redact):
    b = p.chromium.launch()
    print("a4-study-sheet")
    a4_first_page(b, a4, IMG / "a4-study-sheet/sheet.png", redact)
    if a4_fig:
        a4_first_page(b, a4_fig, IMG / "a4-study-sheet/sheet-figures.png", redact)

    print("study-explainer")
    page = b.new_page(viewport={"width": 1180, "height": 800}, device_scale_factor=1)
    page.goto(explainer.as_uri())
    page.wait_for_timeout(600)
    save_png(shot(page), IMG / "study-explainer/top.png")
    # 02 섹션 제목부터 03 섹션 제목 직전까지 — 코드 + 그림 + 함정 박스가 한 화면에 들어온다
    y0, y1 = page.evaluate("""() => {
      const hs = [...document.querySelectorAll('h2.sec')];
      const top = h => h.getBoundingClientRect().top + scrollY;
      return [top(hs[1]) - 24, top(hs[2]) - 40];
    }""")
    full = shot(page, full_page=True)
    save_png(full.crop((0, int(y0), full.width, int(y1))), IMG / "study-explainer/section.png")
    b.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", choices=["qa", "study"])
    ap.add_argument("--a4", type=pathlib.Path)
    ap.add_argument("--explainer", type=pathlib.Path)
    ap.add_argument("--a4-fig", type=pathlib.Path, help="그림(인라인 SVG)이 들어간 A4 요약 HTML")
    ap.add_argument("--redact", action="append", default=[], help="캡처 전에 화면에서 지울 문구 (회사명 등). 여러 번 줄 수 있다")
    a = ap.parse_args()
    with sync_playwright() as p:
        if a.target == "qa":
            qa(p)
        else:
            if not (a.a4 and a.explainer):
                ap.error("study 는 --a4 와 --explainer 가 필요하다")
            study(p, a.a4.resolve(), a.explainer.resolve(), a.a4_fig.resolve() if a.a4_fig else None, a.redact)


if __name__ == "__main__":
    main()
