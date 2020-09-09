#app = Flask(__name__)
#@app.route('/')
#def hello_world():
#    return 'Hello world' 
# Importing dependencies for datetime, numpy and pandas
import datetime as dt
import numpy as np
import pandas as pd
# Importing dependencies for SQlAlchemy 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# Importing dependenciey for Flask
from flask import Flask, jsonify
# Accessing  the SQlite Database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base() 
Base.prepare(engine, reflect=True)
# Creating variable for each of the classes
Measurement = Base.classes.measurement
Station = Base.classes.station
# Creating session link from python to our Database
session = Session(engine)
# Creting a Flask application called app
app = Flask(__name__)
# Define the welcome route
@app.route("/")
# create a function with return statment(precipitation, stations,tobs) 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
## Creating the precipitation route:
@app.route("/api/v1.0/precipitation")
# Creating the precipitation function 
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365) 
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # Creating a dictionry with date as key and precipitation as value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

## Creating the stations route:
@app.route("/api/v1.0/stations")
# Creating the stations function 
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

## Creating the monthly route
@app.route("/api/v1.0/tobs")
# Creating the tobs function 
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

## Creating the summary statistics route
@app.route("/api/v1.0/temps/<start>")
@app.route("/api/v1.0/temps/<start>/<end>")
# Creating statistics function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
   
    if not end:
        results = session.query(*sel).\
        filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
    



    


