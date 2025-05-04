import os
import sys

from src.Common import common_variable
from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log




class DataIngestionConfig:
    def __init__(self):
        try:
            self.artifact = common_variable.ARTIFACT
            self.data_ingestion_dir = os.path.join(self.artifact,common_variable.DATA_INGESTIONDIR)
            self.data_file = os.path.join(self.data_ingestion_dir,common_variable.DATA_FILE)
            

        except Exception as e :
            my_log.info(e)
            raise MyException(e,sys)
        
class DataValidationConfig:
    def __init__(self):
        try:
            self.data_validation_dir = os.path.join(common_variable.ARTIFACT,common_variable.DATA_VALIDATION)
            self.data_file = os.path.join(self.data_validation_dir,
                                          common_variable.DATA_FILE)
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
class DataTransformationConfig:
    def __init__(self):
        try:
            self.yaml_path = 'params/colums.yaml'
            self.data_transformation_dir = os.path.join(common_variable.ARTIFACT,common_variable.DATA_TRANSFORMATION_DIR)
            self.transformed_train = os.path.join(self.data_transformation_dir,common_variable.TRAIN_FILE)
            self.transformed_test = os.path.join(self.data_transformation_dir,common_variable.TEST_FILE)
            self.model_file = os.path.join(common_variable.MODEL_DIR,common_variable.PREMODEL_FILE)
            
        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)

class ModelTrainConfig:
    def __init__(self):
        try:
            self.model_thresold : float = 0.5
            self.prams_file : str = "params/params.yaml"
            self.model_file : str = os.path.join(common_variable.MODEL_DIR,common_variable.MODEL_FILE)
        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
        
class ModelEvaluationConfig:
    try:
        pass
    except Exception as e :
        my_log.error(e)
        raise MyException(e,sys)

