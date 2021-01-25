import datetime
import json
import re
import numpy as np
import pandas as pd
import config_vars
from notebooks import config


def list_to_str(obj):
    
    '''
    Helper function for Pandas series's apply method to convert 
    a string to a list.
    
    Args:
        obj (float, str, list) - row item

    Returns:
        Self if obj is not a list, else list items joined into a string
    '''
    
    return obj if not isinstance(obj, list) else ' '.join(obj)


def parse_budget(s):

    '''
    Helper function for Pandas series's apply method to parse 
    a budget string and convert it to a float.

    Args:
        s (str) - budget string

    Returns:
        Budget as a float
    '''

    # Null check
    if isinstance(s, float):
        return s
    
    # Remove $, spaces, and commas
    s = re.sub(r'[\$\s,]', '', s).lower()
    
    # Convert to float
    if 'mil' in s:
        f = float(s.replace('mil', '')) * 1e6
    else:
        f = float(s)
        
    return f
    

def wiki_json_to_df(wikipedia_data, keys_dict=config_vars.keys_to_rename):

    '''
    Filter for movies in Wikipedia data. Within each movie to keep, 
    filter for keys to keep and rename them according to `keys_dict`.
    An item is a movie if it has runtime, director, and imdb_link 
    data and does not have episode or season data. Convert the final 
    data to a Pandas dataframe.

    Args:
        [1] wikipedia_data (list[dict]) - Wikipedia json data
        [2] keys_dict (dict) - keys to keep and rename

    Returns:
        Trimmed Wikipedia data as a Pandas dataframe.
    '''

    # Check all items
    wiki_data = []
    for mov in wikipedia_data:

        # Conditions
        con1 = 'Duration' in mov or 'Length' in mov or 'Running time' in mov 
        con2 = 'Directed by' in mov or 'Director' in mov
        con3 = 'imdb_link' in mov
        con4 = 'No. of episodes' not in mov and 'No. of seasons' not in mov

        # Keep if item is a movie
        if con1 and con2 and con3 and con4:

            # Clean keys to keep
            clean_movie = {}
            for oldkey, newkey in keys_dict.items():
                if oldkey in mov:
                    clean_movie[newkey] = mov[oldkey]

            # Add clean movie to list
            wiki_data.append(clean_movie)
    
    return pd.DataFrame(wiki_data)


def recast_date(obj_col):

    '''
    Convert an object column containing dates to datetime type.

    Args:
        obj_col (Pandas series[obj]) - object column with dates

    Returns:
        Cleaned column converted to datetime type.
    '''

    # Convert lists to strings
    date_col = obj_col.apply(list_to_str)

    # Remove date ranges
    date_col = date_col.str.replace(r' [-–—] \d\d?', '', regex=True)

    # Extract dates
    f1 = r'(?:\d\d? )?[a-z]{3,9}(?: \d\d?)?,? \d{4}'
    f2 = r'\d{4}(?:\D\d\d?\D\d\d?)?'
    date_col = date_col.str.extract(f'({f1}|{f2})', flags=re.IGNORECASE)[0]

    return pd.to_datetime(date_col, infer_datetime_format=True)


def recast_budget(obj_col):

    '''
    Recast the budget column to a numeric type.

    Args:
        obj_col (Pandas series[obj]) - object column with budget values

    Returns:
        Cleaned column converted to numeric type.
    '''

    # Convert lists to strings
    num_col = obj_col.apply(list_to_str).str.strip()

    # Remove citation brackets in strings (ex: [1])
    num_col = num_col.str.replace(r'\[\s*(?:\w+\s*)*\]', '', regex=True)

    # Remove number ranges
    num_col = num_col.str.replace(r'[-–—]\s?\$?\d+', '', regex=True)

    # Budget string formats
    f1 = r'\$?\s?\d{1,3}(?:\.\d+)?\s*mil'
    f2 = r'\$?\s?\d{1,3}(?:,\d{3})+'

    # Replace values with different formats with NaN
    contains1 = num_col.dropna().str.contains(f1, flags=re.IGNORECASE)
    contains2 = num_col.dropna().str.contains(f2, flags=re.IGNORECASE)
    for val in num_col.dropna()[~contains1 & ~contains2].unique().tolist():
        num_col.replace(val, np.NaN, inplace=True)

    # Extract budget
    num_col = num_col.str.extract(f'({f1}|{f2})', flags=re.IGNORECASE)[0]

    return num_col.apply(parse_budget)


def clean_wikipedia_movies_data(wikipedia_data):

    '''

    '''

    # Filter for movies
    wiki_df = wiki_json_to_df(wikipedia_data)

    # Extract id from imdb link
    wiki_df['imdb_id'] = wiki_df.imdb_link.str.extract(r'(tt\d{7})')

    # Drop duplicate rows
    wiki_df.drop_duplicates(subset=['imdb_id'], inplace=True)

    # Recast `release_date` to datetime type
    wiki_df['release_date'] = recast_to_datetime(wiki_df['release_date'])
    
    
    
    return wiki_df.info()




def clean_kaggle_movies_data():

    '''

    '''

    pass


def extract_data(file_path, file_type='csv'):

    '''
    Import data from a csv or json file.

    Args:
        [1] file_path (str) - path to data file
        [2] file_type (str) - "csv" or "json"

    Returns:
        Pandas dataframe if importing from a csv file or list of 
        dictionaries if importing from a json file.
    '''

    # If importing from csv
    if file_type == 'csv':
        data = pd.read_csv(file_path, low_memory=False)

    # If importing from json
    elif file_type == 'json':
        with open(file_path, 'r') as f:
            data = json.load(f)
        
    # Invalid file type
    else:
        raise ValueError('Invalid file type.')

    return data


def transform_data():

    '''

    '''

    pass


def load_data():

    '''

    '''

    pass


def etl_pipeline():

    '''

    '''

    pass


if __name__ == '__main__':
    path = '/Users/tribui/Desktop/Trilogy/DV/8-ETL/movietl/data/raw/wikipedia.movies.json'
    data = extract_data(path, 'json')
    print(clean_wikipedia_movies_data(data))