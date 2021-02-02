import json
import numpy as np
import pandas as pd

import clean_wikipedia_data as clean_wiki
import clean_kaggle_data as clean_kaggle
import clean_movie_data as clean_movies
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
    movies_df = clean_movies.drop_duplicates(movies_df)

    # Recast columns to appropriate data types
    movies_df = clean_wiki.recast_wiki_columns(movies_df)
    return movies_df


def clean_kaggle_movies(movies_df):

    # Drop duplicate rows
    movies_df = clean_movies.drop_duplicates(movies_df)

    # Filter out adult videos and drop unused columns
    movies_df = clean_kaggle.drop_cols(movies_df)

    # Recast columns to appropriate data types
    movies_df = clean_kaggle.recast_cols(movies_df)
    return movies_df


def etl_pipeline():

    # Data paths
    path = '/Users/tribui/Desktop/projects/sandbox-dbs/movie-etl/data/raw/'
    wiki_file = 'wikipedia.movies.json'
    kaggle_file = 'movies_metadata.csv'
    rating_file = 'ratings.csv'

    # Wikipedia data
    wiki_data = extract(path + wiki_file, 'json') # extract
    wiki_df = clean_wiki_movies(wiki_data) # clean
    print(wiki_df.info())

    # Kaggle data
    kaggle_df = extract(path + kaggle_file) # extract
    kaggle_df = clean_kaggle_movies(kaggle_df) # clean
    print(kaggle_df.info())

    # Join Wikipedia and Kaggle data
    movies_df = pd.merge(wiki_df, kaggle_df, how='inner', 
                         on='imdb_id', suffixes=['_wiki', '_kaggle'])
    print(movies_df.info())

    # Clean columns
    movies_df = clean_movies.drop_redundant_cols(movies_df) # drop redundant columns
    movies_df = clean_movies.clean_cols(movies_df) # rename and reorder columns
    print(movies_df.info())

    return movies_df


if __name__ == '__main__':
    etl_pipeline()

