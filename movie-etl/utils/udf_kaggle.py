import numpy as np
import pandas as pd
import udf_movies


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


def recast_cols(movies_df):

    """
    Recast `release_date` to datetime type and recast `budget`, `id`, and 
    `popularity` to numeric type.

    Parameters
    ----------
    movies_df : Pandas dataframe
        Kaggle movie data

    Returns
    -------
    Pandas dataframe
        Kaggle movie data columns recasted
    """

    # Recast `release_date` to datetime type
    movies_df['release_date'] = pd.to_datetime(movies_df['release_date'])

    # Recast `budget` and `id` to integer type
    movies_df['budget'] = movies_df['budget'].astype(int)
    movies_df['id'] = movies_df['id'].astype(int)

    # Recast `popularity` to float type
    movies_df['popularity'] = movies_df['popularity'].astype(float)
    return movies_df


def clean_kaggle_movies(movies_df):

    """
    Clean the Kaggle movie data with the following steps:
    1. Drop duplicate rows
    2. Filter out adult videos and drop unnecessary columns
    3. Recast columns to appropriate data types

    Parameters
    ----------
    movies_df : Pandas dataframe
        Kaggle movie data

    Returns
    -------
    Pandas dataframe
        Clean Kaggle movie data
    """

    # Drop duplicate rows
    movies_df = udf_movies.drop_duplicates(movies_df)

    # Filter out adult videos and drop unnecessary columns
    movies_df = drop_cols(movies_df)

    # Recast columns to appropriate data types
    movies_df = recast_cols(movies_df)
    
    return movies_df