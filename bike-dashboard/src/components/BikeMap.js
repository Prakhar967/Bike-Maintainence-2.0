import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function BikeMap({ bikes }) {
  // Center of Gorakhpur
  const gorakhpurCenter = [26.7606, 83.3732];

  // Route state
  const [route, setRoute] = useState([]);

  // Load optimized route from Flask backend
  useEffect(() => {
    fetch("http://127.0.0.1:5000/simple_route")
      .then((res) => res.json())
      .then((data) => {
        if (data.route) {
          const fullPath = [
            [data.start_point.lat, data.start_point.lon],
            ...data.route.map((r) => [r.lat, r.lon])
          ];
          setRoute(fullPath);
        }
      })
      .catch((err) => console.log("Route Fetch Error:", err));
  }, []);

  return (
    <div>
      <h2 style={{ textAlign: "center", marginBottom: "10px" }}>
        Real-Time Bike Map (Gorakhpur) + Maintenance Route
      </h2>

      {/* Full-width wrapper */}
      <div style={{ width: "100vw", marginLeft: "calc(-50vw + 50%)" }}>
        <MapContainer
          center={gorakhpurCenter}
          zoom={13}
          style={{ height: "600px", width: "100%" }}
        >
          {/* Base Map Layer */}
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="© OpenStreetMap contributors"
          />

          {/* Draw Route Polyline */}
          {route.length > 1 && (
            <Polyline
              positions={route}
              pathOptions={{ color: "blue", weight: 4 }}
            />
          )}

          {/* Plot All Bikes */}
          {bikes.map((bike, index) => (
            <Marker key={index} position={[bike.latitude, bike.longitude]}>
              <Popup>
                <b>Bike ID:</b> {bike.bike_id} <br />
                <b>Status:</b> {bike.predicted_label} <br />
                <b>Tire Risk:</b> {bike.prob_tire_risk.toFixed(2)} <br />
                <b>Brake Risk:</b> {bike.prob_brake_risk.toFixed(2)} <br />
                <b>Multi Risk:</b> {bike.prob_multi_risk.toFixed(2)} <br />
                <b>Health:</b>{" "}
                <span
                  style={{
                    color:
                      bike.health_status === "Critical"
                        ? "red"
                        : bike.health_status === "Warning"
                        ? "orange"
                        : "green",
                    fontWeight: "bold"
                  }}
                >
                  {bike.health_status}
                </span>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}

export default BikeMap;
