import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return (
        "Aloha! Here are further destinations you can loo through:<br/><br/>"
        "/api/v1.0/precipitation<br/><br/>"
        "/api/v1.0/stations<br/><br/>"
        "/api/v1.0/tobs<br/><br/>"
        "Dates between 2010-01-01 and 2017-08-23<br/><br/>"
        "/api/v1.0/(SET START DATE)<br/><br/>"
        "/api/v1.0/(SET START DATE)/(SET END DATE)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date)

    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)
    
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name, Measurement.station).\
        filter(Station.station == Measurement.station).\
        group_by(Station.name).all()

    station_data = []
    for name, station in results:
        station_dict = {}
        station_dict["name"] = name
        station_dict["station"] = station
        station_data.append(station_dict)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').all()

    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(Measurement.date, func.min(Measurement.tobs).label('min'), func.avg(Measurement.tobs).label('avg'), func.max(Measurement.tobs).label('max')).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()

    start_data = []
    for result in results:
        start_dict = {}
        start_dict['Start Date'] = result[0]
        start_dict['Min Temp'] = result.min
        start_dict['Avg Temp'] = result.avg
        start_dict['Max Temp'] = result.max
        start_data.append(start_dict)
    
    return jsonify(start_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    results = session.query(Measurement.date, func.min(Measurement.tobs).label('min'), func.avg(Measurement.tobs).label('avg'), func.max(Measurement.tobs).label('max')).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()

    start_end_data = []
    for result in results:
        start_end_dict = {}
        start_end_dict['Start Date'] = result[0]
        start_end_dict['Min Temp'] = result.min
        start_end_dict['Avg Temp'] = result.avg
        start_end_dict['Max Temp'] = result.max
        start_end_data.append(start_end_dict)
    
    return jsonify(start_end_data)
    return

if __name__ == "__main__":
    app.run(debug=True)