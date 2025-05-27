import time
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 调试版本(需要有亚马逊账号并登陆，且已保存cookies到amazon_cookies.json文件中)
# 也可以用来单独爬取某一年数据（建议先跑一年看是否成功再用循环）
def load_cookies(driver, path="amazon_cookies.json"):
    driver.get("https://www.amazon.com")
    with open(path, "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            if 'sameSite' in cookie:
                del cookie['sameSite']
            driver.add_cookie(cookie)

def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def scrape_book_description(url):
    driver = create_driver()
    try:
        load_cookies(driver)
        driver.get(url)
        time.sleep(3)

        try:
            read_more = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".a-expander-partial-collapse-header a"))
            )
            driver.execute_script("arguments[0].click();", read_more)
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".a-expander-content.a-expander-content-expanded"))
            )
            time.sleep(1.5)
        except:
            pass

        soup = BeautifulSoup(driver.page_source, "html.parser")
        for selector in [
            "#bookDescription_feature_div .a-expander-content",
            ".a-expander-content.a-expander-partial-collapse-content",
            "#productDescription p"
        ]:
            container = soup.select_one(selector)
            if container:
                return container.get_text(separator=" ", strip=True)

        return "N/A"
    except Exception as e:
        return f"ERROR: {e}"
    finally:
        driver.quit()

def scrape_top10_books_with_description(year):
    base_url = f"https://www.amazon.com/gp/bestsellers/{year}/books"
    driver = create_driver()
    load_cookies(driver)
    driver.get(base_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    books = []
    items = soup.select("div.zg-grid-general-faceout")
    for i, item in enumerate(items[:10]):
        title_tag = item.select_one('div._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y')
        title = title_tag.text.strip() if title_tag else "N/A"
        link_tag = item.select_one("a.a-link-normal")
        url = "https://www.amazon.com" + link_tag['href'] if link_tag else "N/A"

        print(f"📘 {i+1}. {title[:40]} - 获取描述中...")
        desc = scrape_book_description(url) if url != "N/A" else "N/A"
        print(f"✅ 完成（{len(desc)} 字）")

        books.append({
            "year": year,
            "rank": i + 1,
            "title": title,
            "url": url,
            "description": desc
        })

    return books

# 用于测试
# === 执行某一年 ===
year = 2013
books = scrape_top10_books_with_description(year)
df = pd.DataFrame(books)
df.to_csv(f"data/top10desc/{year}.csv", index=False)
print(f"✅ 已保存：top10desc/{year}.csv")

# # === 循环跑所有年份 ===
# for year in range(2009, 2015):
#     try:
#         df = pd.DataFrame(scrape_top10_books_with_description(year))
#         df.to_csv(f"data/top10desc/{year}.csv", index=False)
#         print(f"✅ {year} 年完成")
#     except Exception as e:
#         print(f"❌ {year} 年失败：{e}")