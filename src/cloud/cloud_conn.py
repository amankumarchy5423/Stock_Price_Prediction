import boto3.resources
from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
import boto3
import os,sys

from dotenv import load_dotenv
load_dotenv()

access_key = os.getenv('ACCESS_kEY_ID')
secret_key = os.getenv('SECRET_ACCESS_KEY')


class AwsConn:
    s3_client = None
    s3_resources = None
    def __init__(self, region_name, access_key = access_key, secret_key = secret_key):
        try:
            if AwsConn.s3_client is None and AwsConn.s3_resources is None:
                self.access_key = access_key
                self.secret_key = secret_key
                self.region_name = region_name

                if self.access_key is None or self.secret_key is None:
                    my_log.error("Access Key or Secret Key is None")
                    raise MyException("Access Key or Secret Key is None",sys)
                
                AwsConn.s3_client = boto3.client('s3',
                                                 aws_access_key_id = self.access_key,
                                                 aws_secret_access_key = self.secret_key,
                                                 region_name = self.region_name)
                my_log.info("s3 client setup completed ...")

                AwsConn.s3_resources = boto3.resources('s3',
                                                 aws_access_key_id = self.access_key,
                                                 aws_secret_access_key = self.secret_key,
                                                 region_name = self.region_name)
                my_log.info("s3 resources setup completed ...")

                self.client = AwsConn.s3_client
                self.resources = AwsConn.s3_resources

        except Exception as e:
            my_log.error("Error in AwsConn class __init__ method : " + str(e))
            raise MyException("Error in AwsConn class __init__ method : " + str(e),sys)
