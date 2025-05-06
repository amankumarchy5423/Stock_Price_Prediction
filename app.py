from src.Exception.Project_Exception import MyException
from src.loggers.logger import my_log
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
        return render_template('predict.html')
    except Exception as e:
        my_log.error(f"An error occurred: {e}")
        



if __name__ == '__main__':
    app.run(debug=True)