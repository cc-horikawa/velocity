from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import csv

url = "https://coinmarketcap.com/currencies/brilliantcrypto/historical-data/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=60000)

    # tbodyが表示されるまで待つ
    page.wait_for_selector("tbody", timeout=20000)
    print("tbodyが正常に表示されました。データの取得を開始します。")

    # 実データ（6列のtd）描画を待機
    for _ in range(20):
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

    # データを抽出
    data = []
    for row in rows:
        cols = [td.text.strip() for td in row.find_all("td")]
        data.append(cols)

    # CSVに保存
    with open("result.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        #CoinMarketCapのHistoryから
        writer.writerow(["Date", "Open", "High", "Low", "Close", "Volume"])
        writer.writerows(data)

    print(f"{len(data)} 行を result.csv に保存しました。")

    browser.close()
