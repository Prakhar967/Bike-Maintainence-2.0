import React, { useEffect, useState } from "react";
function BikeDetails({ bikeId }) {
  const [details, setDetails] = useState(null);
  useEffect(() => {
    fetch(`http://127.0.0.1:5000/bike_details/${bikeId}`)
      .then(res => res.json())
      .then(data => setDetails(data));
  }, [bikeId]);
  if (!details) return <p>Loading bike details...</p>;
  return (
    <div style={{ padding: "20px" }}>
      <h2>Bike Details: {bikeId}</h2>
      <div className="card">
        <p><strong>Status:</strong> {details.status}</p>
        <p><strong>Tire Risk:</strong> {details.tire_risk}</p>
        <p><strong>Brake Risk:</strong> {details.brake_risk}</p>
        <p><strong>Multi Risk Score:</strong> {details.multi_risk}</p>
        <p><strong>Total Distance:</strong> {details.total_distance_m} m</p>
        <p><strong>Average Speed:</strong> {details.mean_speed} km/h</p>
        <p><strong>Vibration Index:</strong> {details.vibration_index}</p>
        <p><strong>Jerk Value:</strong> {details.max_jerk}</p>
        <p><strong>Health:</strong> {details.health_status}</p>
      </div>
      <h3>Ride History</h3>
      <table className="history-table">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Speed</th>
            <th>Distance</th>
            <th>Stops</th>
          </tr>
        </thead>
        <tbody>
          {details.history.map((ride, idx) => (
            <tr key={idx}>
              <td>{ride.timestamp}</td>
              <td>{ride.speed}</td>
              <td>{ride.distance}</td>
              <td>{ride.stops}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
export default BikeDetails;