from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time

def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

driver = create_driver()
driver.get("https://www.amazon.com/")

input("🧠 请在弹出窗口中点击右上角“Sign in”并完成登录后，按回车继续保存 cookie...")

with open("amazon_cookies.json", "w") as f:
    json.dump(driver.get_cookies(), f)

print("✅ Cookie 已保存至 amazon_cookies.json")
driver.quit()
