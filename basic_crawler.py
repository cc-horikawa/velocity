from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

url = "https://coinmarketcap.com/currencies/brilliantcrypto/historical-data/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=60000)

    # tbodyが表示されるまで待つ
    page.wait_for_selector("tbody", timeout=20000)
    print("tbodyが正常に表示されました。データの取得を開始します。")

    # 「Loading data...」ではなく、実際のデータが描画されるのを待機
    for _ in range(20):  # 最大20回（約10秒）試行
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        tbody = soup.find("tbody")
        rows = tbody.find_all("tr") if tbody else []
        if rows and all(len(row.find_all("td")) == 6 for row in rows):
            break
        time.sleep(0.5)
    else:
        print("データ読み込みがタイムアウトしました。")
        browser.close()
        exit()

    # 正常に取得できたデータを表示
    data = []
    for row in rows:
        cols = [td.text.strip() for td in row.find_all("td")]
        data.append(cols)

    for row in data:
        print(row)

    browser.close()
