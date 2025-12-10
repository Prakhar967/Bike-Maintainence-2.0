import random
import datetime
import time
from influxdb_client import Point, WritePrecision
from connect_influx import client, org, bucket

write_api = client.write_api()

#creating a fleet of bikes
bike_ids = [f"Bike_{i:03}" for i in range(1, 21)]

def generate_bike_data(bike_id):
    weather_map = {"Rainy": 0, "Normal": 1, "Hot": 2}
    weather_value = random.choice(list(weather_map.values()))
    latitude = 26.7606 + random.uniform(-.01,.01)
    longitude =83.3732 + random.uniform(-.02,.02)

    return Point("bike_metrics") \
        .tag("bike_id", bike_id) \
        .field("avg_accel_magnitude", float(random.uniform(0.1, 2.0))) \
        .field("std_accel_magnitude", float(random.uniform(0.05, 0.5))) \
        .field("max_jerk", float(random.uniform(1.0, 5.0))) \
        .field("vibration_index", float(random.uniform(0.5, 4.0))) \
        .field("mean_speed", float(random.uniform(20, 80))) \
        .field("max_speed", float(random.uniform(40, 100))) \
        .field("total_distance_m", float(random.uniform(1000, 50000))) \
        .field("altitude_gain_m", float(random.uniform(0, 500))) \
        .field("num_stops", float(random.randint(0, 20))) \
        .field("weather", float(weather_value)) \
        .field("suspicious_flag", float(random.randint(0, 1))) \
        .field("speed_variability", float(random.uniform(0.0, 1.0))) \
        .field("vibration_to_speed_ratio", float(random.uniform(0.01, 0.3))) \
        .field("stops_per_km", float(random.uniform(0.0, 2.0))) \
        .field("altitude_rate", float(random.uniform(0.0, 10.0))) \
        .field("latitude",latitude) \
        .field("longitude",longitude) \
        .time(datetime.datetime.now(datetime.timezone.utc), WritePrecision.NS)


while True:
    for bike_id in bike_ids:
        point = generate_bike_data(bike_id)
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Data written for {bike_id}")
    time.sleep(10)
