from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
from src.cloud.cloud_conn import AwsConn

import os,sys
import pandas as pd
import numpy as np
import yaml
import joblib
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV



def save_file(file_path : str ,data = None ,Model = None) -> any :
    try:
        file_lis = file_path.split('.')[-1].lower()
        if file_lis =='csv'  :
            try :
                data.to_csv(file_path)
                return "File saved successfully ..."
            except Exception as e :
                my_log.error(e)
        
        elif file_lis == 'yaml'  or file_lis == 'yml' :
            try :
                yaml.safe_dump(data,file_path)
                return "File saved successfully ..."
            except Exception as e :
                my_log.error(e)

        elif file_lis == 'joblib' or file_lis == 'pkl' :
            try:
                joblib.dump(Model , file_path)
                return "File saved successfully ..."
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
        
        elif file_ext in ['joblib','pkl']:
            try:
                return joblib.load(file_path)
            except Exception as e:
                my_log.error(e)
                raise MyException(e,sys)

        else:
            msg = f"Unsupported file type: {file_ext}"
            my_log.error(msg)
            raise MyException(msg, sys)

    except Exception as e:
        my_log.error(f"File open failed: {e}")
        raise MyException(e, sys)


def scoring_value(model, x_test, y_test) -> float:
    try:
        scores = cross_val_score(model, x_test, y_test, scoring='r2', cv=10)
        return np.mean(scores)
    except Exception as e:
        my_log.error(e)
        raise MyException(e, sys)
    
def check_bucket(bucket_name :str) -> bool:
    try:
        AwsConn.s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' exists and is accessible.")
        return True
    except Exception as e:
        my_log.error(e)
        raise MyException(e, sys)

    

# def fine_tuning(models : dict , params : dict, x_train : pd.DataFrame, y_train : pd.DataFrame,
#                 x_test : pd.DataFrame , y_test : pd.DataFrame) -> any :
#     try:
#         best_score = 0.0
#         best_model = None
#         best_model_name = None

#         for i in range(len(models)):
#             model = list(models.values())[i]
#             model_name = list(models.keys())[i]
#             param = params.get(model_name,{})

#             with mlflow.start_run(run_name=f"{model_name}_parent_run") as parent_run:
#                 cv_model = GridSearchCV(model,param_grid=param,cv=10,verbose=1)
#                 cv_model.fit(x_train,y_train)

#                 for j in range(len(cv_model.cv_results_['params'])):
#                     with mlflow.start_run(run_name=f"{model_name}_child_run") as child_run:

#                         for param_name, param_value in cv_model.cv_results_['params'][j].items():
#                                 mlflow.log_param(param_name, param_value)
                        
#                         # y_pred = cv_model.predict(x_test)
#                         score = scoring_value(cv_model,x_test,y_test)
#                         mlflow.log_metric("accuracy" , score)

#                         if score > best_score :
#                             best_score = score
#                             best_model = cv_model.best_estimator_
#                             best_model_name = model_name

#         save_file(file_path='path',Model=best_model)


#     except Exception as e:
#         my_log.error(e)
#         raise MyException(e,sys)
    

# class create_objective:

