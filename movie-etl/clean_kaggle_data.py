import numpy as np
import pandas as pd




""" ### CLEANING ### """


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
    movies_df = movies_df.query('imdb_id != "0"').copy()

    # Drop duplicate rows
    movies_df.drop_duplicates(subset=['imdb_id'], inplace=True)
    return movies_df


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