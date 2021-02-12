# Movie Data ETL Pipeline

This is an extract-transform-load (ETL) pipeline for movie data from Wikipedia and the Open Movie Database (OMDB). The Wikipedia data was scraped from the site and the OMDB data was downloaded from [Kaggle](https://www.kaggle.com/rounakbanik/the-movies-dataset). As the name suggests, this movie data was extracted from flat files, cleaned and transformed, and loaded into a PostgreSQL database.

## Getting started

1. Create a PostgreSQL database using pgAdmin or any other PostgreSQL database management tool
2. Download `ratings.csv` from [Kaggle](https://www.kaggle.com/rounakbanik/the-movies-dataset) and move the file to this project's `data/raw/` subdirectory
3. In the `notebooks/` subdirectory, create a file named `config.py` and in that file, create a variable named `PSQL_PW` to store the PostgreSQL database password
4. In the `config/` subdirectory, create a file named `sys_vars.py` to store paths to data files and database properties for the connection string
5. In `config/sys_vars.py`, create the following variables and assign the corresponding value:
    - `wiki_path` - path to the JSON file containing Wikipedia movie data
    - `kaggle_path` - path to the CSV file containing the Kaggle movie data
    - `ratings_path` - path to the CSV file containing the Kaggle rating data
    - `reduced_ratings_path` - path to the CSV file containing the reduced rating data (created by the `transform()` function in the `etl.py` script)
6. In `config/sys_vars.py`, create a dictionary named `psql` with the following keys and values:
    - `user` - database user, by default 'postgres'
    - `password` - database password
    - `location` - host address, by default '127.0.0.1'
    - `port` - port used, by default '5432'
    - `database` - name of database as created in step 1
7. Run `etl.py` in the command line to run the pipeline - extract the raw data, clean and transform it, and load it into the database created in step 1

Sample connection string: `postgres://postgres:password@127.0.0.1:5432/movie_database`

## Data

1. `data/raw/wikipedia.movies.json` - Wikipedia movie data scraped from the site
2. `data/raw/movies_metadata.csv` - OMDB movie data downloaded from [Kaggle](https://www.kaggle.com/rounakbanik/the-movies-dataset)
3. `data/raw/ratings.csv` - OMDB movie ratings data download from [Kaggle](https://www.kaggle.com/rounakbanik/the-movies-dataset)
4. `data/wiki_movies.pkl` - cleaned Wikipedia movie data created by `notebooks/1-extract.ipynb`
5. `data/kaggle_movies.pkl` - cleaned Kaggle movie data created by `notebooks/1-extract.ipynb`
6. `data/movies.pkl` - joined movie data created by `notebooks/2-transform.ipynb`

In this project, data files 1 - 3 were the raw data and files 4 - 6 were generated in the notebooks following some data transformations.

## Notebooks

1. `notebooks/1-extract.ipynb` - Begins the ETL process by extracting the data from the 2 data sources (2 CSV files from Kaggle and 1 JSON file with data scraped from Wikipedia) and starts the transform step by cleaning the data.
2. `notebooks/2-transform.ipynb` - Continue the transform step by merging the Wikipedia data and the Kaggle data and performing some additional cleaning and transformation on the combined data.
3. `notebooks/3-load.ipynb` - Loads the data into a PostgreSQL database after incorporating some of the ratings data into the combined movie data.
4. `notebooks/config.py` - Hold a variable named `PSQL_PW` to store the PostgreSQL database password.

## Scripts

1. `etl.py` - main script to run the ETL pipeline
2. `utils/udf_wiki.py` - functions for cleaning the Wikipedia movie data
3. `utils/udf_kaggle.py` - functions for cleaning the OMDB movie data (from Kaggle)
4. `utils/udf_movies.py` - functions for joining and cleaning the movie data from both sources
5. `utils/udf_ratings.py` - functions for transforming the OMDB rating data (from Kaggle) and joining it into the combined movie data
6. `config/data_vars` - variables holding key and column names used in the cleaning/transformation process
7. `config/sys_vars` - variables holding paths to data files and database properties for the connection string