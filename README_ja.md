[For English](https://github.com/Syogo-Suganoya/inkpost/blob/main/README.md)

# 日記生成ツール

## 概要

このツールは、X（旧Twitter）から取得したツイートと天気データを組み合わせて、日記形式のテキストを生成するプログラムです。また、生成された日記から画像生成に必要な要素を抽出し、画像生成APIを利用して関連する画像を生成します。

## 主な機能

1. **ツイート取得**
   - 指定されたユーザーのツイートを取得します。
   - モックデータを使用するオプションもあります。

2. **天気データ取得**
   - 指定された期間と場所の天気データを取得します。
   - モックデータまたは実際の天気データAPIを利用します。

3. **日記生成**
   - ツイート内容を日記形式に変換します。

4. **画像生成**
   - 日記の内容からシチュエーションや登場人物を抽出し、画像生成APIを利用して画像を生成します。

5. **ファイル出力**
   - 生成された日記と画像を指定のディレクトリに保存します。

## 使用技術

- **外部API**
  - 天気データ取得: [気象データ Web API](https://www.cultivationdata.net/weather-web-api.html)
  - 画像生成: Gemini
  - ツイート取得: Tweepy

## インストール

1. 必要なライブラリをインストールします。

    ```bash
    pip install -r requirements.txt
    ```

2. 環境変数を設定します。`.env` ファイルを作成し、以下の内容を記載してください。

    ```env
    X_API_KEY="YOUR_X_API_KEY"
    X_API_KEY_SECRET="YOUR_X_API_KEY_SECRET"
    X_ACCESS_TOKEN="YOUR_X_ACCESS_TOKEN"
    X_ACCESS_TOKEN_SECRET="YOUR_X_ACCESS_TOKEN_SECRET"
	X_BEARER_TOKEN="X_BEARER_TOKEN"
    GEMINI_KEY="YOUR_GEMINI_API_KEY"
    ```

## 実行方法

1. 実際のデータを使用して実行する場合：

    ```bash
    python src/main.py --user_name <ユーザー名> --location_name <地名> --start_date <開始日> --end_date <終了日>
    ```

    例：

    ```bash
    python src/main.py --user_name "example_user" --location_name "東京" --start_date "2023-05-01" --end_date "2023-05-07"
    ```

2. モックデータを使用して実行する場合：

    ```bash
    python src/main.py --mock
    ```

**注意事項:**

- `user_name` は X のユーザー名を指定してください。`@` は、あってもなくても構いません。
- `location_name` は [materials/station_data.json](https://github.com/Syogo-Suganoya/inkpost/blob/main/materials/station_data.json) に記載されている地名を参照してください。
- `start_date` と `end_date` は `yyyy-mm-dd` 形式の文字列で指定してください。
- `start_date` と `end_date` の期間は 1 ヶ月未満である必要があります。
  - `start_date=2024-03-20` のとき:
    - `end_date=2024-04-19` は OK
    - `end_date=2024-04-20` は NG

## 注意事項

- X APIの利用規約を遵守してください。
- 生成された日記や画像は、必ずしも現実的または適切であるとは限りません。利用前に十分な確認を行ってください。

## 課題と今後の展望

- **天気データ取得を気象庁APIに変更**
  気象庁の[過去の気象データ・ダウンロード](https://www.data.jma.go.jp/risk/obsdl/)が現在メンテナンス中のため、
  サードパーティの[API](https://www.cultivationdata.net/weather-web-api.html)を使用しています。このAPIも気象庁のデータを参照しています。
  メンテナンスが明け次第、直接気象庁のデータをダウンロードするように変更します。
