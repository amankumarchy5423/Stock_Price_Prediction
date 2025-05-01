from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
from src.config.project_config import DataIngestionConfig
from src.Artifact.project_artifact import DataIngestionArtifact

import pandas as pd
import numpy as np
import os,sys
import pymongo
from dotenv import load_dotenv
load_dotenv()


class DataIngestion:
    def __init__(self,config : DataIngestionConfig):
        try :
            self.config = config
            # self.artifact = artifact
            self.client = pymongo.MongoClient(os.getenv('MONGO_URL'))
            self.data : pd.DataFrame = None
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
    def data_fetch(self):
        try :
            
            cloud_data  = self.client[os.getenv('MONGO_DB')][os.getenv('MONGO_COLLECTION')] .find()
            my_log.info("data fetched from mogo atlas ")

            self.data  = (pd.DataFrame(cloud_data))
            self.data.drop(columns=['_id'],inplace=True)
            my_log.info("cloud data is converted into pd.DataFrame ")

        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
        
    def data_local(self) -> None:
        try:
            os.makedirs(self.config.artifact , exist_ok=True)
            os.makedirs(self.config.data_ingestion_dir,exist_ok=True)
            my_log.info("Directory created ...")

            self.data.to_csv(self.config.data_file)
            my_log.info("data save into local directory")

        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
        
    def initiate_dataingestion(self) -> DataIngestionArtifact:
        try:
            self.data_fetch()
            my_log.info("data fetching ended")

            self.data_local()
            my_log.info("data_local saves successfully ")

            return DataIngestionArtifact(data_dir = self.config.data_file)

        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)