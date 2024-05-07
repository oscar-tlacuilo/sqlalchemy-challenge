# Import necessary dependencies
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

#################################################
# Database Setup
#################################################

# Create engine for the "hawaii.sqlite" database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link to the database
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Create an app, being sure to pass __name__
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define the root route and welcome message
@app.route("/")
def home():
    return (
        f"Welcome to the Honolulu, Hawaii Climate Analysis API!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Function to get precipitation data
def get_precipitation_data():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precipitation_data = {date: prcp for date, prcp in results}
    return precipitation_data

# Route to get precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(get_precipitation_data())

# Function to get stations
def get_stations():
    results = session.query(Station.station, Station.name).all()
    stations_list = [{"Station": station, "Name": name} for station, name in results]
    return stations_list

# Route to get stations
@app.route("/api/v1.0/stations")
def stations():
    return jsonify(get_stations())

# Function to get temperature observations
def get_temperature_observations():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= prev_year).all()
    temperature_observations = [{"Date": date, "Temperature": tobs} for date, tobs in results]
    return temperature_observations

# Route to get temperature observations
@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(get_temperature_observations())

# Other Flask routes here...

if __name__ == "__main__":
    app.run(debug=True)
