import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save reference to the table
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
        f"/api/v1.0/enter requested start date in yyyy-mm-dd<br/>"
        f"/api/v1.0/enter requested start date in yyyy-mm-dd/enter requested end date in yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
#     # Create our session (link) from Python to the DB
    session = Session(engine)

#     """Return a list of all precipitation info"""
#     # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

#     # Convert list of tuples into normal list
    #all_precipitations = list(np.ravel(results))
    
    precip_score = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precipitation"] = prcp
        precip_score.append(precip_dict)

    return jsonify(precip_score)

##get JSON list of stations 
@app.route("/api/v1.0/stations")
def stations():
#     # Create our session (link) from Python to the DB
    session = Session(engine)
#     """Return a list of all stations"""
#     # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

#     # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)
#   

#### query date and temp obverstaions of most active station for the last year of data- return a JASON list of temp obvs (TOBS) for previous year
@app.route("/api/v1.0/tobs")


def tobs():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
# #     # Create our session (link) from Python to the DB
    session = Session(engine)
# #     # Query all stations and precips
 

    results= session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >=year_ago).filter(Measurement.station =="USC00519281").all()

    session.close()


# Create a dictionary from the row data and append to a list of precip_scores
    tobs_score = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_score.append(tobs_dict)



    return jsonify(tobs_score)
# #   
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#start only
@app.route("/api/v1.0/<start>")
def search_date (start):
    session = Session(engine)
# #     # Query all stations and precips
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()  

    session.close()

    start_date_data = []
    for min, avg, max in results:
        start_date_data_dict = {}
        start_date_data_dict["min_temp"] = min
        start_date_data_dict["avg_temp"] = avg
        start_date_data_dict["max_temp"] = max
        start_date_data.append(start_date_data_dict) 

    return jsonify(start_date_data)

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
#with end date
@app.route("/api/v1.0/<start>/<end>")
def two_dates (start,end):
    session = Session(engine)
# #     # Query all stations and precips
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()  

    session.close()

    start__end_date_data = []
    for min, avg, max in results:
        start__end_date_dict = {}
        start__end_date_dict["min_temp"] = min
        start__end_date_dict["avg_temp"] = avg
        start__end_date_dict["max_temp"] = max
        start__end_date_data.append(start__end_date_dict) 
    return jsonify(start__end_date_data)


if __name__ == '__main__':
    app.run(debug=True)
