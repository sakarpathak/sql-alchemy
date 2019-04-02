import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


app = Flask(__name__)



@app.route("/")
def home():
    return (
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation/<br/>"
        f"/api/v1.0/stations/<br/>"
        f"/api/v1.0/tobs/")


@app.route('/api/v1.0/precipitation/')
def precipitation():
    prcp_results = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= '2017-01-01').all()
    prcp_dict = dict(prcp_results)
    print()
    print("Precipitation Results")
    return jsonify(prcp_dict)

@app.route('/api/v1.0/stations/')
def stations():
    station_list = session.query(Station.station)\
    .order_by(Station.station).all() 
    print()
    print("Station List:")   
    for row in station_list:
        print (row[0])
    return jsonify(station_list)

@app.route('/api/v1.0/tobs/')
def tobs():
    temp_data=session.query(Measurement.date, Measurement.tobs)\
                    .filter(Measurement.date>="2016-08-23")\
                    .order_by(Measurement.date).all()
    temp_dict=dict(temp_data)
    print()
    print("Temperature Results for All Stations")
    return jsonify(temp_dict)



if __name__ == "__main__":
    app.run(debug=True)