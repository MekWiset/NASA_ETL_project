import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import timedelta
import os
from dotenv import load_dotenv
from pathlib import Path

from plugins.extract.extract_from_api import extract_nasa_data
from plugins.transform.transform_events import final_transform
from plugins.transform.filter_wildfires import filter_wildfires
from plugins.load.export import export_to_mysql, export_to_postgres, export_to_mongodb, export_to_s3


dotenv_path = Path('.env')
load_dotenv(dotenv_path = dotenv_path)

# Variables
NASA_API_KEY = os.getenv('NASA_API_KEY')
NASA_URL = os.getenv('NASA_URL')

MYSQL_CONN_STRING = os.getenv('MYSQL_CONN_STRING')

PG_USERNAME = os.getenv('PG_USERNAME')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_DBNAME = os.getenv('PG_DBNAME')
PG_HOST = os.getenv('PG_HOST')

MONGO_CLIENT = os.getenv('MONGO_CLIENT')
MONGO_DB = os.getenv('MONGO_DB')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET = os.getenv('AWS_BUCKET')

dataset_path = 'datasets/nasa_events.csv'
transformed_file_path = 'output/transformed_nasa_events.csv'
wildfire_file_path = 'output/wildfire_events.csv'
s3_object_key = 'wildfire_events.csv'


default_args = {
    'owner': 'Mek',
    'retries': 1,
    'retry_delay': timedelta(seconds=3)
}

with DAG(

    default_args = default_args,
    dag_id = 'nasa_events',
    description = 'DAG to process and export NASA event data',
    start_date = airflow.utils.dates.days_ago(1),
    schedule_interval = None,
    catchup = False

)as dag:
    
    start_task = EmptyOperator(
        task_id = 'start'
    )

    extract_from_api_task = PythonOperator(
        task_id = 'extract_from_api',
        python_callable = extract_nasa_data,
        op_kwargs = {
            'api_key': NASA_API_KEY,
            'url': NASA_URL,
            'output_path': dataset_path
            }
    )

    transform_data_task = PythonOperator(
        task_id = 'transform_data',
        python_callable = final_transform,
        op_kwargs = {
            'file_path': dataset_path,
            'output_path': transformed_file_path
            }
    )

    filter_wildfires_task = PythonOperator(
        task_id = 'filter_wildfires',
        python_callable = filter_wildfires,
        op_kwargs = {
            'file_path': transformed_file_path,
            'output_path': wildfire_file_path
            }
    )

    export_to_mysql_task = PythonOperator(
        task_id = 'export_to_mysql',
        python_callable = export_to_mysql,
        op_kwargs = {
            'file_path': transformed_file_path,
            'mysql_conn_string': MYSQL_CONN_STRING
            }
    )

    export_to_postgres_task = PythonOperator(
        task_id = 'export_to_postgres',
        python_callable = export_to_postgres,
        op_kwargs = {
            'file_path': transformed_file_path,
            'username': PG_USERNAME,
            'password': PG_PASSWORD,
            'dbname': PG_DBNAME,
            'host': PG_HOST
            }
    )

    export_to_mongodb_task = PythonOperator(
        task_id = 'export_to_mongo',
        python_callable = export_to_mongodb,
        op_kwargs = {
            'file_path': wildfire_file_path,
            'client': MONGO_CLIENT,
            'db': MONGO_DB,
            'collection': MONGO_COLLECTION
            }
    )

    export_to_s3_task = PythonOperator(
        task_id = 'export_to_aws_s3',
        python_callable = export_to_s3,
        op_kwargs = {
            'file_path': wildfire_file_path,
            'access_key': AWS_ACCESS_KEY_ID,
            'secret_key': AWS_SECRET_ACCESS_KEY,
            'bucket_name': AWS_BUCKET,
            'object_key': s3_object_key
            }
    )

    # Task Dependencies
    start_task >> extract_from_api_task >> transform_data_task >> filter_wildfires_task
    filter_wildfires_task >> [export_to_mysql_task, export_to_postgres_task, export_to_mongodb_task, export_to_s3_task]