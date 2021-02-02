import re
import numpy as np
import pandas as pd
from config_vars import keys_to_rename




""" ### CLEANING ### """


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


def clean_movie(movie_dict, keys_to_rename=keys_to_rename):

    """
    Rename keys for consistency and to consolidate similar columns into 1. All 
    other keys not in the list are dropped from the data.

    Parameters
    ----------
    movie_dict : dict
        Record to clean
    keys_to_rename : dict, optional
        mapping of old key name to new key name, by default `keys_to_rename` 
        from `config_vars` module

    Returns
    -------
    Dict
        Clean movie record
    """
    
    # Create empty dictionary to hold clean data
    clean_dict = {}
    
    # Add keys to dictionary
    for old, new in keys_to_rename.items():
        if old in movie_dict:
            clean_dict[new] = movie_dict[old]
        
    return clean_dict




""" ### PARSING ### """


def obj_to_str(obj):

    """
    Convert an object to a string if it's not already a string. If it's a list, 
    join its items into a single string.

    Parameters
    ----------
    obj : str or list[str]
        Object to convert to string

    Returns
    -------
    Str
        Object as a string
    """

    return ' '.join(obj) if isinstance(obj, list) else obj


def parse_budget(s):

    """
    Parse a `budget` string and convert it to a float.

    Parameters
    ----------
    s : str or float
        String `budget` value

    Returns
    -------
    Float
        Numeric `budget` value
    """
    
    # Null check
    if isinstance(s, float):
        return s
    
    # Remove $, spaces, and commas
    s = re.sub(r'[\$\s,]', '', s).lower()
    
    # Convert to float
    if 'mil' in s:
        f = float(s.replace('mil', '')) * 1e6 # million
    else:
        f = float(s)
    return f


def parse_box_office(s):

    """
    Parse a `box_office` string and convert it to a float.

    Parameters
    ----------
    s : str or float
        String `box_office` value

    Returns
    -------
    Float
        Float `box_office` value
    """
    
    # Null check
    if isinstance(s, float):
        return s
    
    # Remove $, spaces, and commas
    s = re.sub(r'[\$\s,]', '', s).lower()
    
    # Convert to float
    if 'k' in s:
        f = float(s.replace('k', '')) * 1e3 # thousand
    elif 'm' in s:
        f = float(s.replace('m', '')) * 1e6 # million
    elif 'b' in s:
        f = float(s.replace('b', '')) * 1e9 # billion
    elif '.' in s:
        f = float(s.replace('.', '')) # for numbers using "." as a thousand-separator
    else:
        f = float(s)
    return f


def parse_duration(s):
    
    """
    Parse a `duration` string and convert it to an integer.

    Parameters
    ----------
    s : str or float
        String `duration` value

    Returns
    -------
    Int
        Integer `duration` value
    """
    
    # Null check
    if isinstance(s, float):
        return s
    
    # Remove seconds, "m", and spaces
    s = re.sub(r'\:\s*\d{1,2}', '', s)
    s = re.sub(r'm|\s*', '', s, flags=re.IGNORECASE)
    
    # Convert to int
    match = re.search(r'(\d)(ho?u?r?s?)(\d\d?)?', s, flags=re.IGNORECASE)
    if match: # if time is in hours
        i = int(match.group(1)) * 60 # hours to minutes
        if match.group(3):
            i += int(match.group(3)) # add minutes
    else: # if time is in minutes
        i = int(s)
    return i




""" ### RECASTING ### """


def release_date_to_dt(release_date):

    """
    Parse `release_date` in the Wikipedia data and convert it to datetime type.

    Parameters
    ----------
    release_date : Pandas series[obj]
        `release_date` column in the Wikipedia data

    Returns
    -------
    Pandas series[datetime]
        `release_date` column as a datetime type
    """

    # Convert all values to strings
    release_date = release_date.apply(obj_to_str)

    # Select lower limit of date ranges
    release_date = release_date.str.strip() \
                               .str.replace(r' [-–—] \d\d?', '', regex=True)

    # Date formats
    format1 = r'(?:\d\d? )?[a-z]{3,9}(?: \d\d?)?,? \d{4}'
    format2 = r'\d{4}(?:\D\d\d?\D\d\d?)?'
    formats = f'({format1}|{format2})'

    # Extract date from string
    release_date = release_date.str.extract(formats, flags=re.IGNORECASE)[0]

    # Convert column to datetime type
    release_date = pd.to_datetime(release_date, infer_datetime_format=True)
    return release_date


def budget_to_num(budget):

    """
    Parse `budget` in the Wikipedia data and convert it to numeric type.

    Parameters
    ----------
    budget : Pandas series[obj]
        `budget` column in the Wikipedia data

    Returns
    -------
    Pandas series[float]
        `budget` column as a numeric type
    """

    # Convert all values to strings
    budget = budget.apply(obj_to_str)

    # Clean string and select lower limit of amount ranges
    budget = budget.str.strip().str.replace(r'\[\s*(?:\w+\s*)*\]', '', regex=True) \
                               .str.replace(r'[-–—]\s?\$?\d+', '', regex=True)

    # Budget formats
    format1 = r'\$?\s?\d{1,3}(?:\.\d+)?\s*mil'
    format2 = r'\$?\s?\d{1,3}(?:,\d{3})+'
    formats = f'({format1}|{format2})'

    # Replace values not captured by these formats with NaN
    contains = budget.dropna().str.contains(formats, flags=re.IGNORECASE)
    for val in budget.dropna()[~contains].unique():
        budget.replace(val, np.NaN, inplace=True)

    # Parse amount from string
    budget = budget.str.extract(formats, flags=re.IGNORECASE)[0]
    budget = budget.apply(parse_budget)
    return budget


def box_office_to_num(box_office):

    """
    Parse `box_office` in the Wikipedia data and convert it to numeric type.

    Parameters
    ----------
    box_office : Pandas series[obj]
        `box_office` column in the Wikipedia data

    Returns
    -------
    Pandas series[float]
        `box_office` column as numeric
    """

    # Convert all values to strings
    box_office = box_office.apply(obj_to_str)

    # Box office formats
    format1 = r'\$?\s?\d{1,3}(?:\.\d+)?\s*[kmb]'
    format2 = r'\$?\s?\d{1,3}(?:[\s\.,]?\d{3})+\$?'
    formats = f'({format1}|{format2})'

    # Replace values not captured by these formats with NaN
    contains = box_office.dropna().str.contains(formats, flags=re.IGNORECASE)
    for val in box_office.dropna()[~contains].unique():
        box_office.replace(val, np.NaN, inplace=True)

    # Parse amount from string
    box_office = box_office.str.extract(formats, flags=re.IGNORECASE)[0]
    box_office = box_office.apply(parse_box_office)
    return box_office


def duration_to_num(duration):

    """
    Parse `duration` in the Wikipedia data and convert it to numeric type.

    Parameters
    ----------
    duration : Pandas series[obj]
        `duration` column in the Wikipedia data

    Returns
    -------
    Pandas series[float]
        `duration` column as numeric
    """

    # Convert all values to strings
    duration = duration.apply(obj_to_str)

    # Clean string and select lower limit of duration ranges
    duration = duration.str.strip().str.replace(r'\[\d\]', '', regex=True) \
                                   .str.replace(r'[-–—]\s?\d+', '', regex=True)

    # Duration formats
    format1 = r'(?:\d\s*ho?u?r?s?\s*)?\d{1,3}\s*m'
    format2 = r'\d\s*ho?u?r?s?|\d{1,2}\s*\:\s*\d{1,2}'
    formats = f'({format1}|{format2})'

    # Replace values not captured by these formats with NaN
    contains = duration.dropna().str.contains(formats, flags=re.IGNORECASE)
    for val in duration.dropna()[~contains].unique():
        duration.replace(val, np.NaN, inplace=True)

    # Parse duration from string
    duration = duration.str.extract(formats, flags=re.IGNORECASE)[0]
    duration = duration.apply(parse_duration)
    return duration


def recast_wiki_columns(wiki_data):

    """
    Recast the following columns in the Wikipedia data:
    1. `release_date` to datetime
    2. `budget` to numeric
    3. `box_office` to numeric
    4. `duration` to numeric

    Parameters
    ----------
    wiki_data : Pandas dataframe
        Wikipedia data with the 4 columns listed above

    Returns
    -------
    Pandas dataframe
        Wikipedia data with the 4 columns above recasted
    """

    # Recast columns
    wiki_data['release_date'] = release_date_to_dt(wiki_data['release_date'])
    wiki_data['budget'] = budget_to_num(wiki_data['budget'])
    wiki_data['box_office'] = box_office_to_num(wiki_data['box_office'])
    wiki_data['duration'] = duration_to_num(wiki_data['duration'])
    return wiki_data