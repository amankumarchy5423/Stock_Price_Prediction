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
    def __init__(self,config : DataIngestionConfig,
                 artifact = DataIngestionArtifact()):
        try :
            self.config = config
            self.artifact = artifact
            self.client = pymongo.MongoClient(os.getenv('MONGO_URL'))
            self.data = None
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
    def data_fetch(self):
        try :
            
            self.data = self.client[os.getenv('MONGO_DB')][os.getenv('MONGO_COLLECTION')] .find()
            my_log.info("data fetched from mogo atlas ")

        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
        
    def data_local(self):
        try:
            pass
        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
        
    def initiate_dataingestion(self):
        try:
            pass
        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)