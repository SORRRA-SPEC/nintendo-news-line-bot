#get_nintendo_news/py
import xml.etree.ElementTree as ET
import requests


def fetch_nintendo_news():
    # Google Newsが配信している「任天堂」に関する最新ニュースのRSS（プログラム用データ）
    url = "https://news.google.com/rss/search?q=%E4%BB%BB%E5%A4%A9%E5%A0%82&hl=ja&gl=JP&ceid=JP:ja"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 届いたXML（RSSデータ）を解析する
        root = ET.fromstring(response.content)

        news_items = []

        # RSSの中にある <item>（記事データ）を上から5件探す
        for item in root.findall(".//item")[:5]:
            title_elem = item.find("title")
            link_elem = item.find("link")

            title = (
                title_elem.text
                if title_elem is not None and title_elem.text
                else "タイトルなし"
            )
            link = (
                link_elem.text
                if link_elem is not None and link_elem.text
                else ""
            )

            news_items.append({"title": title, "url": link})

        return news_items

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return []


if __name__ == "__main__":
    print("任天堂の最新ニュースを取得中...\n")
    articles = fetch_nintendo_news()

    if articles:
        for i, item in enumerate(articles, 1):
            print(f"[{i}] {item['title']}")
            print(f"    URL: {item['url']}\n")
    else:
        print("ニュースが取得できませんでした。")