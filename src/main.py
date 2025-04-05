import argparse
import os
from argparse import ArgumentParser
from datetime import datetime, timedelta

from dotenv import load_dotenv

from lib import gemini_api, text, validation, whether, x_api


class DiaryDataset:
    def __init__(self):
        self.user_name = None
        self.location_name = None
        self.start_date = None
        self.end_date = None
        self.tweets = []
        self.weather_data = {}

        self._load_metadata()
        self._load_weather_data()

    def _load_metadata(self):
        if args.mock:
            self.user_name = "j4pam5muuw"
            self.location_name = "東京"
            self.start_date = datetime.strptime("2023-05-01", "%Y-%m-%d")
            self.end_date = datetime.strptime("2023-05-02", "%Y-%m-%d")
            self.tweets = x_api.get_user_tweets_mock()
        else:
            self.user_name = args.user_name
            self.location_name = args.location_name
            self.start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
            self.end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
            self.tweets = x_api.get_user_tweets(self.user_name)

        validation.validate_dates(self.start_date, self.end_date)

    def _load_weather_data(self):
        months = {(self.start_date.year, self.start_date.month), (self.end_date.year, self.end_date.month)}

        for year, month in months:
            if args.mock:
                path = f"絵日記/mock/weather/{year}{month:02d}.json"
                raw = text.load_json(path)
            else:
                raw = whether.get_past_weather(self.location_name, year, month)

            daily = whether.extract_daily_weather(raw)
            self.weather_data.update(daily)


def tweet_to_diary(tweet_text):
    """
    ツイートの内容を日記の文体に変換する
    """
    prompt_template = text.read_text_file("絵日記/prompt/tweet_to_diary.txt")
    prompt = prompt_template.replace("###TWEET_TEXT###", tweet_text)
    result = gemini_api.query(prompt)
    return result


def extract_diary_for_image(diary_text):
    """
    日記のテキストから画像生成に必要なシチュエーションや登場人物などの要素を抽出する
    """
    prompt_template = text.read_text_file("絵日記/prompt/diary_to_situation.txt")
    prompt = prompt_template.replace("###DIARY_TEXT###", diary_text)
    result = gemini_api.query(prompt)
    return result


def parse_args():
    parser = ArgumentParser(description="日記生成ツール")

    parser.add_argument("--mock", action="store_true", help="モックデータを使用する")

    parser.add_argument("--user_name", type=str, help="Xのユーザー名")
    parser.add_argument("--location_name", type=str, help="天気の取得に使う地名")
    parser.add_argument("--start_date", type=str, help="開始日 (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, help="終了日 (YYYY-MM-DD)")

    args = parser.parse_args()

    # バリデーション
    if args.mock:
        # モック使用時は他の引数を指定してはいけない
        if any([args.user_name, args.location_name, args.start_date, args.end_date]):
            parser.error("--mock を指定した場合、--user_name、--location_name、--start_date、--end_date は指定できません。")
    else:
        # 実データ使用時は全ての引数が必要
        missing = [opt for opt in ["user_name", "location_name", "start_date", "end_date"] if getattr(args, opt) is None]
        if missing:
            parser.error(f"--mock を使わない場合、以下の引数が必要です: {', '.join('--' + m for m in missing)}")

    return args


def main():
    dataset = DiaryDataset()

    tweets_by_date = {}
    if dataset.tweets.data:
        for tweet in dataset.tweets.data:
            tweet_date = tweet.created_at.strftime("%Y-%m-%d")
            tweets_by_date.setdefault(tweet_date, []).append(tweet.text)

    current_date = dataset.start_date
    while current_date <= dataset.end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        directory = os.path.join("dialy", date_str)
        # ディレクトリがない場合は作成
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        diary_intro = f"{date_str}: {dataset.weather_data[date_str]}\n"
        if date_str in tweets_by_date:
            # 日記文章の生成
            posts = "\n".join(tweets_by_date[date_str])
            diary_text = tweet_to_diary(posts)
            # 絵の生成
            contents = extract_diary_for_image(diary_text)
            gemini_api.image_genrate(contents, directory)
        else:
            # 投稿がない日
            diary_text = "何もありませんでした。"
        text.write_to_file(os.path.join(directory, "diary.txt"), "\n".join([diary_intro, diary_text]))
        current_date += timedelta(days=1)


if __name__ == "__main__":
    load_dotenv("絵日記/.env")
    parser = argparse.ArgumentParser(description="トレンド分析とアイデア生成")
    parser.add_argument("--mock", action="store_true", help="モックデータを使用する")
    args = parse_args()
    # main()
