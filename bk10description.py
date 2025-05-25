from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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

    desc_tag = soup.select_one("#bookDescription_feature_div span") or \
               soup.select_one("div#productDescription") or \
               soup.select_one("div.a-expander-content span")

    if desc_tag:
        return desc_tag.get_text(strip=True)
    return "N/A"

def crawl_top10_descriptions(year=2024, output_csv=True):
    books = scrape_amazon_top10_with_links(year)
    for book in books:
        if book["url"] != "N/A":
            try:
                desc = scrape_book_description(book["url"])
                book["description"] = desc
                print(f"✅ {book['title'][:30]} - 描述抓取成功")
            except Exception as e:
                book["description"] = "N/A"
                print(f"❌ {book['title'][:30]} - 描述抓取失败: {e}")

    if output_csv:
        pd.DataFrame(books).to_csv(f"amazon_books_{year}_top10_desc_only.csv", index=False)
        print(f"✅ 已保存：amazon_books_{year}_top10_desc_only.csv")

    return books

if __name__ == "__main__":
    crawl_top10_descriptions(2024)
