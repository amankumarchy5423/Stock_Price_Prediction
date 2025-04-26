import os
import sys

from src.Common import common_variable




class DataIngestionConfig:
    def __init__(self):
        try:
            self.artifact = common_variable.ARTIFACT
            self.data_ingestion_dir = os.path.join(self.artifact,common_variable.DATA_INGESTIONDIR)
            self.data_file = os.path.join(self.data_ingestion_dir,common_variable.DATA_FILE)

        except Exception as e :
            raise e

