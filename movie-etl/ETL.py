import json
import numpy as np
import pandas as pd

from utils import udf_wiki, udf_kaggle, udf_movies, udf_ratings
from config import sys_vars


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


def transform(wiki_movies, kaggle_movies, 
              data_path=sys_vars.data_path,
              ratings_file=sys_vars.ratings_file, 
              reduced_ratings_file=sys_vars.reduced_ratings_file):

    """
    Clean the movie and rating data, then join them all. Additionally, reduce 
    the rating data to only movies in the movie data and save this reduced 
    rating data to a CSV file.

    Parameters
    ----------
    wiki_movies : list[dict]
        Wikipedia movie data in JSON format
    kaggle_movies : Pandas dataframe
        Kaggle movie data
    data_path : str
        Path to the data directory, by default `data_path` from the 
        `config.sys_vars` module
    ratings_file : str
        Name of the rating data file, by default `ratings_file` from the 
        `config.sys_vars` module
    reduced_ratings_file : str
        Name of the CSV file to save the reduced rating data to, by default 
        `reduced_ratings_file` from the `config.sys_vars` module

    Returns
    -------
    Pandas dataframe
        Complete data containing movies and aggregate ratings
    """

    # Clean movie data
    wiki_df = udf_wiki.clean_wiki_movies(wiki_movies) # clean Wikipedia data
    kaggle_df = udf_kaggle.clean_kaggle_movies(kaggle_movies) # clean kaggle data
    movies_df = udf_movies.join_movie_data(wiki_df, kaggle_df) # join movie data

    # Extract and reduce rating data
    ratings_df = extract(data_path + ratings_file)
    ratings_df = udf_ratings.reduce_ratings(ratings_df, 
                                            movies_df['movie_id'].values, 
                                            data_path + reduced_ratings_file)

    # Add aggregate rating counts to the movie data
    df = udf_ratings.join_data(movies_df, ratings_df)

    return df


def load():

    

    pass


def etl_pipeline():

    # Extract movie data
    wiki_data = extract(sys_vars.data_path + sys_vars.wiki_file, 'json') # Wikipedia data
    kaggle_df = extract(sys_vars.data_path + sys_vars.kaggle_file) # Kaggle data

    # Transform data
    df = transform(wiki_data, kaggle_df)
    print(df.info())

    # Extract reduced rating data
    rating_df = extract(sys_vars.data_path + sys_vars.reduced_ratings_file)
    
    return df


if __name__ == '__main__':
    import os
    print(os.getcwd())
    etl_pipeline()