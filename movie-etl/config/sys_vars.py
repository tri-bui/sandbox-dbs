# Data paths
data_path = '/Users/tribui/Desktop/projects/sandbox-dbs/movie-etl/data/'
wiki_file = 'raw/wikipedia.movies.json'
kaggle_file = 'raw/movies_metadata.csv'
ratings_file = 'raw/ratings.csv'
reduced_ratings_file = 'ratings_min.csv'

# File paths
wiki_path = data_path + wiki_file
kaggle_path = data_path + kaggle_file
ratings_path = data_path + ratings_file
reduced_ratings_path = data_path + reduced_ratings_file

# PostgreSQL connection string properties
psql = {
    'user': 'postgres', 
    'password': '12qwaszx', 
    'location': '127.0.0.1', 
    'port': '5432',
    'database': 'movies'
}

