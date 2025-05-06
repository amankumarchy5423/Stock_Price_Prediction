from src.loggers.logger import my_log
from src.Exception.Project_Exception import MyException

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

    def load_cloud_model(self):
        try:
            s3 = boto3.client('s3')
        except Exception as e:
            my_log.error(f"Error in load_cloud_model: {e}")
            raise MyException(e,sys)
        
    