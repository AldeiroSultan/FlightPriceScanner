from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import ssl
import certifi
from OpenSSL import SSL


app = Flask(__name__)
model = pickle.load(open("c1_flight_rf.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure
        dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        # Duration
        Duration_hour = abs(arrival_hour - dep_hour)
        Duration_mins = abs(arrival_min - dep_min)
        # print("Duration : ", dur_hour, dur_min)

        # Total Stops
        Total_Stops = int(request.form["stops"])
        # print(Total_stops)



       airline = request.form['airline']
        if(airline == 'Garuda Indonesia'):
            Airline_AirAsia = 0
            Airline_GoAir = 0
            Airline_Citilink = 0
            Airline_GarudaIndonesia = 1
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_BatikAir = 0
            Airline_Other = 0

        elif (airline == 'Citilink'):
            Airline_AirAsia = 0
            Airline_GoAir = 0
            Airline_Citilink = 1
            Airline_GarudaIndonesia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_BatikAir = 0
            Airline_Other = 0

        elif (airline == 'AirAsia'):
            Airline_AirAsia = 1
            Airline_GoAir = 0
            Airline_Citilink = 0
            Airline_GarudaIndonesia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_BatikAir = 0
            Airline_Other = 0
            
        elif (airline == 'Multiple carriers'):
            Airline_AirAsia = 0
            Airline_GoAir = 0
            Airline_Citilink = 0
            Airline_GarudaIndonesia = 0
            Airline_MultipleCarriers = 1
            Airline_SpiceJet = 0
            Airline_BatikAir = 0
            Airline_Other = 0
            
        elif (airline == 'SpiceJet'):
            Airline_AirAsia = 0
            Airline_GoAir = 0
            Airline_Citilink = 0
            Airline_GarudaIndonesia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 1
            Airline_BatikAir = 0
            Airline_Other = 0
            
        elif (airline == 'Batik Air'):
            Airline_AirAsia = 0
            Airline_GoAir = 0
            Airline_Citilink = 0
            Airline_GarudaIndonesia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_BatikAir = 1
            Airline_Other = 0

        elif (airline == 'GoAir'):
            Airline_AirAsia = 0
            Airline_GoAir = 1
            Airline_Citilink = 0
            Airline_GarudaIndonesia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_BatikAir = 0
            Airline_Other = 0

        else:
            Airline_AirAsia = 0
            Airline_GoAir = 0
            Airline_Citilink = 0
            Airline_GarudaIndonesia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_BatikAir = 0
            Airline_Other = 1


        Source = request.form["Source"]
        if (Source == 'Jakarta'):
            Source_Jakarta = 1
            Source_Surabaya = 0
            Source_Bandung = 0
            Source_Semarang = 0

        elif (Source == 'Surabaya'):
            Source_Jakarta = 0
            Source_Surabaya = 1
            Source_Bandung = 0
            Source_Semarang = 0

        elif (Source == 'Bandung'):
            Source_Jakarta = 0
            Source_Surabaya = 0
            Source_Bandung = 1
            Source_Semarang = 0

        elif (Source == 'Semarang'):
            Source_Jakarta = 0
            Source_Surabaya = 0
            Source_Bandung = 0
            Source_Semarang = 1

        else:
            Source_Jakarta = 0
            Source_Surabaya = 0
            Source_Bandung = 0
            Source_Semarang = 0



        Destination = request.form["Destination"]
        if (Destination == 'Medan'):
            Destination_Medan = 1
            Destination_Jakarta = 0
            Destination_Makassar = 0
            Destination_Surabaya = 0

        elif (Destination == 'Jakarta'):
            Destination_Medan = 0
            Destination_Jakarta = 1
            Destination_Makassar = 0
            Destination_Surabaya = 0

        elif (Destination == 'Makassar'):
            Destination_Medan = 0
            Destination_Jakarta = 0
            Destination_Makassar = 1
            Destination_Surabaya = 0

        elif (Destination == 'Surabaya'):
            Destination_Medan = 0
            Destination_Jakarta = 0
            Destination_Makassar = 0
            Destination_Surabaya = 1

        else:
            Destination_Medan = 0
            Destination_Jakarta = 0
            Destination_Makassar = 0
            Destination_Surabaya = 0


        prediction = model.predict([[
            Total_Stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arrival_hour,
            arrival_min,
            Duration_hour,
            Duration_mins,
            Airline_AirAsia,
            Airline_GoAir,
            Airline_Citilink,
            Airline_GarudaIndonesia,
            Airline_MultipleCarriers,
            Airline_Other,
            Airline_SpiceJet,
            Airline_BatikAir,
            Source_Semarang,
            Source_Surabaya,
            Source_Bandung,
            Destination_Medan,
            Destination_Jakarta,
            Destination_Makassar,
            Destination_Surabaya,
        ]])


        output=round(prediction[0],2)

        return render_template('home.html',prediction_text="Your Flight price is Rs. {}".format(output))


    return render_template("home.html")




if __name__ == "__main__":
    app.run(debug=True)
