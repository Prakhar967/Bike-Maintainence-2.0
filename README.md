# Predictive Bike Maintenance Dashboard

## **Project Overview**
Building a data-driven system to predict component-specific failures (e.g., brakes, tires, 
chains) in a public bike-sharing fleet, enabling efficient, preventive maintenance and improving bike 
availability and safety. 

## **Tech Stack**

### Backend
- Python
- Flask REST API
- PostgreSQL for structured storage of bike metadata and maintenance records
- InfluxDB for time-series sensor data such as vibration, speed, and accelerometer values
- Pandas and NumPy for data processing
- Geopy for distance calculations

### Frontend
- React JS
- Leaflet JS for interactive map rendering
- Axios for API communication

## **Features Implemented**

### Real-Time Bike Location Tracking
- Displays each bike as a marker on the map.
- Shows bike ID, predicted maintenance status, tire risk score, brake risk score, multi-risk score, and overall health category.
- Health categories include Critical, Warning, and Good.

### Risk Prediction and Prioritization
- Each bike is assigned risk levels based on ML-predicted component failure probabilities.
- Bikes are categorized into priority groups to help maintenance teams identify which bikes require immediate attention.

### Maintenance History Table
- Shows historical maintenance information retrieved from PostgreSQL.
- Includes bike ID, risk assessments, and previous service results.

### InfluxDB Integration
- Stores time-series sensor data such as vibration, GPS coordinates, and accelerometer signals.
- Enables real-time feature engineering and historical trend analysis.
- Allows future expansion into live IoT-based predictive maintenance pipelines.

---

## **How to Run the Project**

### 1. Start InfluxDB
- Ensure InfluxDB is installed and running locally.
- open terminal and write influxd to start the influxdb server
- Access the UI at: http://localhost:8086
- signin username : Prakhar
- signin password : prashiasthana
- Create the bucket required for sensor data storage.

### 2. Run postgre SQL
  - install postgreSQL
  - Create a new Database after all the prerequisite setup
  - open the newly created database
  - click on the query tool
  - click on open file
  - select **.SQL** database file that i have provided in github
  - click on execute

### 3. Start the Backend (Flask API)
Run the following command inside the backend folder: python flask_app.py

### 4. Start the Frontend (React)
start the frontend :
- cd bike-dashboard
- npm install
- npm start

## Improvements to be done
  - In the Bike Maintenance System, I wanted to implement the routing algorithm properly so the maintenance crew gets the correct order of bikes to visit. I started it, but the dataset had too many critical bikes and time was less, so the routing was not completed. This will be improved later.
    
## Author
- Prakhar Asthana
