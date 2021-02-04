import numpy as np
import pandas as pd


def add_rating_count(movies_df, ratings_df):

    """
    Aggregate rating counts for each movie and merge the aggregate rating data 
    into the movie data.

    Parameters
    ----------
    movies_df : Pandas dataframe
        Joined movie data
    ratings_df : Pandas dataframe
        Kaggle rating data

    Returns
    -------
    Pandas dataframe
        Movie data with aggregate rating data
    """

    # Count ratings by movie
    pivot = pd.pivot_table(data=ratings_df, index="movieId", columns='rating', 
                           values='timestamp', aggfunc='count', fill_value=0).reset_index()

    # Rename columns
    pivot.columns = ['movie_id'] + ['rating_' + str(rating) for rating in pivot.columns[1:]]
    
    # Merge aggregate rating data into movie data
    df = pd.merge(movies_df, ratings_count_df, on='movie_id', how='left')

    # Fill missing rating counts with 0
    for col in df.columns[-10:]:
        df[col].fillna(0, inplace=True)

    return df


def reduce_ratings(ratings_df, movie_id, save_path):

    """
    Convert `timestamp` to datetime and reduce the rating data to only the 
    movies in the movie data. Save this reduced rating data to a CSV file.

    Parameters
    ----------
    ratings_df : Pandas dataframe
        Kaggle ratings data
    movie_id : array-like[int]
        List of `id`s in the movie data
    save_path : str
        Path to save the reduced rating data

    Returns
    -------
    Pandas dataframe
        Reduced rating data
    """

    # Convert timestamp to datettime
    ratings_df['timestamp'] = pd.to_datetime(ratings_df['timestamp'], unit='s')

    # Filter the rating data to only the movies in the movie data
    reduced_df = ratings_df[ratings_df['movieId'].isin(movie_id)]

    # Save reduced rating data
    reduced_df.to_csv(save_path, index=False)
    return reduced_df