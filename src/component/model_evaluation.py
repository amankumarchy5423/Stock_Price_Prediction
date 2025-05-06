from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
from src.config.project_config import ModelEvaluationConfig
from src.Artifact.project_artifact import ModelTrainerArtifact,DataTransformationArtifact
from src.cloud.cloud_conn import AwsConn
from src.utility.project_utils import check_bucket,scoring_value

import os,sys
import numpy as np
import pandas as pd
import boto3
import mlflow
import joblib
from io import BytesIO



class ModelEvaluation:
    def __init__(self ,config : ModelEvaluationConfig,artifact : ModelTrainerArtifact,
                 transformation_artifact : DataTransformationArtifact):
        try:
            self.config = config
            self.artifact = artifact
            self.trans_artifact = transformation_artifact
        except Exception as e:
            my_log.error(f"Error in ModelEvaluation __init__ : {str(e)}")
            raise MyException(f"Error in ModelEvaluation __init__ : {str(e)}",sys)
        
    def load_cloud_model(self) -> object:
        try:
            if check_bucket(self.config.bucket_name):
                cloud_obj = AwsConn.s3_client.get_object(Bucket =self.config.bucket_name, Key=self.config.model_key)
                my_log.info("a copy of cloud object is created ..")

                model_byte = cloud_obj['Body'].read()
                cloud_model = joblib.load(BytesIO(model_byte))
                my_log.info("cloud model is loaded ..")

                return cloud_model
            return None
        except Exception as e:
            my_log.error(f"Error in ModelEvaluation load_cloud_model : {str(e)}")
            raise MyException(f"Error in ModelEvaluation load_cloud_model : {str(e)}",sys)
    
    def evaluate_model(self,cloud_model : any,x_data : pd.DataFrame,y_data : pd.DataFrame) -> bool:
        try:
            if cloud_model is not None:
               local_model = joblib.load(self.artifact.model_file)
            #    preprocessor = joblib.load(self.artifact.preprocessor_file)
               my_log.info("local model and preprocessor loaded is loaded ..")

            #    transformed_data = preprocessor.transform(x_data)
               my_log.info("data is transformed ..")

               cloud_model_score = scoring_value(cloud_model,x_test=x_data,y_test=y_data)
               my_log.info(f"cloud model score is calculated and score is {cloud_model_score}..")

               local_model_score = scoring_value(local_model,x_test=x_data,y_test=y_data)   
               my_log.info(f"local model score is calculated and score is {local_model_score}..")

               if cloud_model_score > local_model_score:
                   return False
               else:
                   return True

            else :
                return True
        except Exception as e:
            my_log.error(f"Error in ModelEvaluation evaluate_model : {str(e)}")
            raise MyException(f"Error in ModelEvaluation evaluate_model : {str(e)}",sys)
        
    def initiate_model_eval(self):
        try:

            data = pd.read_csv(self.trans_artifact.test_file)
            x_data = data.iloc[:,:-1]
            y_data = data.iloc[:,-1]
            my_log.info("data is loaded ..")

            model = self.load_cloud_model()
            my_log.info("cloud model is loaded successfully ..")

            report = self.evaluate_model(model,x_data,y_data)
            my_log.info(f"model evaluation is completed and report is {report}..")
            
        except Exception as e:
            my_log.error(f"Error in ModelEvaluation initiate_model_eval : {str(e)}")
            raise MyException(f"Error in ModelEvaluation initiate_model_eval : {str(e)}",sys)