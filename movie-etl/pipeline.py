import datetime
import json
import re
import numpy as np
import pandas as pd
import config_vars
from notebooks import config


def extract_data(file_path, file_type='csv'):

    """
    Args:
        [1] file_path (str) - path to data file
        [2] file_type (str) - "csv" or "json"

    Returns:
        Pandas dataframe if importing from a csv file or list of 
        dictionaries if importing from a json file.
    Import data from a csv or json file.

    Parameters
    ----------
    file_path : str
        path to data file
    file_type : str, optional
        csv or json, by default 'csv'

    Returns
    -------
    Pandas dataframe 
        If reading data from a CSV file
    List[dict]
        If readinng data from a json file

    Raises
    ------
    ValueError
        The `file_type` parameter only accepts 'csv' or 'json'
    """

    # If reading data from csv
    if file_type == 'csv':
        data = pd.read_csv(file_path, low_memory=False)

    # If reading data from json
    elif file_type == 'json':
        with open(file_path, 'r') as f:
            data = json.load(f)
        
    # Any input other than 'csv' or 'json'
    else:
        raise ValueError('Invalid file type.')

    return data


def transform_data():

    

    pass


def load_data():

    

    pass


def etl_pipeline():

    

    pass


if __name__ == '__main__':
    path = '/Users/tribui/Desktop/Trilogy/DV/8-ETL/movietl/data/raw/wikipedia.movies.json'
    data = extract_data(path, 'json')
    print(clean_wikipedia_movies_data(data))