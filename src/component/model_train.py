from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
from src.config.project_config import ModelTrainConfig
from src.Artifact.project_artifact import DataTransformationArtifact,ModelTrainerArtifact
from src.utility.project_utils import save_file,open_file,scoring_value

from sklearn.linear_model import LogisticRegression,ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error



import os,sys
import pandas as pd
import mlflow
from dotenv import load_dotenv
load_dotenv()

# import dagshub
# dagshub.init(repo_owner='amankumarchy5423', repo_name='Stock_Price_Prediction', mlflow=True)


mlflow.set_tracking_uri(uri=os.getenv('DAGSHUB_URL'))

os.environ["MLFLOW_TRACKING_USERNAME"] = "amankumarchy5423" 
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("DAGSHUB_TOKEN")  
# mlflow.set_experiment(experiment_id=os.getenv('DAGSHUB_EXPERIMENT_ID'))








class ModelTrain:
    def __init__(self,config : ModelTrainConfig,artifact : DataTransformationArtifact):
        try:
            self.config = config
            self.artifact = artifact
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
    def model_and_param(self) -> dict:
        try:
            models : dict = {
                'LR':LogisticRegression(),
                'EN':ElasticNet(),
                'DT':DecisionTreeRegressor(),
                'RF':RandomForestRegressor(),
                'GB':GradientBoostingRegressor(),
                'SVR':SVR()

            }
            my_log.info("dict of models created")

            params : dict = open_file(file_path=self.config.prams_file)
            my_log.info("params file opened")

            return models,params
        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
        
    
    def fine_tuning(self, x_train: pd.DataFrame, y_train: pd.DataFrame,
                x_test: pd.DataFrame, y_test: pd.DataFrame) -> any:
        try:
            models : dict = {
                'EN':ElasticNet(),
                'DT':DecisionTreeRegressor(),
                'RF':RandomForestRegressor(),
                'GB':GradientBoostingRegressor(),
                'SVR':SVR()

            }
            my_log.info("dict of models created")

            params : dict = open_file(file_path=self.config.prams_file)
            my_log.info("params file opened")

            best_score = self.config.model_thresold
            best_model = None
            best_model_name = None
    
            while mlflow.active_run():
                mlflow.end_run()
    
            for model_name, model in models.items():
                param = params.get(model_name, {})
    
                with mlflow.start_run(run_name=f"{model_name}_parent_run") as parent_run:
                    print(f"Started parent run: {parent_run.info.run_id}")
                    cv_model = GridSearchCV(model, param_grid=param, cv=10, verbose=1)
                    cv_model.fit(x_train, y_train)
    
                    for j, param_set in enumerate(cv_model.cv_results_['params']):
                        with mlflow.start_run(run_name=f"{model_name}_child_run_{j}", nested=True) as child_run:
                            print(f"Started child run: {child_run.info.run_id}")
                            for param_name, param_value in param_set.items():
                                mlflow.log_param(param_name, param_value)
    
                            score = cv_model.cv_results_['mean_test_score'][j]
                            
                            mlflow.log_metric("accuracy", score)
                            my_log.info(f"model name {model_name} gives accuracy of {score}")
    
                            if score > best_score:
                                best_score = score
                                best_model = cv_model.best_estimator_
                                best_model_name = model_name
    
            save_file(file_path=self.config.model_file, Model=best_model)
    
        except Exception as e:
            my_log.error(e)
            while mlflow.active_run():
                mlflow.end_run()
            raise MyException(e, sys)

        
    def initiate_modeltrain(self) ->ModelTrainerArtifact:
        try:
            
            train_data = open_file(self.artifact.train_file)
            test_data = open_file(self.artifact.test_file)
            x_train,x_test,y_train,y_test = train_test_split(train_data.iloc[:,:-1],train_data.iloc[:,-1],random_state=42)
            my_log.info("train and test data are loade .....")

            # models,params = self.model_and_param()
            my_log.info("models and params are loaded .....")

            self.fine_tuning(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test)

            return ModelTrainerArtifact(model_file=self.config.model_file,
                                        preprocessor_file=self.artifact.preprocessor_path)
        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
        
    
    
