import json
import numpy as np
import pandas as pd

import clean_wikipedia_data as clean_wiki
import misc_functions as misc
from notebooks import config


def extract(file_path, file_type='csv'):

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


def transform():

    

    pass


def load():

    

    pass


def clean_wiki_movies(wiki_movies):

    # Filter for movies
    movies = clean_wiki.filter_for_movies(wiki_movies)

    # Clean movies and convert to dataframe
    movies = [clean_wiki.clean_movie(movie) for movie in movies]
    movies_df = pd.DataFrame(movies)

    # Drop duplicate rows
    movies_df = misc.drop_duplicates(movies_df)

    # Recast columns to appropriate data types
    movies_df = clean_wiki.recast_wiki_columns(movies_df)
    return movies_df


def etl_pipeline():

    

    pass


if __name__ == '__main__':
    path = '/Users/tribui/Desktop/projects/sandbox-dbs/movie-etl/data/raw/wikipedia.movies.json'
    data = extract(path, 'json')
    print(len(data))

    data_filtered = clean_wiki.filter_for_movies(data)
    print(len(data_filtered))

    print(clean_wiki_movies(data_filtered).info())
