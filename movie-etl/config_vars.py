# Key rename pairs for Wikipedia data (old name: new name)
keys_to_rename = {
    'Adaptation by': 'writers',
    'Box office': 'box_office',
    'Budget': 'budget',
    'Cinematography': 'cinematographers',
    'Composer(s)': 'composers',
    'Country': 'country',
    'Country of origin': 'country',
    'Directed by': 'director',
    'Director': 'director',
    'Distributed by': 'distributor',
    'Distributor': 'distributor',
    'Edited by': 'editors',
    'Editor(s)': 'editors',
    'Length': 'duration',
    'Music by': 'composers',
    'Original release': 'release_date',
    'Produced by': 'producers',
    'Producer': 'producers',
    'Producer(s)': 'producers',
    'Release date': 'release_date',
    'Released': 'release_date',
    'Running time': 'duration',
    'Screen story by': 'writers',
    'Screenplay by': 'writers',
    'Starring': 'stars',
    'Story by': 'writers',
    'Theme music composer': 'composers',
    'Written by': 'writers',
    'imdb_link': 'imdb_link', 
    'url': 'url', 
    'year': 'year'
}

# Column order for joined movie data
col_order = [
    'id', 'imdb_id', 'imdb_link', 'url', 'poster_path', 'title', 'overview', 
    'release_date_kaggle', 'year', 'runtime', 'budget_wiki', 'box_office', 
    'genres', 'country', 'original_language', 'spoken_languages', 
    'status', 'popularity', 'vote_average', 'vote_count', 
    'writers', 'director', 'cinematographers', 'editors', 'composers', 'stars', 
    'producers', 'production_companies', 'production_countries', 'distributor'
]

# New column names for joined movie data
col_names = [
    'movie_id', 'imdb_id', 'imdb_link', 'url', 'poster_path', 'title', 'overview', 
    'release_date', 'year', 'runtime', 'budget', 'revenue', 
    'genres', 'country', 'language', 'spoken_languages', 
    'status', 'popularity', 'vote_average', 'vote_count', 
    'writers', 'director', 'cinematographers', 'editors', 'composers', 'stars', 
    'producers', 'production_companies', 'production_countries', 'distributor'
]