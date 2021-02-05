## Import Dependencies
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import os
import sys

print(os.path.dirname(__file__))

root_project_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, root_project_path)

hawaii_path = os.path.join(root_project_path, "Resources/hawaii.sqlite")

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///"+hawaii_path)

# Reflect the DB

Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/tobs<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query prcp data
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all precip data
    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query station data
    results = session.query(Station.station, Station.name).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all station data
    station_data = []
    for station, name in results:
        station_dict = {}
        station_dict["Station ID #"] = station
        station_dict["Station Name:"] = name
        station_data.append(station_dict)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query tobs data (query process as .ipynb)
    #recentDate_query = (session.query(Measurement.date)
                #.order_by(Measurement.date.desc())
                #.first())
    #recentDate = dt.date(2017, 8, 23)

    #yearbeforeDate = recentDate - dt.timedelta(days=365)
    
    
    
    
    session.close()

    # Create a dictionary from the row data and append to a list of all station data
    station_data = []
    for station, name in results:
        station_dict = {}
        station_dict["Station ID #"] = station
        station_dict["Station Name:"] = name
        station_data.append(station_dict)

    return jsonify(station_data)



if __name__ == '__main__':
    app.run(debug=True)

