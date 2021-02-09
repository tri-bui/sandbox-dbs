import datetime as dt
import numpy as np
import pandas as pd

from sqlalchemy import create_engine, func as F
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

from flask import Flask, jsonify


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