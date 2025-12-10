import React, { useEffect, useState } from "react";
import HistoryTable from "./HistoryTable";
import BikeMap from "./BikeMap";

function Dashboard() {
  const [data, setData] = useState([]);

  // Fetch data from Flask
  useEffect(() => {
    fetch("http://127.0.0.1:5000/sensor_data")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <div className="dashboard-container">
      <div className="section">
        <h2>Maintenance Records</h2>
        <HistoryTable data={data} />
      </div>

      <div className="section">
        <h2>Route Optimization (Map)</h2>
        <BikeMap bikes={data} />
      </div>
    </div>
  );
}

export default Dashboard;
