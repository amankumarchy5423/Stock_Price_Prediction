from src.loggers.logger import my_log
from src.Exception.Project_Exception import MyException
from src.component.data_validation import DataValidation
import numpy as np

import boto3
import joblib
import os,sys
import pandas as pd
from io import BytesIO


class PredictPipe:
    def __init__(self,data : pd.DataFrame):
        try:
            self.data = data
        except Exception as e:
            my_log.error(f"Error in PredictPipe init: {e}")
            raise MyException(e,sys)
        
    def handle_date_time(self, data: pd.DataFrame) -> any:
        try:
            my_log.info("Converting timestamp column to datetime...")
            data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')

            my_log.info("Separating timestamp into various attributes...")

            data['year'] = data['timestamp'].dt.year
            data['month'] = data['timestamp'].dt.month
            data['day'] = data['timestamp'].dt.day
            data['day_of_week'] = data['timestamp'].dt.dayofweek
            data['is_weekend'] = data['day_of_week'].isin([5, 6]).astype(int)

            my_log.info("Timestamp successfully split into year, month, day, day_of_week, and is_weekend.")

            data1 = data.drop(columns=['timestamp'])
            return data1

        except Exception as e:
            my_log.error(e)
            raise MyException(e, sys)

    def load_cloud_model(self) -> float:
        try:
            s3_client = boto3.client('s3',
                              aws_access_key_id = 'AKIA5MSUB5SJUMK7KNN6',
                              aws_secret_access_key = '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',
                              region_name = 'us-east-1')
            
            response = s3_client.get_object(Bucket = 'stock-price-bucket-aman',Key = 'models/ml_model/model.joblib')
            model_byte = response['Body'].read()
            model = joblib.load(BytesIO(model_byte))
            my_log.info(" ml model is loaded from cloud")

            response_pre = s3_client.get_object(Bucket = 'stock-price-bucket-aman',Key = 'models/ml_model/preprocessor.joblib')
            pre_byte = response_pre['Body'].read()
            pre_model = joblib.load(BytesIO(pre_byte))
            my_log.info(" preprocessor is loaded from cloud")

            my_log.info(f" data by the user {self.data}")

            data_1 = self.handle_date_time(self.data)
            my_log.info(f"date time handeled {data_1}")

            data_2 = pre_model.transform(data_1)
            my_log.info(f" transformed data {data_2}")

            data_3 = np.array(data_2)
            new_data = np.insert(data_3, 0, 1, axis=1)
            my_log.info(f" new data look like {new_data}")

            predict = model.predict(new_data)
            my_log.info(f" prediction {predict}")

            return predict

        except Exception as e:
            my_log.error(f"Error in load_cloud_model: {e}")
            raise MyException(e,sys)
        
    