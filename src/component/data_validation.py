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
        
    def initiate_datavalidation(self):
        try:
            data = open_file(self.artifact.data_dir)
            my_log.info("data loaded successfully...")
        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
