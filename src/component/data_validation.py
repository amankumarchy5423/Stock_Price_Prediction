from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
from src.Artifact.project_artifact import DataValidationArtifact,DataIngestionArtifact
from src.config.project_config import DataValidationConfig
from src.utility.project_utils import open_file

import os,sys
import pandas as pd 



class DataValidation:
    def __init__(self,artifact : DataIngestionArtifact,
                 config : DataValidationConfig):
        try:
            self.artifact = artifact
            self.config = config
        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
        
    def duplicate_data_deletion(self,data : pd.DataFrame) -> any:
        try:
            duplicate_data = data[data.duplicated()]
            my_log.info(f"these are duplicate data {duplicate_data} and their shape is {duplicate_data.shape}")

            data_1 = data.drop_duplicates()
            my_log.info("duplicate data deleted ...")

            return data_1

        except Exception as e:
            my_log.error(e)
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
        
    def outlier_handling(self,data : pd.DataFrame):
        try:
            pass
        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)

        
    def data_save_artifact(self,data : pd.DataFrame) -> any :
        try :
            os.makedirs(self.config.data_validation_dir,exist_ok=True)
            my_log.info("data validation dir created ...")

            my_log.info(f" data saved at {self.config.data_file}")
            data.to_csv(self.config.data_file)
            my_log.info("data saved in artifact ")
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
    def initiate_datavalidation(self):
        try:
            data = open_file(self.artifact.data_dir)
            my_log.info("data loaded successfully...")

            data_v1 = self.duplicate_data_deletion(data=data)
            my_log.info("duplicate_data_deletion is successfully completed ..")

            data_v2 = self.handle_date_time(data_v1)
            my_log.info("handle_date_time is successfully completed ..")

            data_v3 = self.data_save_artifact(data_v2)
            my_log.info("data_save_artifact is successfully completed ..")

            return DataIngestionArtifact(data_dir=self.config.data_file)

        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
