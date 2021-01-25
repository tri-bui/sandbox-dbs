import datetime
import json
import re
import numpy as np
import pandas as pd
import config_vars
from notebooks import config


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


def drop_duplicates():

    