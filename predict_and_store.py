import pandas as pd
import numpy as np
import psycopg2
import joblib,pickle
from connect_influx import client

query_api = client.query_api()

query = '''
from(bucket: "BikeData")
  |> range(start: -1m)
  |> filter(fn: (r) => r._measurement == "bike_metrics")
  |> group(columns: ["bike_id"])
  |> map(fn: (r) => ({ r with _value: float(v: r._value) }))
  |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> keep(columns: ["_time", "bike_id", "avg_accel_magnitude", "std_accel_magnitude", "max_jerk",
                    "vibration_index", "mean_speed", "max_speed", "total_distance_m",
                    "altitude_gain_m", "num_stops", "weather", "suspicious_flag",
                    "latitude","longitude"])
  |> sort(columns: ["_time"], desc: false)
'''

result = query_api.query_data_frame(query)

# Columns that is to be used for running the model and predicting
feature_cols = [ "avg_accel_magnitude", "std_accel_magnitude", "max_jerk",
                "vibration_index", "mean_speed", "max_speed", "total_distance_m",
                 "altitude_gain_m", "num_stops", "weather", "suspicious_flag",
                ]
df = result[feature_cols].copy()

df['speed_variability'] = df['std_accel_magnitude'] / (df['mean_speed'] + 1e-5)
df['vibration_to_speed_ratio'] = df['vibration_index'] / (df['mean_speed'] + 1e-5)
df['stops_per_km'] = df['num_stops'] / ((df['total_distance_m'] / 1000) + 1e-5)
df['altitude_rate'] = df['altitude_gain_m'] / (df['total_distance_m'] + 1e-5)

#Loading the trained model
model = joblib.load('xgb_best_model.joblib')

X = df.astype(float).to_numpy()

pred_classes = model.predict(X)
pred_probs = model.predict_proba(X)


import json
with open("class_names_new.json","r") as f:
    class_names = json.load(f)

df["predicted_class"] = [class_names[i] for i in pred_classes]
for i, name in enumerate(class_names):
    df[f"prob_{name.lower()}"] = pred_probs[:, i]


df['bike_id'] = result['bike_id'].values
df['_time'] = result['_time'].values
df['latitude'] = result['latitude'].values
df['longitude'] = result['longitude'].values

print(df.info())

# Connecting the data to Postgres SQL
conn = psycopg2.connect(host="localhost",database = "bike_maintenance",user = "postgres",password = "prashiasthana"
                        , port = "5432")
cur = conn.cursor()


#Storing the data in bike_sensor_data
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO bike_sensor_data (
            bike_id, avg_accel_magnitude, std_accel_magnitude, max_jerk,
            vibration_index, mean_speed, max_speed, total_distance_m,
            altitude_gain_m, num_stops, weather, suspicious_flag,
            speed_variability, vibration_to_speed_ratio, stops_per_km,
            altitude_rate, maintenance_log, sensor_timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (bike_id, sensor_timestamp) DO NOTHING;
    """, (
        row["bike_id"], row["avg_accel_magnitude"], row["std_accel_magnitude"], row["max_jerk"],
        row["vibration_index"], row["mean_speed"], row["max_speed"], row["total_distance_m"],
        row["altitude_gain_m"], row["num_stops"], row["weather"], row["suspicious_flag"],
        row["speed_variability"], row["vibration_to_speed_ratio"], row["stops_per_km"],
        row["altitude_rate"], row['predicted_class'], row["_time"]
    ))

conn.commit()

# storing the data in bike_prediction data
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO bike_predictions (bike_id,sensor_timestamp,predicted_label,prob_good,prob_tire_risk,
            prob_brake_risk,prob_multi_risk,latitude,longitude
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)
        ON CONFLICT (bike_id, sensor_timestamp) DO NOTHING;
    """, (
        row['bike_id'],row['_time'],str(row['predicted_class']),  float(row['prob_good']),float(row['prob_tire_risk']),
        float(row['prob_brake_risk']),float(row['prob_multi_risk']),float(row['latitude']),float(row['longitude'])
    ))
conn.commit()
cur.close()
conn.close()







