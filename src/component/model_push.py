import mlflow.sklearn
from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
from src.Artifact.project_artifact import ModelEvaluatorArtifact,ModelTrainerArtifact
from src.cloud.cloud_conn import AwsConn

import os,sys
import joblib
import mlflow
import boto3
from dotenv import load_dotenv
load_dotenv()


client = mlflow.MlflowClient()

aws_id = os.getenv('ACCESS_kEY_ID')
aws_secret = os.getenv('SECRET_ACCESS_KEY')
aws_region = os.getenv('REGION_NAME')
my_log.info(f"aws id {aws_id},secret key is {aws_secret},region is {aws_region}")

class ModelPush:
    def __init__(self,model_train_artifact : ModelTrainerArtifact, model_eval_artifact : ModelEvaluatorArtifact):
        try:
            self.train_artifact = model_train_artifact
            self.eval_artifact = model_eval_artifact
        except Exception as e:
            my_log.error(f"Error in ModelPush class: {str(e)}")
            raise MyException(f"Error in ModelPush class: {str(e)}")
        
    def push_model_mlflow(self,model,preprocessor):
        try:
            
            
            mlflow.sklearn.log_model(model,"model",registered_model_name="ml_model")
            mlflow.sklearn.log_model(preprocessor,"preprocessor",registered_model_name="pre_model")
            my_log.info("all models are registerd in mlflow registery ")

            if self.eval_artifact.report:
                client.transition_model_version_stage(
                    name="ml_model", 
                    version=client.get_latest_versions(name="ml_model")[0].version,
                    stage="Production",
                    archive_existing_versions=True
                )
                my_log.info("model is pushed to mlflow registry")
                client.transition_model_version_stage(
                    name="pre_model",
                    version=client.get_latest_versions(name="pre_model")[0].version,
                    stage="Production",
                    archive_existing_versions=True
                )
                my_log.info("preprocessor is pushed to mlflow registry")

        except Exception as e:
            my_log.error(f"Error in push_model_mlflow method: {str(e)}")
            raise MyException(f"Error in push_model_mlflow method: {str(e)}",sys)
        
    def push_model_s3(self,model,preprocessor) :
        try:
            if self.eval_artifact.report:
                # s3 = AwsConn()
                s3= boto3.client('s3',
                              aws_access_key_id = aws_id,
                              aws_secret_access_key = aws_secret,
                              region_name = aws_region)


                s3.upload_file(
                    Filename=self.train_artifact.preprocessor_file,
                    Bucket=self.eval_artifact.bucket_name,
                    Key=self.eval_artifact.ml_model_key
                )
                my_log.info("ml_model is uploaded to s3 bucket")

                s3.upload_file(
                    Filename="my_model/model.joblib",
                    Bucket='stock-price-bucket-aman',
                    Key="models/ml_model/model.joblib"
                )
                my_log.info("preprocessor is uploaded to s3 bucket")
                
            

        except Exception as e:
            my_log.error(f"Error in push_model_s3 method: {str(e)}")
            raise MyException(f"Error in push_model_s3 method: {str(e)}",sys)
        
    def initiate_modelpush(self):
        try:
            model = joblib.load(self.train_artifact.model_file)
            preprocessor = joblib.load(self.train_artifact.preprocessor_file)
            my_log.info("models loaded for pushing on cloud ...")

            self.push_model_mlflow(model=model,preprocessor=preprocessor)
            my_log.info("model pushed to mlflow registry ...")

            self.push_model_s3(model=model,preprocessor=preprocessor)
            my_log.info("model pushed to s3 bucket ...")
            
        except Exception as e:
            my_log.error(f"Error in initiate_modelpush method: {str(e)}")
            raise MyException(f"Error in initiate_modelpush method: {str(e)}",sys)
        

if __name__ == "__main__":
    modelpush = ModelPush()
    modelpush.push_model_mlflow()