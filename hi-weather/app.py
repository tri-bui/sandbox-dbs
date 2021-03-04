import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, jsonify

from sqlalchemy import create_engine, func as F
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

import utils


# SQL engine and session
engine = create_engine('sqlite:///hi-weather/hawaii.sqlite')
session = Session(engine)

# Reflect db tables
Base = automap_base()
Base.prepare(engine, reflect=True)
M, S = Base.classes

# Flask app
app = Flask(__name__)


""" App Routes """


@app.route('/')
def home():

    """ Home page with links to routes """

    return """
        <h1>Welcome to the Hawaii Weather Analysis API!</h1><br />

        <h2>Available routes:</h2>
        <h3><a href="/api/v1.0/precipitation">Precipitation (last 12 months)</a></h3>
        <h3><a href="/api/v1.0/stations">Weather Stations' Measurement Counts</a></h3>
        <h3><a href="/api/v1.0/tobs">Most Active Station's Temperature Observations (last 12 months)</a></h3>
        <h3><a href="/api/v1.0/temp/start/end">Temperature Statistics</a></h3>
    """


@app.route('/api/v1.0/precipitation')
def precipitation():

    """ Precipitation data from the last 12 months """

    start, _ = utils.get_date_range(session=session, table=M, n_days=365) # get start date
    prcp_12m = session.query(M.date, M.prcp).filter(M.date >= start).all() # query precipitation
    prcp_json = jsonify(_Route='Precipitation in the last 12 months',
                        Precipitation={date: prcp for date, prcp in prcp_12m}) # convert to json
    session.rollback() # rollback session transaction before returning
    return prcp_json


@app.route('/api/v1.0/stations')
def stations():

    """ Measurement count from each station """

    stations = utils.count_by_station(session=session, table=M) # query measurement counts
    stations_json = jsonify(_Route='Weather stations and number of measurements recorded',
                            Stations={station: count for station, count in stations}) # convert to json
    session.rollback() # rollback session transaction before returning
    return stations_json


@app.route('/api/v1.0/tobs')
def tobs():
    
    """ Most active station's temperature observations from the last 12 months """

    # Date range for the last 12 months in the data
    start, _ = utils.get_date_range(session=session, table=M, n_days=365)

    # Get the most active station (most measurements)
    most_active = utils.count_by_station(session=session, table=M)[0][0]

    # Query the `tobs` data for this stations from the last 12 months
    temps = session.query(M.date, M.tobs)
    temps = temps.filter((M.station == most_active) & (M.date >= start)).all()

    # Convert query results to JSON
    temps_json = jsonify({date: temp for date, temp in temps})

    # Rollback session transaction
    session.rollback()

    return temps_json


@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def temp_stats(start='start', end='end'):

    """ Minimum, average, and maximum temperature over the date range from the 
    start date to the end date """

    # Date range to calculate statistics for
    start, end = utils.get_date_range(session=session, table=M, 
                                      start_date=start, end_date=end)

    # Query the data to calculate the 3 statistics over the date range
    SELECT = [F.min(M.tobs), F.avg(M.tobs), F.max(M.tobs)]
    stats = session.query(*SELECT).filter((M.date >= start) & (M.date <= end))
    stats = stats.first()

    # Convert query results to JSON
    stats_json = jsonify(dict(
        _1_start_date=start, 
        _2_end_date=end, 
        _3_min_temp=stats[0], 
        _4_avg_temp=stats[1], 
        _5_max_temp=stats[2]
    ))

    # Rollback session transaction
    session.rollback()

    return stats_json


if __name__ == '__main__':
    app.run()