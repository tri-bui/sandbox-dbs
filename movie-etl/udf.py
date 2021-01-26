import datetime
import json
import re
import numpy as np
import pandas as pd
import config_vars
from notebooks import config


""" ### CLEANING FUNCTIONS ### """


def filter_for_movies(movie_data):

    """
    Filter the Wikipedia movie data for movies with an `imdb_link`, `director`, 
    and `duration`, but missing `no. of seasons` and `no. of episodes`.

    Parameters
    ----------
    movie_data : list[dict]
        Scraped Wikipedia movie data in JSON format

    Returns
    -------
    List[dict]
        Movie data with TV shows filtered out
    """

    return [movie for movie in movie_data if 
                ('imdb_link' in movie) and 
                ('Directed by' in movie or 'Director' in movie) and 
                ('Duration' in movie or 'Length' in movie or 'Running time' in movie) and 
                ('No. of seasons' not in movie) and 
                ('No. of episodes' not in movie)]


def clean_movie(movie_dict, keys_to_rename=config_vars.keys_to_rename):

    """
    Rename keys for consistency and to consolidate similar columns into 1. All 
    other keys not in the list are dropped from the data.

    Parameters
    ----------
    movie_dict : dict
        Record to clean
    keys_to_rename : dict, optional
        mapping of old key name to new key name, by default `keys_to_rename` 
        from `config_vars` module

    Returns
    -------
    Dict
        Clean movie record
    """
    
    # Create empty dictionary to hold clean data
    clean_dict = {}
    
    # Add keys to dictionary
    for old, new in keys_to_rename.items():
        if old in movie_dict:
            clean_dict[new] = movie_dict[old]
        
    return clean_dict


def drop_duplicates(movies_df):

    """
    Drop duplicate rows based on `imdb_id`. If `imdb_id` is not in the columns, 
    create it from `imdb_link`. Additionally, drop any movies with an `imdb_id` 
    of 0.

    Parameters
    ----------
    movies_df : Pandas dataframe
        movie data

    Returns
    -------
    Pandas dataframe
        Data with duplicate rows dropped
    """

    # Extract `imdb_id` into a new column if not already present
    if 'imdb_id' not in movies_df.columns and 'imdb_link' in movies_df.columns:
        movies_df['imdb_id'] = movies_df['imdb_link'].str.extract(r'(tt\d{7})')

    # Drop movies with an `imdb_id` of 0
    id0 = movies_df.query('imdb_id == 0').index
    movies_df.drop(id0, inplace=True)

    # Drop duplicate rows
    movies_df.drop_duplicates(subset=['imdb_id'], inplace=True)
    return movies_df




""" ### DATA TYPE FUNCTIONS ### """


def obj_to_str(obj):

    """
    Convert an object to a string if it's not already a string. If it's a list, 
    join its items into a single string.

    Parameters
    ----------
    obj : str or list[str]
        Object to convert to string

    Returns
    -------
    Str
        Object as a string
    """

    return ' '.join(obj) if isinstance(obj, list) else obj


def release_date_to_dt(release_date):

    """
    Parse `release_date` in the Wikipedia data and convert it to datetime type.

    Parameters
    ----------
    release_date : Pandas series[obj]
        `release_date` column in the Wikipedia data

    Returns
    -------
    Pandas series[datetime]
        `release_date` column as datetime
    """

    # Convert all values to strings
    release_date = release_date.apply(obj_to_str)

    # Select lower limit of date ranges
    release_date = release_date.str.strip() \
                               .str.replace(r' [-–—] \d\d?', '', regex=True)

    # Date formats
    format1 = r'(?:\d\d? )?[a-z]{3,9}(?: \d\d?)?,? \d{4}'
    format2 = r'\d{4}(?:\D\d\d?\D\d\d?)?'
    formats = f'({format1}|{format2})'

    # Extract date from string
    release_date = release_date.str.extract(formats, flags=re.IGNORECASE)[0]

    # Convert column to datetime type
    release_date = pd.to_datetime(release_date, infer_datetime_format=True)
    return release_date


def recast_wiki_columns(wiki_data):

    """
    Recast the following columns in the Wikipedia data:
    1. `release_date` to datetime
    2. `budget` to numeric
    3. `box_office` to numeric
    4. `duration` to numeric

    Parameters
    ----------
    wiki_data : Pandas dataframe
        Wikipedia data with the 4 columns listed above

    Returns
    -------
    Pandas dataframe
        Wikipedia data with the 4 columns above recasted
    """

    # Recast columns
    wiki_data['release_date'] = release_date_to_dt(wiki_data['release_date'])
    return wiki_data