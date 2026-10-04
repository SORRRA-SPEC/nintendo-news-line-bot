# send_line_test.py
import json
import requests

# 1. 先ほど取得したLINEのチャネルアクセストークンを設定
LINE_ACCESS_TOKEN = "DvdXbecSCwb7f8U3cusQMQb3g15lVL6GV46VYyS6Eu490XRlkEMcmNWjGo49m0QILyb84GKo0n+i31umaR4Bj96D1B4Bb42ekNpDM9ougQLY1QyXjXMobnmhqtgGA7zuMKuEbDAOuEmJPKuZf2Y58gdB04t89/1O/w1cDnyilFU="


def send_line_message(message_text):
    # LINEに全員一斉送信（ブロードキャスト）するためのURL
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
        print("LINEへの送信に成功しました！スマホを確認してください！")

    except requests.exceptions.RequestException as e:
        print(f"送信エラーが発生しました: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"詳細: {e.response.text}")


if __name__ == "__main__":
    test_message = "🎮 こんにちは。soraです！Pythonで作ったゲームニュースBotからのテスト送信です！"
    send_line_message(test_message)