# sqlalchemy-challenge

### Background
Performing climate analysis for Honolulu, Hawaii in order to help plan a vacation. 

## Step 1 - Climate Analysis and Exploration
To begin, I used Python and SQLAlchemy to do basic climate analysis and data exploration of the climate database. All of the following analysis are completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

The climate_starter notebook and hawaii.sqlite files were used to complete the climate analysis and data exploration.

- I used SQLAlchemy create_engine to connect to the hawaii sqlite database.
 
- I also used SQLAlchemy automap_base() to reflect the tables into classes and saved a reference to those classes called Station and Measurement.

- Linked Python to the database by creating an SQLAlchemy session.


### Precipitation Analysis


- Found the most recent date in the data set.

- Used the most recent date to retrieve the last 12 months of precipitation data by querying the 12 preceding months of data.

- Selected only the date and prcp values, loaded the query results into a Pandas DataFrame and set the index to the date column, also sorting the DataFrame by date.

- Plotted the results using Matplotlib.

- Used Pandas to print the summary statistics for the precipitation data.


### Station Analysis


- Designed a query to calculate the total number of stations in the dataset.

- Designed another query to find the most active stations.

- Listed the stations and observation counts in descending order.

- Using the most active station id, I calculated the lowest, highest, and average temperature.

- Designed a query to retrieve the last 12 months of temperature observation data (TOBS).

- Filtered by the station with the highest number of observations.

- Designed a query to retrieve the last 12 months of temperature observation data for this station.

- Plotted the results as a histogram, setting bins=12.

- Closed out the session.


## Step 2 - Climate App
After completing the initial analysis, I designed a Flask API based on the queries that I developed.

I used Flask to create these routes:

/ (Home page)

/api/v1.0/precipitation
- Converted the query results to a dictionary using date as the key and prcp as the value.
- Returned the JSON representation of the dictionary.

/api/v1.0/stations
- Returned a JSON list of stations from the dataset.

/api/v1.0/tobs
- Queried the dates and temperature observations of the most active station for the last year of data.
- Returned a JSON list of temperature observations (TOBS) for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>
- Returned a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
- When given the start only, it calculates TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
- When given the start and the end date, it calculates the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
