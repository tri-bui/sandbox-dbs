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


def filla_dropb(cola, colb, movies_df):

    """
    Fill missing values in column a (keep) using values in column b (drop), 
    then drop column b from the joined movie data.

    Parameters
    ----------
    cola : Pandas series
        Column to fill and keep
    colb : Pandas series
        Colunmn to drop
    movies_df : Pandas dataframe
        Joined movie data

    Returns
    -------
    Pandas dataframe
        Movie data with missing values of `cola` filled and `colb` dropped
    """
    
    # Helper function to fill missing `cola` values with `colb` values
    def filla(row):
        cond1 = pd.isnull(row[cola]) or row[cola] == 0 # `cola` is 0 or missing
        cond2 = pd.notnull(row[colb]) and row[colb] != 0 # `colb` has a value
        return row[colb] if cond1 and cond2 else row[cola]
            
    # Fill `cola` missing values and drop `colb`
    movies_df[cola] = movies_df.apply(filla, axis=1)
    movies_df.drop(colb, axis=1, inplace=True)
    return movies_df


def drop_redundant_cols(movies_df):

    """
    Drop the following redundant columns:
    [1] `release_data_wiki` - after dropping the outlier
    [2] `revenue` - after using it to fill `box_office` missing values
    [3] `budget_kaggle` - after using it to fill `budget_wiki` missing values
    [4] `duration` - after using it to fill `runtime` missing values

    Parameters
    ----------
    movies_df : Pandas dataframe
        Joined movie data

    Returns
    -------
    Pandas dataframe
        Movie data with redundant columns dropped
    """

    # Drop record with `release_date` outlier and `release_date_wiki` column
    outlier_index = movies_df.loc[(movies_df['release_date_wiki'] > '2000') & 
                                  (movies_df['release_date_kaggle'] < '1960')].index
    movies_df.drop(outlier_index, inplace=True)
    movies_df.drop('release_date_wiki', axis=1, inplace=True)

    # Pairs of redundant columns
    redundant_pairs = [
        ['box_office', 'revenue'],
        ['budget_wiki', 'budget_kaggle'],
        ['runtime', 'duration']
    ]

    # Fill the first column and drop the second column for each pair
    for pair in redundant_pairs:
        movies_df = filla_dropb(pair[0], pair[1], movies_df)
    return movies_df