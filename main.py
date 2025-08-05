from fastapi import FastAPI, Query
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API giải CAPTCHA slider iframe"}

@app.get("/solve")
def solve_captcha(target_url: str = Query(..., description="URL chứa CAPTCHA iframe")):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(target_url)
        time.sleep(2)

        # Tìm iframe CAPTCHA
        iframe = driver.find_element(By.XPATH, '//iframe[contains(@src, "captcha.uvfuns.com")]')
        driver.switch_to.frame(iframe)

        time.sleep(2)

        # Tìm slider button
        slider = driver.find_element(By.XPATH, '//div[contains(@class, "slider") or contains(@class, "slider-btn") or contains(@class, "nc_iconfont")]')

        # Kéo slider giả lập
        actions = ActionChains(driver)
        actions.click_and_hold(slider).perform()

        for move in [10, 15, 20, 10, 5]:
            actions.move_by_offset(move, 0).perform()
            time.sleep(0.1)

        actions.release().perform()

        time.sleep(2)
        return {"status": "solved"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()
