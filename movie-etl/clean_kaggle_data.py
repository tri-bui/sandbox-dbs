import re
import numpy as np
import pandas as pd
import config_vars


""" ### CLEANING FUNCTIONS ### """


def drop_cols(movies_df):

    """
    Filter out adult videos and drop columns that will not be used.

    Parameters
    ----------
    movie_df : Pandas dataframe
        Kaggle movie data

    Returns
    -------
    Pandas dataframe
        Kaggle movie data with adult videos filtered out and columns dropped
    """

    # Filter out adult videos
    movies_df = movies_df.query('adult != "True"').copy()

    # Drop columns
    cols_to_drop = ['adult', 'belongs_to_collection', 'homepage', 
                    'original_title', 'tagline', 'video']
    movies_df.drop(cols_to_drop, axis=1, inplace=True)
    return movies_df