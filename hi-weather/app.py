import datetime as dt
import numpy as np
import pandas as pd

from sqlalchemy import create_engine, func as F
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

from flask import Flask, jsonify


# SQL engine and session
engine = create_engine('sqlite:///hawaii.sqlite')
session = Session(engine)

# Reflect db tables
Base = automap_base()
Base.prepare(engine, reflect=True)
M, S = Base.classes

# Flask app
app = Flask(__name__)


""" App routes """


@app.route('/')
def welcome():

    ''' Home page with links to routes '''

    return '''
        <h1>Welcome to the Hawaii Climate Analysis API!</h1><br />

        <h2>Available routes:</h2>
        <h3><a href="/api/v1.0/precipitation">Precipitation</a></h3>
        <h3><a href="/api/v1.0/stations">Stations</a></h3>
        <h3><a href="/api/v1.0/tobs">Temperature Observations</a></h3>
        <h3><a href="/api/v1.0/temp/start/end">Temperature Statistics</a></h3>
    '''


@app.route('/api/v1.0/precipitation')
def precipitation():

    ''' Precipitation data from the last 12 months '''

    # Date range for the last 12 months in the data
    start, _ = get_date_range(n_days=365)

    # Query the precipitation data from the last 12 months
    prcps = session.query(M.date, M.prcp).filter(M.date >= start).all()

    # Convert query results to JSON
    prcp_json = jsonify({date: prcp for date, prcp in prcps})

    # Rollback session transaction
    session.rollback()
    return prcp_json


@app.route('/api/v1.0/stations')
def stations():

    ''' Measurement count from each station '''

    # Query the data to count number of measurements from each station
    Mcounts = count_measurements_by_station()

    # Convert query results to JSON
    station_json = jsonify({station: count for station, count in Mcounts})

    # Rollback session transaction
    session.rollback()
    return station_json


@app.route('/api/v1.0/tobs')
def tobs():
    
    ''' Most active station's temperature observations from the last 12 months '''

    # Date range for the last 12 months in the data
    start, _ = get_date_range(n_days=365)

    # Get the most active station (most measurements)
    most_active = count_measurements_by_station()[0][0]

    # Query the tobs data for this stations from the last 12 months
    temps = session.query(M.date, M.tobs)
    temps = temps.filter((M.station == most_active) & (M.date >= start)).all()

    # Convert query results to JSON
    temp_json = jsonify({date: temp for date, temp in temps})

    # Rollback session transaction
    session.rollback()
    return temp_json


@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def temp_stats(start='start', end='end'):

    ''' Minimum, average, and maximum temperature over the date range from the start date to the end date '''

    # Date range to calculate statistics for
    start, end = get_date_range(start, end)

    # Query the data to calculate the 3 statistics over the date range
    SELECT = [F.min(M.tobs), F.avg(M.tobs), F.max(M.tobs)]
    stats = session.query(*SELECT).filter((M.date >= start) & (M.date <= end))
    stats = stats.all()[0]

    # Convert query results to JSON
    stats_json = jsonify(dict(
        _1_start_date=start, _2_end_date=end, 
        _3_min_temp=stats[0], _4_avg_temp=stats[1], _5_max_temp=stats[2]
    ))

    # Rollback session transaction
    session.rollback()
    return stats_json


if __name__ == '__main__':
    app.run()