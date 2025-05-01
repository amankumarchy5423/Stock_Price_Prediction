from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
import os,sys
import pandas as pd
import numpy as np
import yaml
import joblib



def open_file(file_path : str ) -> any :
    try:
        file_lis = file_path.split('.')[-1].lower()
        if file_lis =='csv'  :
            try :
                return pd.read_csv(file_path)
            except Exception as e :
                my_log.error(e)
        
        if file_lis == 'yaml'  or file_lis == 'yml' :
            try :
                return yaml.safe_load(file_path)
            except Exception as e :
                my_log.error(e)

        if file_lis == 'joblib' or file_lis == 'pkl' :
            try:
                return joblib.load(file_path)
            except Exception as e :
                my_log.error(e)
        
        else:
            msg = f"Unsupported file type: {file_lis}"
            my_log.error(msg)

    except Exception as e :
        my_log.error(e)
        raise MyException(e,sys)
    



def open_file(file_path: str) -> any:
    try:
        file_ext = file_path.split('.')[-1].lower()
        
        if file_ext == 'csv':
            try:
                return pd.read_csv(file_path)
            except Exception as e:
                my_log.error(f"CSV Read Error: {e}")
                raise MyException(e, sys)
        
        elif file_ext in ['yaml', 'yml']:
            try:
                with open(file_path, 'r') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                my_log.error(f"YAML Load Error: {e}")
                raise MyException(e, sys)

        else:
            msg = f"Unsupported file type: {file_ext}"
            my_log.error(msg)
            raise MyException(msg, sys)

    except Exception as e:
        my_log.error(f"File open failed: {e}")
        raise MyException(e, sys)

