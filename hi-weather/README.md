# Hawaii Weather Analysis

This is an analysis of Hawaii weather using data in a SQLite database. This project explores the object relational mapping (ORM) paradigm of accessing a database with SQLAlchemy. The final deliverable is a Flask app that summarizes some key insights of the analysis.

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
