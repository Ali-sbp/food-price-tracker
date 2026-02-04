interface AnomalyPoint {
  date: string;
  price: number;
  z_score: number;
}

interface UserAlert {
  id: string;
  commodity: string;
  region: string;
  threshold: number;
  createdAt: string;
}

interface AlertsPanelProps {
  anomalies: AnomalyPoint[];
  userAlerts: UserAlert[];
  onDeleteAlert: (alertId: string) => void;
}

export const AlertsPanel = (props: AlertsPanelProps) => {
  return (
    <aside className="panel alerts-panel">
      <div className="panel-header">
        <h2>Your Alerts</h2>
        <div className="pill">{props.userAlerts.length > 0 ? props.userAlerts.length : "None"}</div>
      </div>
      <ul>
        {props.userAlerts.length === 0 ? (
          <li style={{ color: "#94a3b8", padding: "20px", textAlign: "center", fontSize: "14px" }}>
            📢 No alerts created yet
          </li>
        ) : (
          props.userAlerts.map((alert) => (
            <li
              key={alert.id}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "12px",
                borderLeft: "3px solid #3b82f6",
                marginBottom: "8px",
              }}
            >
              <div style={{ flex: 1 }}>
                <strong>
                  {alert.commodity} - {alert.region}
                </strong>
                <div style={{ fontSize: "12px", color: "#94a3b8", marginTop: "4px" }}>
                  🔔 Threshold: {alert.threshold.toFixed(2)} RUB
                </div>
                <div style={{ fontSize: "11px", color: "#64748b", marginTop: "2px" }}>
                  Created: {alert.createdAt}
                </div>
              </div>
              <button
                onClick={() => props.onDeleteAlert(alert.id)}
                style={{
                  background: "none",
                  border: "none",
                  color: "#ef4444",
                  cursor: "pointer",
                  fontSize: "18px",
                  padding: "4px 8px",
                }}
                title="Delete alert"
              >
                ✕
              </button>
            </li>
          ))
        )}
      </ul>
    </aside>
  );
};
