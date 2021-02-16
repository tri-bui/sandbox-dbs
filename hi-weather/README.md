# Hawaii Weather Analysis

This is an analysis of Hawaii weather using data in a SQLite database. This project explores the object relational mapping (ORM) paradigm of accessing a database with SQLAlchemy. The ORM creates a decoupled system by creating Python classes that are mapped to (but separate from) tables in the database. The final deliverable is a Flask app that summarizes some key insights of the analysis.

## Data

The data is stored in the following 2 tables in a SQLite database in `hawaii.sqlite`:
1. `measurement` - precipitation (`prcp`) and temperature (`tobs`) measurements of 9 different weather stations in Hawaii from 2010 to 2017
2. `station` - metadata of the 9 weather stations, including their names and locations

## Files

1. `analysis.ipynb` - notebook for data analysis and visualization
2. `utils.py` - script containing utility functions for querying the database
3. `app.py` - script containing the Flask app with the routes described below

## App Routes

- `/` - home page with links to all the routes
- `/api/v1.0/precipitation` - precipitation data from the last 12 months
- `/api/v1.0/stations` - all weather stations and the number of measurements each station recorded
- `/api/v1.0/tobs` - the most active station's temperature observations from the last 12 months
- `/api/v1.0/temp/<start>/<end>` - the minimum, average, and maximum temperature over the date range from the start date to the end date
    - Clicking the link to the `temp` route, from the home page, displays the entire date range (i.e. the default start date will be the first date in the data and the default end date will be the last date in the data)
    - Change `start` and/or `end` in the URL to change the default dates and visit that updated URL to display the temperature statistics over the new date range
    - Use the date format `%Y-%m-%d` (e.g. `2010-12-31`)
    - Sample URL: `/api/v1.0/temp/2010-12-31/2015-1-1`

## Getting Started

- Requirements: Python 3, Numpy, Pandas, Matplotlib, SQLAlchemy, Flask
- Run `app.py` in the terminal and visit the provided URL to launch the app