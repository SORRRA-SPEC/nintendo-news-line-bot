#main.py
import json
import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv  # 追加
import requests

# 1. .env ファイルから環境変数を読み込む
load_dotenv()

# os.environ.get で環境変数から安全にトークンを取得
LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")

# 歴史記録ファイルの設定など（以降のコードはそのまま）
HISTORY_FILE = "sent_articles.txt"

def fetch_nintendo_news():
    """任天堂の最新ニュース（RSS）を取得する"""
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

        root = ET.fromstring(response.content)
        news_items = []

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
        print(f"ニュース取得エラー: {e}")
        return []


def load_sent_urls():
    """送信済みのURL一覧をファイルから読み込む"""
    if not os.path.exists(HISTORY_FILE):
        return set()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def save_sent_url(url):
    """送信したURLをファイルに追記保存する"""
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{url}\n")


def send_line_message(message_text):
    """LINE Messaging APIを使ってブロードキャスト送信する"""
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
    }
    payload = {"messages": [{"type": "text", "text": message_text}]}

    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(payload), timeout=10
        )
        response.raise_for_status()
        print("LINEへの送信に成功しました！")
    except requests.exceptions.RequestException as e:
        print(f"LINE送信エラー: {e}")


def main():
    print("--- 任天堂ニュースBot 起動 ---")

    # 1. 送信済みURLの履歴を読み込む
    sent_urls = load_sent_urls()

    # 2. 最新ニュースを取得
    articles = fetch_nintendo_news()

    if not articles:
        print("ニュースが見つかりませんでした。")
        return

    # 3. 未送信のニュースだけを抽出
    new_articles = [a for a in articles if a["url"] not in sent_urls]

    if not new_articles:
        print("新しいニュースはありません（すべて送信済み）。")
        return

    print(f"{len(new_articles)}件の新しいニュースが見つかりました！")

    # 4. LINE用にメッセージ文章を組み立てる
    message_text = "🎮【最新】任天堂ニュースをお届けします！\n"
    for item in new_articles:
        message_text += f"\n■ {item['title']}\n{item['url']}\n"

    # 5. LINEへ送信
    send_line_message(message_text)

    # 6. 送信したニュースのURLを履歴ファイルに保存
    for item in new_articles:
        save_sent_url(item["url"])


if __name__ == "__main__":
    main()