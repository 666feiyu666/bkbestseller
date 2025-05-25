from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup
import pandas as pd
import time

def scroll_all_items(driver, max_scrolls=5):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    wait = WebDriverWait(driver, 10)
    action = ActionChains(driver)

    prev_count = 0
    for _ in range(max_scrolls):
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "zg-grid-general-faceout")))
        items = driver.find_elements(By.CLASS_NAME, "zg-grid-general-faceout")

        for item in items:
            try:
                action.move_to_element(item).perform()
                time.sleep(0.3)
            except:
                continue

        # 等待新元素加载
        time.sleep(1.5)
        new_items = driver.find_elements(By.CLASS_NAME, "zg-grid-general-faceout")

        # 如果数量不再增加就退出
        if len(new_items) <= prev_count:
            break
        prev_count = len(new_items)


def scrape_amazon_top100(year):
    base_url = f"https://www.amazon.com/gp/bestsellers/{year}/books"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    books = []

    for page in [1, 2]:
        url = base_url if page == 1 else f"{base_url}?pg=2"
        driver.get(url)
        time.sleep(2)
        scroll_all_items(driver) 
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.select("div.zg-grid-general-faceout")

        if not items:
            print(f"❗ {year} 第 {page} 页无数据，跳过")
            continue

        for item in items:
            if len(books) >= 100:
                break

            title_tag = item.select_one('div._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y')
            title = title_tag.text.strip() if title_tag else "N/A"

            author_tag = item.select_one("div.a-row.a-size-small")
            author = author_tag.text.strip() if author_tag else "N/A"

            price_tag = item.select_one("span._cDEzb_p13n-sc-price_3mJ9Z") or item.select_one("span.p13n-sc-price")
            price = price_tag.text.strip() if price_tag else "N/A"

            rating_tag = item.select_one("span.a-icon-alt")
            rating = rating_tag.text.strip().split(" ")[0] if rating_tag else "N/A"

            format_tag = item.select_one("span.a-size-small.a-color-secondary.a-text-normal")
            book_format = format_tag.text.strip() if format_tag else "N/A"

            books.append({
                "year": year,
                "rank": len(books) + 1,
                "title": title,
                "author": author,
                "price": price,
                "rating": rating,
                "format": book_format
            })

        print(f"✅ {year} - Page {page} 抓取完毕，目前共 {len(books)} 本")

    driver.quit()
    return books

# 批量爬取 1995–2024 年图书
all_books = []
for y in range(1995, 2025):
    try:
        books = scrape_amazon_top100(y)
        print(f"✅ {y} 年完成，共 {len(books)} 本")
        all_books.extend(books)
    except Exception as e:
        print(f"❌ {y} 年失败：{e}")

# 保存结果
df = pd.DataFrame(all_books)
df.to_csv("data/amazon_books_1995_2024_top100.csv", index=False)
print("✅ 全部完成，已保存：amazon_books_1995_2024_top100.csv")