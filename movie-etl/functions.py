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


    