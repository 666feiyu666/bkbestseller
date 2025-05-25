from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_amazon_top10(year):
    url = f"https://www.amazon.com/gp/bestsellers/{year}/books/ref=zg_bsar_cal_ye"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    books = []
    items = soup.select("div.zg-grid-general-faceout")
    for i, item in enumerate(items[:10]):
        # 书名
        title_tag = item.select_one('div._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y')
        title = title_tag.text.strip() if title_tag else "N/A"

        # 作者
        author_tag = item.select_one("div.a-row.a-size-small")
        author = author_tag.text.strip() if author_tag else "N/A"

        # 价格
        price_tag = item.select_one("span._cDEzb_p13n-sc-price_3mJ9Z") or item.select_one("span.p13n-sc-price")
        price = price_tag.text.strip() if price_tag else "N/A"

        # 评分
        rating_tag = item.select_one("span.a-icon-alt")
        rating = rating_tag.text.strip().split(" ")[0] if rating_tag else "N/A"

        # 装帧类型（Paperback / Hardcover）
        format_tag = item.select_one("span.a-size-small.a-color-secondary.a-text-normal")
        book_format = format_tag.text.strip() if format_tag else "N/A"

        books.append({
            "year": year,
            "rank": i + 1,
            "title": title,
            "author": author,
            "price": price,
            "rating": rating,
            "format": book_format
        })

    return books

# 批量爬取 1995–2024 年图书
all_books = []
for y in range(1995, 2025):
    try:
        books = scrape_amazon_top10(y)
        print(f"✅ {y} 年完成，共 {len(books)} 本")
        all_books.extend(books)
    except Exception as e:
        print(f"❌ {y} 年失败：{e}")

# 保存结果
df = pd.DataFrame(all_books)
df.to_csv("data/amazon_books_1995_2024_top10.csv", index=False)
print("✅ 全部完成，已保存：amazon_books_1995_2024_top10.csv")