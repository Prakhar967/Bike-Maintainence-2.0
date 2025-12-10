from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(host = "localhost",database = "bike_maintenance",user = "postgres",
                        password = "prashiasthana", port = "5432")

@app.route('/')
def home():
    return jsonify({"message": "Flask connected successfully to Postgres SQL"})
@app.route("/sensor_data")
def sensor_data():
    cur = conn.cursor()
    cur.execute("""
            SELECT DISTINCT on (bike_id)
            bike_id, predicted_label,prob_tire_risk,prob_brake_risk,prob_multi_risk,latitude,longitude
            FROM bike_predictions
            ORDER BY bike_id, sensor_timestamp DESC; 
                """)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    data = [dict(zip(columns, row)) for row in rows]


    for row in data:
        max_prob = max(row['prob_tire_risk'],row['prob_brake_risk'],row['prob_multi_risk'])
        row['health_status'] = (
            "Critical" if max_prob > 0.8 else
            "Warning" if max_prob > 0.5 else
            "Good"
        )
    cur.close()
    return jsonify(data)


def distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))


# -----------to do later----------------
# @app.route("/simple_route")
# def simple_route():
#     # Maintenance center (fixed)
#     maintenance_center = {
#         "lat": 26.7606,
#         "lon": 83.3732,
#         "name": "Maintenance Hub"
#     }
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT bike_id, latitude, longitude
#         FROM bike_predictions
#         WHERE predicted_label != 'Good'
#     """)
#     rows = cur.fetchall()
#
#     bikes = [{"bike_id": r[0], "lat": float(r[1]), "lon": float(r[2])} for r in rows]
#     route = []
#     current_lat = maintenance_center["lat"]
#     current_lon = maintenance_center["lon"]
#     while bikes:
#         nearest = min(
#             bikes,
#             key=lambda b: distance(current_lat, current_lon, b["lat"], b["lon"])
#         )
#         route.append({
#             "bike_id": nearest["bike_id"],
#             "lat": nearest["lat"],
#             "lon": nearest["lon"],
#             "stay_minutes": 10
#         })
#         current_lat = nearest["lat"]
#         current_lon = nearest["lon"]
#         bikes.remove(nearest)
#     return jsonify({
#         "start_point": maintenance_center,
#         "route": route
#     })


if __name__ == "__main__":
    app.run(debug=True)



