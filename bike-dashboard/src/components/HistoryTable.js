import React from "react";

function HistoryTable({ data }) {
  return (
    <table className="history-table">
      <thead>
        <tr>
          <th>Bike ID</th>
          <th>Tire Risk</th>
          <th>Brake Risk</th>
          <th>Multi Risk</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {data.length === 0 ? (
          <tr>
            <td colSpan="5">No data available</td>
          </tr>
        ) : (
          data.map((row, index) => (
            <tr key={index}>
              <td>{row.bike_id}</td>
              <td>{row.prob_tire_risk.toFixed(2)}</td>
              <td>{row.prob_brake_risk.toFixed(2)}</td>
              <td>{row.prob_multi_risk.toFixed(2)}</td>
              <td
                style={{
                  color:
                    row.predicted_label === "Tire_Risk"
                      ? "orange"
                      : row.predicted_label === "Brake_Risk"
                      ? "red"
                      : row.predicted_label === "Multi_Risk"
                      ? "purple"
                      : "green",
                }}
              >
                {row.predicted_label}
              </td>
            </tr>
          ))
        )}
      </tbody>
    </table>
  );
}

export default HistoryTable;
