from src.component.data_ingestion import DataIngestion
from src.loggers.logger import my_log
from src.Exception.Project_Exception import MyException
from src.config.project_config import DataIngestionConfig

import os,sys


class TrainPipeline:
    def __init__(self) -> None:
        try:
           pass

        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
    def data_ingestion(self) -> None:
        try:
            my_log.info("<<< DataIngestion started >>>")
            config_obj = DataIngestionConfig()
            my_log.info("data ingestion object created ...")

            dataingestionobj = DataIngestion(config=config_obj)
            dataingestionobj.initiate_dataingestion()
            my_log.info("DataIngestion successfully completed ..." )

            my_log.info("<<< DataIngestion ended >>>")
        except Exception as e :
            my_log.error (e)
            raise MyException(e,sys)
        
    def initiate_pipeline(self) -> None:
        try:
            my_log.info(" <<< train pipeline started >>>")
            
            self.data_ingestion()

            my_log.info(" <<< train pipeline ended >>>")
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)