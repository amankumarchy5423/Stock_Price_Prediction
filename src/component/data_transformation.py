from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
from src.config.project_config import DataTransformationConfig
from src.Artifact.project_artifact import DataValidationArtifact,DataTransformationArtifact
from src.utility.project_utils import open_file,save_file

import os,sys
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline,Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder,LabelEncoder
from sklearn.impute import KNNImputer,SimpleImputer
from sklearn.model_selection import train_test_split





class DataTransformation:
    def __init__(self,config : DataTransformationConfig,artifact : DataValidationArtifact):
        try:
            self.config = config
            self.artifact = artifact

        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
    def load_info(self) -> list:
        try:
            file_path = self.config.yaml_path

            data : dict = open_file(file_path)
            my_log.info("yaml data successfully loaded ...")

            num_colum : list= data['numerical_col']
            cat_colum : list= data['categorical_col']
            output_clm : list = data['output_col']
            my_log.info(f"num_col is : {num_colum} \n cat_column is : {cat_colum}")

            return num_colum,cat_colum,output_clm
            
        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
    def build_preprocessor(self, train_data: pd.DataFrame, test_data: pd.DataFrame,
                       num_clm: list, cat_clm: list, out_clm: list) -> any:
        try:
            num_column = Pipeline([
                ('imputer', SimpleImputer(strategy='mean')),
                ('norm', StandardScaler())
            ])
            cat_column = Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('ohe', OneHotEncoder(sparse_output=False))
            ])
    
            preprocessor = ColumnTransformer(transformers=[
                ('num', num_column, num_clm),
                ('categorical', cat_column, cat_clm)
            ], remainder='passthrough')
    
            my_log.info("Data preprocessor is ready.")
    
            X_train = train_data.drop(columns=out_clm)
            X_test = test_data.drop(columns=out_clm)
            my_log.info("output column drop from all dataframes")
    
            preprocessor.fit(X_train)
    
            train_data_pre = preprocessor.transform(X_train)
            test_data_pre = preprocessor.transform(X_test)
    
            my_log.info("Data transformed by preprocessor.")
    
            transformed_train = pd.DataFrame(train_data_pre,index=False)
            transformed_test = pd.DataFrame(test_data_pre,index=False)
    
            # Add back the target column
            # for col in out_clm:
            transformed_train[out_clm] = train_data[out_clm].values
            transformed_test[out_clm] = test_data[out_clm].values
    
            my_log.info("Output column(s) added back to transformed data.")
    
            return preprocessor, transformed_train, transformed_test

        except Exception as e:
            my_log.error(e)
            raise MyException(e, sys)

    
    def save_local(self,train_data: pd.DataFrame,test_data: pd.DataFrame,model : object) -> None:
        try:
            my_log.info("all data are saving starts ...")

            os.makedirs(os.path.dirname(self.config.model_file),exist_ok=True)
            save_file(file_path=self.config.model_file,Model=model)
            my_log.info("preprocessor model are saved ")

            os.makedirs(self.config.data_transformation_dir,exist_ok=True)
            save_file(file_path=self.config.transformed_train,data=train_data)
            save_file(file_path=self.config.transformed_test,data=test_data)
            my_log.info("all data and model are saved locally")

        except Exception as e :
            my_log.error(e)
            raise MyException(e,sys)
        
    def initiate_transformation(self):
        try:
            my_log.info("____ data transformation started ____")

            data = pd.read_csv(self.artifact.data_dir)

            num_colum,cat_colum,output_clm = self.load_info()
            my_log.info("load info function completed ...")

            
            train,test = train_test_split(data.iloc[:,2:],train_size=0.8)
            my_log.info(f"columns are {train.columns}")
            preprocessor,train_df,test_df = self.build_preprocessor(train_data=train,test_data=test,
                                                                    num_clm=num_colum,cat_clm=cat_colum,out_clm=output_clm)
            
            self.save_local(train_df,test_df,preprocessor)

            my_log.info("____ data transformation ended ____")

            return DataTransformationArtifact(self.config.transformed_train,self.config.transformed_test,
                                              self.config.model_file)
        except Exception as e:
            my_log.error(e)
            raise MyException(e,sys)
        
        