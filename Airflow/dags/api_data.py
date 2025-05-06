from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from pymongo import MongoClient
import requests
import os

from dotenv import load_dotenv
load_dotenv()


MONGO_URI = os.getenv('MONGO_URL')
DB_NAME = 'stock_price_db'
COLLECTION_NAME = 'stock_data'

# Mongo insert function
def insert_to_mongo(data):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        stock_data = {
            'stock_symbol': 'IBM',
            'open': data['open'],
            'high': data['high'],
            'low': data['low'],
            'close': data['close'],
            'volume': data['volume'],
            'timestamp': datetime.now()
        }
        collection.insert_one(stock_data)
        print(f"Data inserted for {stock_data['stock_symbol']} at {stock_data['timestamp']}")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")

# DAG definition
with DAG(
    dag_id='price_prediction_data',
    start_date=datetime(2023, 3, 21),
    schedule_interval='@hourly',
    catchup=False
) as dag:

    @task
    def get_stock_data():
        url = os.getenv('API')
        r = requests.get(url)
        return r.json()

    @task
    def transform_data(response: dict):
        try:
            timeseries = response.get("Time Series (5min)", {})
            if not timeseries:
                raise ValueError("Time series data is missing in the response")

            latest_date = max(timeseries.keys())
            latest_data = timeseries[latest_date]

            api_data = {
                'open': latest_data.get('1. open', ''),
                'high': latest_data.get('2. high', ''),
                'low': latest_data.get('3. low', ''),
                'close': latest_data.get('4. close', ''),
                'volume': latest_data.get('5. volume', '')
            }
            return api_data
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {}

    @task
    def insert_transformed_data_into_mongo(transformed_data: dict):
        insert_to_mongo(transformed_data)

    
    raw_data = get_stock_data()
    transformed = transform_data(raw_data)
    insert_transformed_data_into_mongo(transformed)
