from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
from src.config.project_config import ModelEvaluationConfig

import os,sys
import numpy as np
import pandas as pd
import boto3
import mlflow


class ModelEvaluation:
    def __init__(self ,config : ModelEvaluationConfig):
        try:
            self.config = config
        except Exception as e:
            my_log.error(f"Error in ModelEvaluation __init__ : {str(e)}")
            raise MyException(f"Error in ModelEvaluation __init__ : {str(e)}",sys)