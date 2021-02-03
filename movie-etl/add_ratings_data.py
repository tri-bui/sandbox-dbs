import numpy as np
import pandas as pd


def reduce_ratings(ratings_df, movie_id, save_path):

    """
    Convert `timestamp` to datetime and reduce the rating data to only the 
    movies in the movie data. Save this reduced rating data to a CSV file.

    Parameters
    ----------
    ratings_df : Pandas dataframe
        Kaggle ratings data
    movie_id : array-like[int]
        List of `movie_id`s in the movie data
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