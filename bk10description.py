from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_amazon_top10_with_links(year):
    url = f"https://www.amazon.com/gp/bestsellers/{year}/books"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    books = []
    items = soup.select("div.zg-grid-general-faceout")
    for i, item in enumerate(items[:10]):
        title_tag = item.select_one('div._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y')
        title = title_tag.text.strip() if title_tag else "N/A"

        link_tag = item.select_one("a.a-link-normal")
        book_url = "https://www.amazon.com" + link_tag['href'] if link_tag else "N/A"

        books.append({
            "year": year,
            "title": title,
            "url": book_url
        })

    return books

def scrape_book_description(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # 寻找描述容器
    desc_container = soup.select_one("#bookDescription_feature_div .a-expander-content")
    if desc_container:
        # 提取所有文本（包括嵌套的 span、p 等）
        return desc_container.get_text(separator=" ", strip=True)

    return "N/A"

# 批量爬取 1995–2024 年前十图书及其描述
all_books = []
for year in range(1995, 2025):
    try:
        books = scrape_amazon_top10_with_links(year)
        for book in books:
            if book["url"] != "N/A":
                try:
                    book["description"] = scrape_book_description(book["url"])
                except Exception as e:
                    book["description"] = "N/A"
        all_books.extend(books)
        print(f"✅ {year} 年完成，共 {len(books)} 本")
    except Exception as e:
        print(f"❌ {year} 年失败：{e}")

# 保存结果
df = pd.DataFrame(all_books)
df.to_csv("data/amazon_books_1995_2024_top10_desc_only.csv", index=False)
print("✅ 全部完成，已保存：amazon_books_1995_2024_top10_desc_only.csv")
