import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient
import boto3
import os
from dotenv import load_dotenv
from pathlib import Path


def read_data(file_path: str) -> pd.DataFrame:
    '''Reads a CSV file and returns a DataFrame.'''
    try: 
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f'Error while trying to read csv: {e}')

    return df


def export_to_mysql(file_path: str, mysql_conn_string: str) -> None:
    '''Export a dataframe to MySQL database'''
    try:
        df_to_export = read_data(file_path=file_path)
        
        ms_engine = create_engine(mysql_conn_string)
        df_to_export.to_sql(name='nasamysql', con=ms_engine, if_exists='replace', index=False)
        
        print('Data successfully exported to MySQL database.')

    except Exception as e:
        print(f'An error occurred: {e}')


def export_to_postgres(file_path: str, username: str, password: str, dbname: str, host: str) -> None:
    '''Export a dataframe to Postgres database'''
    try:
        df_to_export = read_data(file_path=file_path)

        pg_engine = create_engine(f'postgresql://{username}:{password}@{host}/{dbname}')
        df_to_export.to_sql('events', con = pg_engine, if_exists = 'replace', index = False)
        
        print('Data successfully exported to Postgres database.')

    except Exception as e:
        print(f'An error occurred: {e}')


def export_to_mongodb(file_path: str, client: str, db: str, collection: str) -> None:
    '''Export a dataframe to MongoDB'''
    try:
        df_to_export = read_data(file_path=file_path)

        client = MongoClient(client)
        db = client[db]
        collection = db[collection]

        df_json = df_to_export.to_dict(orient='records')
        collection.insert_many(df_json)

        print('Data successfully exported to MongoDB.')

    except Exception as e:
        print(f'An error occurred: {e}')


def export_to_s3(file_path: str, access_key: str, secret_key: str, bucket_name: str, object_key: str) -> None:
    '''Export a csv file to AWS S3 storage'''
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key
        )

        with open(file_path, 'rb') as data:
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)

        print('Data successfully exported to AWS S3.')

    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':

    dotenv_path = Path('.env')
    load_dotenv(dotenv_path = dotenv_path)

    transformed_events_path = 'output/transformed_nasa_events.csv'
    wildfires_events_path = 'output/wildfires_events.csv'

    # Export to MySQL
    MYSQL_CONN_STRING = os.getenv('MYSQL_CONN_STRING')
    export_to_mysql(file_path=transformed_events_path, mysql_conn_string=MYSQL_CONN_STRING)

    # Export to Postgres
    PG_USERNAME = os.getenv('PG_USERNAME')
    PG_PASSWORD = os.getenv('PG_PASSWORD')
    PG_DBNAME = os.getenv('PG_DBNAME')
    PG_HOST = os.getenv('PG_HOST')
    export_to_postgres(file_path=transformed_events_path, username=PG_USERNAME, password=PG_PASSWORD, dbname=PG_DBNAME, host=PG_HOST)

    # Export to MongoDB
    MONGO_CLIENT = os.getenv('MONGO_CLIENT')
    MONGO_DB = os.getenv('MONGO_DB')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')
    export_to_mongodb(file_path=wildfires_events_path, client=MONGO_CLIENT, db=MONGO_DB, collection=MONGO_COLLECTION)

    # Export to AWS S3
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_BUCKET = os.getenv('AWS_BUCKET')
    export_to_s3(file_path=wildfires_events_path, access_key=AWS_ACCESS_KEY_ID, secret_key=AWS_SECRET_ACCESS_KEY, bucket_name=AWS_BUCKET, object_key='wildfire_events.csv')
    