import os
import sys



class MyException(Exception):
    def __init__(self,message,error_details:sys):
        try:
            self.message = message
            _,_,error_tb = error_details.exc_info()
            self.line_no = error_tb.tb_lineno
            self.file_name = error_tb.tb_frame.f_code.co_filename
        except Exception as e :
            raise e
        

    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.line_no, str(self.message))