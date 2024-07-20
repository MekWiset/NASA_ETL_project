import pandas as pd


def read_data(file_path: str) -> pd.DataFrame:
    '''Reads a CSV file and returns a DataFrame.'''
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f'Error while trying to read csv: {e}')
    return df

def filter_wildfires(file_path: str, output_path: str) -> None:
    '''Filters wildfires from the DataFrame and saves to a CSV file.'''
    df = read_data(file_path=file_path)
    df_wildfires = df[df['category_id'] == 8]

    # Save output as .csv file
    try:
        df_wildfires.to_csv(output_path, index=False)
    except IOError as e:
        print(f'Error saving DataFrame to CSV: {e}')

    return df_wildfires


if __name__ == '__main__':

    file_path = 'output/transformed_nasa_events.csv'
    output_path = 'output/wildfire_events.csv'
    
    filter_wildfires(file_path=file_path, output_path=output_path)