from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
from src.Pipeline.predict_pipeline import PredictPipe

import pandas as pd
from flask import Flask
from flask import request,render_template


app = Flask('__name__')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/predict',methods=['GET','POST'])
def predict():
    try:
        if request.method == 'POST':
            my_log.info('Received POST request')
            data = request.form
            my_log.info(data)

            data_df = pd.DataFrame(data, index=[0])
            my_log.info(data_df)

            obj = PredictPipe(data=data_df)
            predict_out = obj.load_cloud_model()
            my_log.info(predict_out)

            return render_template('result.html',predict_out=predict_out)

        return render_template('predict.html')
    except Exception as e:
        my_log.error(f"An error occurred: {e}")
        



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)