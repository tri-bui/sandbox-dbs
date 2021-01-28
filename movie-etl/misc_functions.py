import datetime
import json
import re
import numpy as np
import pandas as pd
import config_vars
from notebooks import config


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