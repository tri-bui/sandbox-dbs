import numpy as np
import pandas as pd
from config.data_vars import col_order, col_names


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
    1. `release_data_wiki` - after dropping the outlier
    2. `revenue` - after using it to fill `box_office` missing values
    3. `budget_kaggle` - after using it to fill `budget_wiki` missing values
    4. `duration` - after using it to fill `runtime` missing values

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


def clean_cols(movies_df, col_order=col_order, col_names=col_names):

    """
    Rename columns for consistency and sort them in a logical order.

    Parameters
    ----------
    movies_df : Pandas dataframe
        Joined movie data
    col_order : list[str], optional
        Column names in logical order, by default `col_order` from the
        `config.data_vars` module
    col_names : list[str], optional
        New names for columns in the same order, by default `col_names` from 
        `config.data_vars` module

    Returns
    -------
    Pandas dataframe
        Movie data with clean column names
    """

    # Column pairs to rename (old name: new name)
    rename_pairs = {old: new for old, new in zip(col_order, col_names)}

    # Rename and reorder columns
    movies_df = movies_df.rename(rename_pairs, axis=1)
    movies_df = movies_df[col_names]
    return movies_df


def join_movie_data(wiki_df, kaggle_df):

    """
    Join the Wikipedia movie data and Kaggle movie data. Clean the columns by 
    dropping redundant columns and renaming remaining columns for consistency.

    Parameters
    ----------
    wiki_df : Pandas dataframe
        Wikipedia movie data
    kaggle_df : Pandas dataframe
        Kaggle movie data

    Returns
    -------
    Pandas dataframe
        Joined movie data
    """

    # Join Wikipedia and Kaggle data
    movies_df = pd.merge(wiki_df, kaggle_df, how='inner', 
                         on='imdb_id', suffixes=['_wiki', '_kaggle'])

    # Clean columns
    movies_df = drop_redundant_cols(movies_df) # drop redundant columns
    movies_df = clean_cols(movies_df) # rename and reorder columns

    return movies_df