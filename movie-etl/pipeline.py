import json
import numpy as np
import pandas as pd

import clean_wikipedia_data as clean_wiki
import clean_kaggle_data as clean_kaggle
import clean_movie_data as clean_movies
import add_ratings_data as add_ratings
import config


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


def transform(wiki_movies, kaggle_movies):


    # Clean movie data
    wiki_df = clean_wiki.clean_wiki_movies(wiki_movies) # clean Wikipedia data
    kaggle_df = clean_kaggle.clean_kaggle_movies(kaggle_movies) # clean kaggle data
    movies_df = clean_movies.join_movie_data(wiki_df, kaggle_df) # join movie data

    # Extract and reduce rating data
    ratings_df = extract(config.data_path + config.ratings_file)
    ratings_df = add_ratings.reduce_ratings(ratings_df, movies_df['movie_id'].values, 
                                            config.data_path + config.reduced_ratings_file)

    # Add aggregate rating counts to the movie data
    df = add_ratings.add_rating_count(movies_df, ratings_df)

    return df


def load():

    

    pass


def etl_pipeline():

    # Extract movie data
    wiki_data = extract(config.data_path + config.wiki_file, 'json') # Wikipedia data
    kaggle_df = extract(config.data_path + config.kaggle_file) # Kaggle data

    # Transform data
    df = transform(wiki_data, kaggle_df)

    # Extract reduced rating data
    rating_df = extract(config.data_path + config.reduced_ratings_file)
    
    return df


if __name__ == '__main__':
    etl_pipeline()

