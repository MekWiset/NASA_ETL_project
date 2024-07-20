import pandas as pd
import numpy as np
import ast


def read_data(file_path: str) -> pd.DataFrame:
    '''Reads a CSV file and returns a DataFrame.'''
    try: 
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f'Error while trying to read csv: {e}')
    return df


def transform_event(file_path: str) -> pd.DataFrame:
    '''Transforms event data.'''
    df = read_data(file_path=file_path)
    df_events = df[['id', 'title']]

    return df_events


def transform_source(file_path: str) -> pd.DataFrame:
    '''Transforms source data.'''
    df = read_data(file_path=file_path)

    df['sources'] = df['sources'].apply(ast.literal_eval)
    df_source = df[['sources']].explode('sources').reset_index(drop=True)
    df_source = pd.json_normalize(df_source['sources'])

    df_source = df_source.drop(columns = ['url'])
    df_source = df_source.rename(columns = {'id' : 'source'})

    return df_source


def transform_category(file_path: str) -> pd.DataFrame:
    '''Transforms category data.'''
    df = read_data(file_path=file_path)

    df['categories'] = df['categories'].apply(ast.literal_eval)
    df_category = df[['categories']].explode('categories').reset_index(drop=True)
    df_category = pd.json_normalize(df_category['categories'])
    df_category = df_category.add_prefix('category_')

    return df_category


def location_flag_identifier(row):
    '''Identifies if the location has both latitude and longitude.'''
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        return '1'
    else:
        return '0'


def transform_geometry(file_path: str) -> pd.DataFrame:
    '''Transforms geometry data.'''
    df = read_data(file_path=file_path)

    df['geometries'] = df['geometries'].apply(ast.literal_eval)
    df_geometry = df[['geometries']].explode('geometries').reset_index(drop=True)
    df_geometry = pd.json_normalize(df_geometry['geometries'])

    df_geometry['time'] = df_geometry['date'].str[11:19].replace('00:00:00', np.nan)
    df_geometry['date'] = df_geometry['date'].str[0:10]

    df_geometry['latitude'] =  df_geometry['coordinates'].apply(lambda x : x[0]).astype(str)
    df_geometry['latitude'] = df_geometry['latitude'].str.rstrip('0')
    df_geometry['longitude'] =  df_geometry['coordinates'].apply(lambda x : x[1]).astype(str)
    df_geometry['longitude'] = df_geometry['longitude'].str.rstrip('0')

    df_geometry['locationFlag'] = df_geometry.apply(location_flag_identifier, axis=1)
    df_geometry.insert(2, 'locationFlag', df_geometry.pop('locationFlag'))

    df_geometry = df_geometry.drop(columns = ['type', 'coordinates'])

    column_order = ['date', 'time', 'locationFlag', 'latitude', 'longitude']
    df_geometry = df_geometry[column_order]

    return df_geometry


def final_transform(file_path: str, output_path: str) -> None:
    '''Performs the final transformation and saves the result to a CSV file.'''
    df_event = transform_event(file_path=file_path)
    df_source = transform_source(file_path=file_path)
    df_category = transform_category(file_path=file_path)
    df_geometry = transform_geometry(file_path=file_path)

    df_merged = pd.concat([df_event, df_source, df_category, df_geometry], axis=1)
    df_merged = df_merged.dropna(subset=['id'])
    df_merged_sorted = df_merged.sort_values(by = ['category_id', 'date', 'time'], ascending=True)
    
    # Save output as .csv file
    try:
        df_merged_sorted.to_csv(output_path, index=False)
    except IOError as e:
        print(f'Error saving DataFrame to CSV: {e}')


if __name__ == '__main__':

    final_transform(file_path='datasets/nasa_events.csv', output_path='output/transformed_nasa_events.csv')

