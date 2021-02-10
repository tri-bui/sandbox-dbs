import datetime as dt
import numpy as np
import pandas as pd
from sqlalchemy import func as F


def get_date_range(session, table, start_date='start', end_date='end', n_days=None):

    """
    Get the starting and end dates of a date range as date objects.

    Parameters
    ----------
    session : SQLAlchemy session object
        Database session
    table : SQLAlchemy ORM table class
        Table to query
    start_date : str, optional
        Start date in date range in the format "%Y-%m-%d", by default 'start'. 
        If 'start', the starting date will be set as the first date in the data.
    end_date : str, optional
        End date in date range in the format "%Y-%m-%d", by default 'end'. 
        If 'end', the end date will be set as the last date in the data.
    n_days : int, optional
        Number of days to set the date range, by default None. If None, the 
        `start_date` and `end_date` will be used.

    Notes
    _____
    If an argument is passed in for the last 3 parameters, `n_days` will not be 
    used. If only `n_days` is passed in, the range returned will be `n_days` 
    from the last date in the data.

    Returns
    -------
    start_date : datetime.date
        Starting date as a date object
    end_date : datetime.date
        End date as a date object
    """

    # Initialize date range variables
    days_from_start = days_from_end = None

    # If no `start_date` specified, get first date in data
    if start_date == 'start':
        start_date = session.query(F.min(table.date)).first()[0] # first date
        days_from_end = n_days # num days from end
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()

    # If no `end_date` specified, get last date in data
    if end_date == 'end':
        end_date = session.query(F.max(table.date)).first()[0] # last date
        days_from_start = n_days # num days from start
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()

    # If `n_days` specified, get the other side of the limit
    if n_days is not None:
        if days_from_end is not None: # `days_from_end` to `end_date`
            start_date = end_date - dt.timedelta(days=n_days)
        elif days_from_start is not None: # `start_date` to `days_from_start`
            end_date = start_date + dt.timedelta(days=n_days)

    return start_date, end_date


def count_by_station(session, table):

    """
    Query the data for the number of measurements each station has.

    Parameters
    ----------
    session : SQLAlchemy session object
        Database session
    table : SQLAlchemy ORM table class
        Table to query

    Returns
    -------
    stations : list[tuple(str, int)]
        Name of each station and the number of measurements they have.
    """

    by_station = session.query(table.station, F.count(table.station))
    by_station = by_station.group_by(table.station)
    by_station = by_station.order_by(F.count(table.station).desc()).all()
    return by_station