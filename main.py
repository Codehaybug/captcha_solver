from fastapi import FastAPI, Query
from playwright.sync_api import sync_playwright
import time

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API giải CAPTCHA slider với Playwright"}

@app.get("/solve")
def solve_captcha(target_url: str = Query(..., description="URL chứa CAPTCHA iframe")):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(target_url, timeout=60000)

        time.sleep(2)

        # Tìm iframe chứa CAPTCHA
        frames = page.frames
        captcha_frame = None
        for f in frames:
            if "captcha.uvfuns.com" in f.url:
                captcha_frame = f
                break

        if not captcha_frame:
            browser.close()
            return {"error": "Không tìm thấy iframe CAPTCHA"}

        # Tìm slider bên trong iframe
        slider = captcha_frame.query_selector('div[class*="slider"], div[class*="slider-btn"], div[class*="nc_iconfont"]')

        if not slider:
            browser.close()
            return {"error": "Không tìm thấy slider"}

        box = slider.bounding_box()
        if not box:
            browser.close()
            return {"error": "Không lấy được vị trí slider"}

        # Kéo slider (move by offset)
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.mouse.down()

        # Kéo từng bước
        for move in [10, 15, 20, 10, 5]:
            page.mouse.move(page.mouse.position[0] + move, page.mouse.position[1])
            time.sleep(0.1)

        page.mouse.up()

        time.sleep(2)
        browser.close()
        return {"status": "solved"}
