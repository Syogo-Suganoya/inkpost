[日本語版](https://github.com/Syogo-Suganoya/inkpost/blob/main/README_ja.md)

# Diary Generation Tool

## Overview

This tool generates diary-style text by combining tweets retrieved from X (formerly Twitter) with weather data. Additionally, it extracts elements from the generated diary necessary for image creation and uses an image generation API to produce related images.

## Key Features

1. **Tweet Retrieval**
   - Fetches tweets from a specified user.
   - Option to use mock data is also available.

2. **Weather Data Retrieval**
   - Retrieves weather data for a specified period and location.
   - Can use either mock data or real weather data APIs.

3. **Diary Generation**
   - Converts tweet content into a diary format.

4. **Image Generation**
   - Extracts situations and characters from the diary and uses an image generation API to create images.

5. **File Output**
   - Saves the generated diary and images to a specified directory.

## Technologies Used

- **External APIs**
  - Weather data retrieval: [Weather Data Web API](https://www.cultivationdata.net/weather-web-api.html)
  - Image generation: Gemini
  - Tweet retrieval: Tweepy

## Installation

1. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

2. Set up environment variables. Create a `.env` file with the following content:

    ```env
    X_API_KEY="YOUR_X_API_KEY"
    X_API_KEY_SECRET="YOUR_X_API_KEY_SECRET"
    X_ACCESS_TOKEN="YOUR_X_ACCESS_TOKEN"
    X_ACCESS_TOKEN_SECRET="YOUR_X_ACCESS_TOKEN_SECRET"
    X_BEARER_TOKEN="X_BEARER_TOKEN"
    GEMINI_KEY="YOUR_GEMINI_API_KEY"
    ```

## How to Run

1. To run using actual data:

    ```bash
    python src/main.py --user_name <user_name> --location_name <location> --start_date <start_date> --end_date <end_date>
    ```

    Example:

    ```bash
    python src/main.py --user_name "example_user" --location_name "Tokyo" --start_date "2023-05-01" --end_date "2023-05-07"
    ```

2. To run using mock data:

    ```bash
    python src/main.py --mock
    ```

**Notes:**

- `user_name` should be the X username. The `@` symbol is optional.
- `location_name` should correspond to a location listed in [materials/station_data.json](https://github.com/Syogo-Suganoya/inkpost/blob/main/materials/station_data.json).
- `start_date` and `end_date` must be strings in `yyyy-mm-dd` format.
- The period between `start_date` and `end_date` must be less than one month.
  - Example:
    - `start_date=2024-03-20` → `end_date=2024-04-19` ✅
    - `start_date=2024-03-20` → `end_date=2024-04-20` ❌

## Caution

- Comply with X API terms of service.
- The generated diary entries and images may not always be realistic or appropriate. Please verify before use.

## Challenges & Future Plans

- **Switch Weather Data Retrieval to JMA API**
  Currently, the Japan Meteorological Agency's [historical weather data download](https://www.data.jma.go.jp/risk/obsdl/) is under maintenance, so a third-party [API](https://www.cultivationdata.net/weather-web-api.html) is being used, which references JMA data.
  Once maintenance is complete, the tool will be updated to download data directly from JMA.
