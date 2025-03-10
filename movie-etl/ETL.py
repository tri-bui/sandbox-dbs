import json
import datetime as dt
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

from utils import udf_wiki, udf_kaggle, udf_movies, udf_ratings
from config import sys_vars


def extract(file_path, file_type='csv'):

    """
    Read data from a csv or json file.

    Parameters
    ----------
    file_path : str
        path to data file
    file_type : str, optional
        'csv' or 'json', by default 'csv'

    Returns
    -------
    Pandas dataframe 
        If reading data from a CSV file
    List[dict]
        If reading data from a json file

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
              ratings_path=sys_vars.ratings_path, 
              reduced_ratings_path=sys_vars.reduced_ratings_path):

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
    ratings_path : str
        Name of the rating data file, by default `ratings_path` from the 
        `config.sys_vars` module
    reduced_ratings_path : str
        Name of the CSV file to save the reduced rating data to, by default 
        `reduced_ratings_path` from the `config.sys_vars` module

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
    ratings_df = extract(ratings_path)
    ratings_df = udf_ratings.reduce_ratings(ratings_df, 
                                            movies_df['movie_id'].values, 
                                            reduced_ratings_path)
    n_ratings = ratings_df.shape[0] # number of rows

    # Add aggregate rating counts to the movie data
    df = udf_ratings.join_data(movies_df, ratings_df)

    return df, n_ratings


def load(data, table='movies', n_ratings=0, n_chunks=10, uri_properties=sys_vars.psql):

    """
    Load data into a PostgreSQL database. This function requires some setup 
    before running:
    1. Create a PostgreSQL database
    2. In the `sys_vars.py` script of the `config` directory, create a `psql` 
       dictionary to hold database properties for the connection string using 
       the following key names:
       a. `user` - database user, by default 'postgres'
       b. `password` - database password
       c. `location` - host address, by default '127.0.0.1'
       d. `port` - port used, by default '5432'
       e. `database` - name of database as created in step 1

    Parameters
    ----------
    data : Pandas dataframe or str
        Movie data or path to CSV file containing rating data
    table : str, optional
        Name of table in database to load into, by default 'movies'
    n_ratings : int, optional
        Number of rows in the rating data, by default 0
    n_chunks : int, optional
        Number of chunks to read and load if loading the rating data, 
        by default 10
    uri_properties : dict, optional
        Connection string properties consisting of the database user, 
        password, location, port, and name; by default `psql` from the 
        `config.sys_vars` module
    """
    
    # Connection string
    user = uri_properties['user']
    password = uri_properties['password']
    location = uri_properties['location']
    port = uri_properties['port']
    database = uri_properties['database']
    uri = f'postgresql://{user}:{password}@{location}:{port}/{database}'

    # Create database engine
    engine = create_engine(uri)

    # Load data into database
    if n_ratings: # load rating data in chunks
        loaded, start = 0, dt.datetime.now() # start tracking progress
        chunksize = round(n_ratings, -len(str(n_ratings)) + 1) // n_chunks # chunk size
        for chunk in pd.read_csv(data, chunksize=chunksize): # read in chunks
            unloaded = min(loaded + chunksize, n_ratings) # upper limit of loading range
            print(f'Loading rows {loaded:7} to {unloaded:7}', end=' | ') # print progress
            chunk.to_sql(table, engine, if_exists='append') # load chunk
            loaded += chunksize # update lower limit of loading range
            print((dt.datetime.now() - start), 'elapsed') # print elapsed time
    else: # load movie data
        data.to_sql(table, engine, if_exists='replace')


def etl_pipeline(wiki_path=sys_vars.wiki_path, 
                 kaggle_path=sys_vars.kaggle_path, 
                 ratings_path=sys_vars.reduced_ratings_path):

    """
    Extract-transform-load pipeline:
    1. Extract      -   read in the raw Wikipedia and Kaggle movie data
    2. Transform    -   clean the raw data from both sources and join them into 
                        a single dataframe, then read in and aggregate the 
                        Kaggle rating data and join it into the movie data; 
                        additionally, reduce the rating data to only the movies 
                        in the movie data
    3. Load         -   load the joined movie data and the reduced rating data 
                        into a PostgreSQL database

    Parameters
    ----------
    wiki_path : str, optional
        Path to the raw Wikipedia movie data, by default `wiki_path` from the 
        `config.sys_vars` module
    kaggle_path : str, optional
        Path to the raw Kaggle movie data, by default `kaggle_path` from the 
        `config.sys_vars` module
    ratings_path : str, optional
        Path to the reduced Kaggle ratings data, by default 
        `reduced_ratings_path` from the `config.sys_vars` module

    Returns
    -------
    Pandas dataframe
        Joined movie data with aggregate rating data
    """

    # Extract movie data
    print('Extracting data...')
    wiki_data = extract(wiki_path, 'json') # Wikipedia data
    kaggle_df = extract(kaggle_path) # Kaggle data
    print('Completed extracting.')

    # Transform data
    print('Transforming data...')
    df, n_ratings = transform(wiki_data, kaggle_df)
    print(df.info())
    print('Completed transforming.')

    # Load data into database
    print('Loading data into database...')
    load(df) # load movie data
    load(ratings_path, table='ratings', n_ratings=n_ratings) # load rating data
    print('Completed loading.')

    return df


if __name__ == '__main__':
    etl_pipeline()