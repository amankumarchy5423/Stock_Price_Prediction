from src.loggers.logger import my_log
from src.Exception.Project_Exception import MyException
from src.Pipeline.train_pipeline import TrainPipeline



import sys


# import os
# os.environ["DAGSHUB_TOKEN"] = os.getenv("DAGSHUB_TOKEN")

# import os
# from dagshub.auth import login

# Read token from environment and login
# login(token=os.getenv("DAGSHUB_TOKEN"))


# class Main:
#     def __init__(self):
#         try:
#             my_log.info(" <<< Main  Started >>>")

#             obj = TrainPipeline()
#             obj.initiate_pipeline()
#             my_log.info(" <<< Main  Ended >>>")
            
#         except Exception as e :
#             my_log.error(e)
#             raise MyException(e , sys)
obj = TrainPipeline()
obj.initiate_pipeline()