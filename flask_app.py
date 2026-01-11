from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS


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



if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5001,debug=True)



