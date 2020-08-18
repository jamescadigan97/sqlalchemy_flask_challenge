#Import Dependencies
import numpy as np
import os
import sqlite3
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from flask import Flask, jsonify
import os

#Create Base
os.chdir(os.path.dirname(os.path.abspath(__file__)))
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
Base = automap_base()

#Reflect
Base.prepare(engine, reflect = True)

#Find keys
Keys = Base.classes.keys()

# Save references to each table
Measurements = Base.classes.measurement
Stations = Base.classes.station
session = Session(engine)

inspector = inspect(engine)
table_names= inspector.get_table_names()


#Create Flask App
app = Flask(__name__)

#Homepage
@app.route("/")
def home():
    return (
        f"Welcome weather app<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
    )

#Precipation Data
@app.route("/api/v1.0/precipitation")
def precipitation():
    precip_data = session.query(Measurements.date, Measurements.prcp).order_by(Measurements.date.desc()).all()
    return jsonify(precip_data)

#Station List
@app.route("/api/v1.0/station")
def station():
    station_list= session.query(Measurements.station).group_by(Measurements.station).order_by(func.count(Measurements.station).desc()).all()
    return jsonify(station_list)

#One year of temperature data
@app.route("/api/v1.0/tobs")
def tobs():
    station_list= session.query(Measurements.station).group_by(Measurements.station).order_by(func.count(Measurements.station).desc()).all()
    most_active = station_list[0][0]
    tobs_data = session.query(Measurements.tobs).filter(Measurements.station == 'USC00519281').filter(Measurements.date>="2016-08-23)").all()
    return jsonify(tobs_data)

#Maximum, minimum and average temperature
@app.route("/api/v1.0/start")
def start():
    max_temp = session.query(func.max(Measurements.tobs)).filter(Measurements.date>="2016-08-23)").all()
    min_temp = session.query(func.min(Measurements.tobs)).filter(Measurements.date>="2016-08-23)").all()
    ave_temp = session.query(func.avg(Measurements.tobs)).filter(Measurements.date>="2016-08-23)").all()
    return (
        f"The maximum temperature recorded was {max_temp[0][0]} degrees. <br/>"
        f"The maximum temperature recorded was {min_temp[0][0]} degrees. <br/>"
        f"The maximum temperature recorded was {round(ave_temp[0][0],2)} degrees. <br/>"
    )

if __name__ == "__main__":
    app.run(debug=True)
