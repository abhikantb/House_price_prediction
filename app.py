import pickle
from flask import Flask,request,app,jsonify,url_for,render_template,json
import numpy as np
import pandas as pd
import config

#created basic flask app and name is starting point of app where it will run
app=Flask(__name__,template_folder='templates')

#load the pickle model
house_pred_model=pickle.load(open(config.model_path,'rb'))
                

#homepage or localhost url including slash / 
# when you click on url after deployment the first page appears will be home page
#go to main directory or upper hirarchy of website/localhost address
@app.route('/')
def home():
    return render_template('House_Price_Prediction_home.html')

#first method: getting result through front end application
@app.route('/predict',methods=['POST'])
def predict_api():
    house_age = float(request.form.get('house_age'))
    distance = float(request.form.get('distance'))
    stores = int(request.form.get('stores'))
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))

    print(house_age,distance,stores,latitude,longitude)
    input_data=pd.DataFrame(data=[[house_age,distance,stores,latitude,longitude]],
    columns=['X2 house age','X3 distance to the nearest MRT station','X4 number of convenience stores','X5 latitude','X6 longitude'])
    print(input_data)
    price =  house_pred_model.predict(input_data)
    return render_template('House_Price_Prediction_home.html',price_result='Unit area Price is {}'.format(float(price)))


#second method: getting result through json postman app
# @app.route('/predict',methods=['POST'])
# def predict_api():
#     #get json data from postman app(where json data is stored) with data as a key
#     json_data=request.json['data']
#     print(json_data)
#     #json_data is in form of dictionary

#     #take only values from json_data----> make a list ---> and put [] outside for making it array 
#     # and pass it to dataframe
#     input_data=pd.DataFrame(data=[list(json_data.values())],columns=['X2 house age','X3 distance to the nearest MRT station','X4 number of convenience stores','X5 latitude','X6 longitude'])
#     print(input_data)

#     #model prediction
#     price =  house_pred_model.predict(input_data)
#     print(price)
#     return jsonify(price[0])   
#     #here if we put only price then it will be 1d Array jsonify wants 2d array hence we give[0] index

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, host=config.host_name,port=config.port_number)
