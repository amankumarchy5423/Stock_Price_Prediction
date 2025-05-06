from src.component.data_ingestion import DataIngestion
from src.loggers.logger import my_log
from src.Exception.Project_Exception import MyException
from src.config.project_config import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainConfig,ModelEvaluationConfig
from src.Artifact.project_artifact import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluatorArtifact
from src.component.data_validation import DataValidation
from src.component.data_transformation import DataTransformation
from src.component.model_train import ModelTrain
from src.component.model_evaluation import ModelEvaluation
from src.component.model_push import ModelPush

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
            output = dataingestionobj.initiate_dataingestion()
            my_log.info("DataIngestion successfully completed ..." )

            my_log.info("<<< DataIngestion ended >>>")
            return output
        except Exception as e :
            my_log.error (e)
            raise MyException(e,sys)
        
    def data_validation_pipe(self,artifact : DataIngestionArtifact):
        try:
            my_log.info("<<< Data Validation Started >>>")
            config_obj = DataValidationConfig()

            validation_obj = DataValidation(artifact=artifact,config=config_obj)
            my_log.info(" data validation obj created ...")

            output = validation_obj.initiate_datavalidation()

            my_log.info("<<< Data Validation Ended >>>")
            return output
        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
        
    def data_transformation_pipe(self,artifact : DataValidationArtifact):
        try:
            my_log.info("<<< Data Transformation Started >>>")

            config_obj = DataTransformationConfig()

            transformation_obj = DataTransformation(config_obj,artifact)

            output = transformation_obj.initiate_transformation()
            my_log.info("<<< Data Transformation Ended >>>")
            return output
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
    def model_training_pipe(self,artifact : DataTransformationArtifact):
        try:
            my_log.info("<<< Model Training Started >>>")

            config_obj = ModelTrainConfig()
            model_train_obj = ModelTrain(config_obj,artifact)
            output = model_train_obj.initiate_modeltrain()

            my_log.info("<<< Model Training Ended >>>")
            return output
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
    
    def model_evaluation_pipe(self,artifact1 : ModelTrainerArtifact,artifact2 : DataTransformationArtifact):
        try:
            my_log.info("<<< Model Evaluation Started >>>")

            config_obj = ModelEvaluationConfig()
            eval_obj = ModelEvaluation(config=config_obj,
                                       artifact=artifact1,
                                       transformation_artifact=artifact2)
            output=eval_obj.initiate_model_eval()

            my_log.info("<<< Model Evaluation Ended >>>")
            return output
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
    def model_pusher_pipe(self,artifact : ModelEvaluatorArtifact,artifact2 : ModelTrainerArtifact):
        try:    
            my_log.info("<<< Model Pusher Started >>>")

            pusher_obj = ModelPush(model_eval_artifact=artifact,
                                   model_train_artifact=artifact2)
            pusher_obj.initiate_modelpush()

            my_log.info("<<< Model Pusher Ended >>>")
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
    def initiate_pipeline(self) -> None:
        try:
            my_log.info(" <<< train pipeline started >>>")
            
            data_ingestion_out = self.data_ingestion()
            my_log.info("data ingestion pipeline completed successfully ...")

            data_validation_out = self.data_validation_pipe(artifact=data_ingestion_out)
            my_log.info("data validation pipeline completed successfully ...")

            data_transformation_out = self.data_transformation_pipe(data_validation_out)
            my_log.info("data validation pipeline Completed successfully ...")

            model_train_out = self.model_training_pipe(data_transformation_out)
            my_log.info("model training pipeline completed successfully ...")

            eval_out=self.model_evaluation_pipe(artifact1=model_train_out,artifact2=data_transformation_out)
            my_log.info("model evaluation pipeline completed successfully ...")

            self.model_pusher_pipe(artifact2=model_train_out, artifact=eval_out)
            my_log.info(" <<< train pipeline ended >>>")
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)