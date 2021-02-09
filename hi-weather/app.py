import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy as sa
from sqlalchemy import create_engine, func as F
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

from flask import Flask, jsonify


# SQL engine and session
engine = create_engine('sqlite:///data/hawaii.sqlite')
session = Session(engine)

# Reflect db tables
Base = automap_base()
Base.prepare(engine, reflect=True)
M, S = Base.classes

# Flask app
app = Flask(__name__)


### Repeated query functions ###


def get_date_range(start_date='start', end_date='end', n_days=None):

    '''
    Get the starting and end dates of a date range as date objects.

    Parameters
    ----------
    start_date : str, optional
        Starting date in date range in the format "%Y-%m-%d", by default 'start'. If 'start', the starting date will be set as the first date 
        in the data.
    end_date : str, optional
        End date in date range in the format "%Y-%m-%d", by default 'end'. If 'end', the end date will be set as the last date in the data.
    n_days : int, optional
        Number of days to set the date range, by default None. If None, the start_date and end_date will be used.

    Notes
    _____
    If all 3 parameters are passed in, n_days will not be used. If only n_days is passed in, the range returned will be n_days from the last date in the data.


    Returns
    -------
    start_date : datetime.date
        Starting date as a date object
    end_date : datetime.date
        End date as a date object
    '''

    days_from_start = days_from_end = None

    # If no start_date specified, get first date in data
    if start_date == 'start':
        start_date = session.query(F.min(M.date)).all()[0][0]
        days_from_end = n_days
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()

    # If no end_date specified, get last date in data
    if end_date == 'end':
        end_date = session.query(F.max(M.date)).all()[0][0]
        days_from_start = n_days
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()

    # If n_days specified, get the other side of the limit
    if n_days is not None:
        if days_from_end is not None:
            start_date = end_date - dt.timedelta(days=n_days)
        elif days_from_start is not None:
            end_date = start_date + dt.timedelta(days=n_days)

    return start_date, end_date


def count_measurements_by_station():

    '''
    Query the data for the number of measurements each station has.

    Returns
    -------
    stations : list[tuple(str, int)]
        Name of each station and the number of measurements they have.
    '''

    by_station = session.query(M.station, F.count(M.station))
    by_station = by_station.group_by(M.station)
    by_station = by_station.order_by(F.count(M.station).desc()).all()
    return by_station


### App rouutes ###


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