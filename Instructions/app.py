import datetime as dt
import numpy as np
import pandas as pdimport
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# db Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect=True)

measurement = base.classes.measurement
station = base.classes.station

# flask setup
app = Flask(__name__)


#############################################
# /api/v1.0/precipitation
#############################################

@app.route("/")
def welcome():
    return("Available Routes:<br/> /api/v1.0/precipitation <br />/api/v1.0/tobs <br /> /api/v1.0/<start> <br /> /api/v1.0/<start>/<end>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)    
    
    precip_results = session.query(measurement.date, measurement.prcp).all()
    
    session.close()
    
    all_dates_prcp = []
    for date, prcp in precip_results:
        precip_data_dict = {}
        precip_data_dict["date"] = date
        precip_data_dict["prcp"] = prcp
        all_dates_prcp.append(precip_data_dict)
    return jsonify(all_dates_prcp)

#############################################
# /api/v1.0/tobs
#############################################

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    #Define One year ago
    one_yr_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)
    
    #Define most active station
    most_active_st = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station)\
                                                    .order_by(func.count(measurement.station).desc()).limit(1).all()

    #Generate results
    tobs_results = session.query(measurement.date, measurement.tobs).filter(measurement.station == most_active_st[0][0]).filter(measurement.date >= one_yr_ago).all()
    
    most_active_tobs_oneYear = []
    for date, tobs in tobs_results:
        tobs_data_dict = {}
        tobs_data_dict["date"] = date
        tobs_data_dict["tobs"] = tobs
        most_active_tobs_oneYear.append(tobs_data_dict)
    return jsonify(most_active_tobs_oneYear)

#############################################
# /api/v1.0/<start>
#############################################

@app.route("/api/v1.0/<start>")
def start_only(start):
    session = Session(engine)
    
    date_tobs = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).filter(measurement.date >= start).all()  
                                              
    
    return jsonify(date_tobs)


#############################################
# /api/v1.0/<start>/<end>
#############################################

@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start,end):
    session = Session(engine)
    
    date_tobs = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()  
                                              
    
    return jsonify(date_tobs)
if __name__ == '__main__':
    app.run(debug=False)




