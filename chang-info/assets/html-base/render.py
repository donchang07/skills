# 사용: python3 render.py <폴더> [page-1 page-2 ...]
# .page 요소를 2배율 PNG로 저장. 세로형 .page 너비 1240px(A4 목표 비율 1.414), 가로형 1672px(16:9 목표 0.5625).
from playwright.sync_api import sync_playwright
import sys, os
d = os.path.abspath(sys.argv[1]); pages = sys.argv[2:] or ["page-1","page-2","page-3"]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1800,"height":1800}, device_scale_factor=2)
    for n in pages:
        pg.goto(f"file://{d}/{n}.html"); pg.wait_for_timeout(400)
        w, h = pg.evaluate("(()=>{const r=document.querySelector('.page').getBoundingClientRect();return [r.width,r.height]})()")
        pg.locator(".page").screenshot(path=f"{d}/{n}.png")
        print(f"{n}: {round(w)}x{round(h)} 비율 {h/w:.3f}")
    b.close()
