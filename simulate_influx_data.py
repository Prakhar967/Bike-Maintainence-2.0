import random
import datetime
import time
from influxdb_client import Point, WritePrecision
from connect_influx import client, org, bucket

write_api = client.write_api()

#creating a fleet of bikes
bike_ids = [f"Bike_{i:03}" for i in range(1, 15)]

import random
import time
import datetime
import pandas as pd
from influxdb_client import Point, WritePrecision
from connect_influx import client, org, bucket


CSV_PATH = "bike_predictive_maintenance_balanced.csv"
df = pd.read_csv(CSV_PATH)

RAW_FEATURES = [
    "avg_accel_magnitude",
    "std_accel_magnitude",
    "max_jerk",
    "vibration_index",
    "mean_speed",
    "max_speed",
    "total_distance_m",
    "altitude_gain_m",
    "num_stops",
    "weather",
    "suspicious_flag",
]
df['weather'] = df['weather'].map({'Rainy':0, 'Normal':1,'Hot':2}).astype(int)

good_df = df[df["maintenance_log"] == "Good"]
risky_df = df[df["maintenance_log"].isin(["Tire_Risk", "Brake_Risk", "Multi_Risk"])]

def build_ranges(dataframe, features):
    ranges = {}
    for col in features:
        low = dataframe[col].quantile(0.10)
        high = dataframe[col].quantile(0.90)
        ranges[col] = (low, high)
    return ranges

NORMAL_RANGES = build_ranges(good_df, RAW_FEATURES)
RISKY_RANGES = build_ranges(risky_df, RAW_FEATURES)

write_api = client.write_api()

def generate_bike_data(bike_id):

    health_state = random.choices(["normal", "risky"],weights=[0.8, 0.2],k=1)[0]
    ranges = NORMAL_RANGES if health_state == "normal" else RISKY_RANGES
    values = {feature: random.uniform(*ranges[feature]) for feature in RAW_FEATURES}
    latitude = 26.7606 + random.uniform(-0.01, 0.01)
    longitude = 83.3732 + random.uniform(-0.02, 0.02)
    return (
        Point("bike_metrics")
        .tag("bike_id", bike_id)
        .field("avg_accel_magnitude", values["avg_accel_magnitude"])
        .field("std_accel_magnitude", values["std_accel_magnitude"])
        .field("max_jerk", values["max_jerk"])
        .field("vibration_index", values["vibration_index"])
        .field("mean_speed", values["mean_speed"])
        .field("max_speed", values["max_speed"])
        .field("total_distance_m", values["total_distance_m"])
        .field("altitude_gain_m", values["altitude_gain_m"])
        .field("num_stops", values["num_stops"])
        .field("weather", values["weather"])
        .field("suspicious_flag", values["suspicious_flag"])
        .field("latitude", latitude)
        .field("longitude", longitude)
        .time(datetime.datetime.now(datetime.timezone.utc), WritePrecision.NS)
    )

while True:
    for bike_id in bike_ids:
        point = generate_bike_data(bike_id)
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Sent data for {bike_id}")
    time.sleep(10)
