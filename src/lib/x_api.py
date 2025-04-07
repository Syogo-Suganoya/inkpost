import json
import os
from collections import namedtuple
from datetime import datetime

import tweepy

X_API_KEY = os.environ.get("X_API_KEY")
X_API_KEY_SECRET = os.environ.get("X_API_KEY_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.environ.get("X_ACCESS_TOKEN_SECRET")
X_BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN")


def get_trends(woeid):
    """
    指定された場所のトレンドを取得します。
    """

    auth = tweepy.OAuthHandler(X_API_KEY, X_API_KEY_SECRET)
    auth.set_access_token(X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # トレンド一覧取得
    trends = api.get_place_trends(woeid)
    return [trend["name"] for trend in trends[0]["trends"]]


def get_trends_mock(file_path, num_posts=10):
    """
    モックのトレンドポストデータを読み込みます。
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            posts = json.load(f)
        return posts[:num_posts]
    except FileNotFoundError:
        print(f"ファイルが見つかりませんでした: {file_path}")
        return []


def client_x():
    """
    X APIのクライアント
    """
    return tweepy.Client(
        bearer_token=X_BEARER_TOKEN,
        consumer_key=X_API_KEY,
        consumer_secret=X_API_KEY_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_TOKEN_SECRET,
    )


def post_post(text, post_id=None):
    """
    X に投稿または返信します。
    """

    try:
        client = client_x()
        post_params = {"text": text}
        if post_id:
            post_params["in_reply_to_post_id"] = post_id
        response = client.create_post(**post_params)
        print(f"X に投稿/返信しました: {response}")
        return response.data["id"]  # 投稿IDを返す
    except tweepy.TweepyException as e:
        print(f"X API エラー: {e}")
        return None


def get_user_posts(name, max_results=None, start_date=None, end_date=None):
    """
    ユーザーの投稿を取得します。
    """
    client = client_x()
    # ユーザーIDを取得
    if name.startswith("@"):
        name = name[1:]
    else:
        name = name
    user = client.get_user(username=name)
    user_id = user.data.id
    post_fields = ["created_at", "text"]
    params = {"id": user_id, "post_fields": post_fields}
    if start_date:
        params["start_time"] = start_date.isoformat() + "Z"
    if end_date:
        params["end_time"] = end_date.isoformat() + "Z"
    if max_results:
        params["max_results"] = max_results
    posts = client.get_users_posts(**params)
    return posts


def get_user_posts_mock():
    """
    get_user_posts のモックデータ
    """
    MockPost = namedtuple("MockPost", ["created_at", "text"])

    class MockResponse:
        def __init__(self, data):
            self.data = data

    with open("mock/post.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    MockPost = namedtuple("MockPost", ["created_at", "text"])
    return MockResponse([MockPost(datetime.strptime(post["created_at"], "%Y-%m-%d %H:%M:%S"), post["text"]) for post in data])
