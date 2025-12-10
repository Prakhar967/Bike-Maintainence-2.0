from influxdb_client import InfluxDBClient

token = "PeVQKxRnLdwuLsA2E0nG9hUvVzgVeBL2th1giZD_e-XsYcKFFPbGlyjWvV1sctlxNgcggQNJ9YA_hJ3Y_sG73w=="
org = "bike_org"
bucket = "BikeData"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)

health = client.health()
print(f"InfluxDB Health: {health.status}")