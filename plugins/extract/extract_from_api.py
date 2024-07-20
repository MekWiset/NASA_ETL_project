import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path


def flatten_nested_column(raw_df: pd.DataFrame, col: str) -> pd.DataFrame:
    '''Flattens a nested column in a DataFrame.'''
    flattened_df = pd.json_normalize(raw_df[col])
    return flattened_df


def extract_nasa_data(api_key: str, url: str, output_path: str) -> None:
    '''Fetches data from the NASA API, processes it, and saves to a CSV file.'''
    params = {
        'api_key' : api_key,
        'hd' : 'TRUE',
        'date' : '2023-12-18'
    }

    try:
        response = requests.get(url, params=params)
        json_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data from NASA API: {e}')
    else:
        raw_df = pd.DataFrame(json_data)

    extracted_flattened_df = flatten_nested_column(raw_df=raw_df, col='events')

    # Save output as .csv file
    try:
        extracted_flattened_df.to_csv(output_path, index=False)
    except IOError as e:
        print(f"Error saving DataFrame to CSV: {e}")


if __name__ == '__main__':

    dotenv_path = Path('.env')
    load_dotenv(dotenv_path = dotenv_path)

    api_key = os.getenv('NASA_API_KEY')
    url = os.getenv('NASA_URL')

    extract_nasa_data(api_key=api_key, url=url, output_path='datasets/nasa_events.csv')

