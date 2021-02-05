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
        f"/api/v1.0/<start>/<end>"
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
    recentDate = (session.query(Measurement.date)
                .order_by(Measurement.date.desc())
                .first())
    
    recentDate = list(np.ravel(recentDate))[0]
    recentDate = dt.datetime.strptime(recentDate, '%Y-%m-%d')
    yearbeforeDate = recentDate - dt.timedelta(days=366)

    results = (session.query(Measurement.date, Measurement.tobs)
                .filter(Measurement.date >= yearbeforeDate)
                .all())
    
    session.close()

    # Create a dictionary from the row data and append to a list of all tobs data
    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temperature Observation Data"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def starting_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query tobs data (query process as .ipynb)
    starting_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    tobs_data = [Measurement.date,
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)]
    
    results = (session.query(*tobs_data)
            .filter(func.strftime('%Y-%m-%d', Measurement.date) >= starting_date)
            .all())
    
    # Create a dictionary from the row data and append to a list of all tobs data for a given start date.
    start_dates = []
    for result in results:
        start_dict = {}
        start_dict["Date"] = result[0]
        start_dict["Low Temperature"] = result[1]
        start_dict["High Temperature"] = result[2]
        start_dict["Avg. Temperature"] = result[3]
        start_dates.append(start_dict)

    return jsonify(start_dates)

@app.route("/api/v1.0/<start>")
def starting_ending_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query tobs data (query process as .ipynb)
    starting_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    ending_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
    
    tobs_data = [Measurement.date,
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)]
    
    results = (session.query(*tobs_data)
            .filter(Measurement.date >= starting_date)
            .filter(Measurement.date <= ending_date)
            .all())
    
    # Use np.ravel to try to solve error instead of a for loop.
    # Store the min, max, avg in a variable so it can be placed into the dict.
    results = list(np.ravel(results))
    min_tobs = results[1]
    max_tobs = results[2]
    avg_tobs = results[3]

    # Create a dictionary from the row data and append to a list of all tobs data for a given start and end date.
    start_end_dates = []
    s_e_dict = [{"Starting Date": starting_date},
                {"Ending Date": ending_date},
                {"Low Temperature": min_tobs},
                {"High Temperature": max_tobs},
                {"Avg. Temperature": avg_tobs}]
    
    start_end_dates.append(s_e_dict)
    
    return jsonify(start_end_dates)

if __name__ == '__main__':
    app.run(debug=True)

