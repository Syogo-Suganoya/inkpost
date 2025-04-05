"""
https://www.cultivationdata.net/weather-web-api.html
"""

from datetime import datetime

import requests

from lib import text


def get_past_weather(location_name: str, year: int, month: int):
    """
    地点名、年、月を指定して過去の気象情報を取得する。
    """
    station_data = text.load_json("station_data.json")
    station_no = station_data.get(location_name)

    if not station_no:
        return {"error": f"地点名 '{location_name}' に対応する国際地点番号が見つかりません"}

    # APIのURL
    api_url = "https://api.cultivationdata.net/past"

    # リクエストパラメータ
    params = {"no": station_no, "year": year, "month": month}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": f"APIリクエストに失敗: {e}"}


def extract_daily_weather(weather_data):
    """
    過去の天気データから日ごとの天気を抽出する。

    :param weather_data: get_past_weather の返り値（JSON形式）
    :return: 日ごとの天気データ（辞書形式）
    """
    # 取得データが空、または期待するキーがない場合はエラー
    if not weather_data or not isinstance(weather_data, dict):
        return {"error": "データが無効です"}

    location_name = next(iter(weather_data.keys()))  # 最初のキー（地点名）を取得
    daily_data = weather_data.get(location_name, {})

    # 各日付の天気を判定
    daily_weather = {}
    for date, details in daily_data.items():
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        daily_weather[formatted_date] = details.get("天気概況（昼）", None)
    return daily_weather


def classify_weather(rainfall):
    """
    降水量に応じて天気を分類。数値でない場合は None を返す
    """
    try:
        rainfall = float(rainfall)
    except (ValueError, TypeError):
        return None  # 数値でない場合は None を返す
    if rainfall == 0.0:
        return "晴れ☀"
    elif 0.1 <= rainfall <= 1.0:
        return "曇り☁"
    else:
        return "雨🌧"
