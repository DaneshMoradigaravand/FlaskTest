from flask import Flask
import pickle
import pandas as pd
from flask import request, jsonify, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random
import matplotlib.pyplot as plt
from flask import Response
import base64

app= Flask(__name__)
app.config["DEBUG"]=True


def predict_drug(input_sequence):
    unique_sequences_freq=[]
    unique_sequences=pd.read_csv("unique_sequences_5.csv")
    unique_sequences=unique_sequences.iloc[:,1].values

    unique_sequences_freq.append([input_sequence.count(i) for i in unique_sequences])
    pickle_file=open('finalized_model_5_PKJK.pkl','rb')
    model=pickle.load(pickle_file)
    return(model.predict(pd.DataFrame(unique_sequences_freq))[0])


@app.route('/plot')
def build_plot():

    img = io.BytesIO()

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)

@app.route("/")
def hello():
    return render_template('home.html')
    #return "Prediction Application"

@app.route("/predict/", methods=['GET', 'POST'])
def api_all():
    if request.method == "POST":
        #get form data
        input_sequence = request.form.get('input_sequence')
        cars = request.form.get('cars')
    #input_sequence=request.args['input_sequence']
    #predicted_value=predict_drug(input_sequence)
    #return(jsonify(predicted_value_output=predicted_value))
        try:
            print(cars)
            prediction = predict_drug(str(input_sequence))
            #cars=str(cars)
            print(prediction)
            
            #if request.form.get('action1') == 'VALUE1':
            print(input_sequence)
            return render_template('predict.html', prediction = prediction, cars= cars)
   
        except ValueError:
            return "Please Enter valid values"
  
        pass
    pass

if __name__ == "__main__":
    app.run(debug=True)
