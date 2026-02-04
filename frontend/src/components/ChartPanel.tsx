interface PriceRecord {
  date: string;
  region: string;
  commodity: string;
  price: number;
  unit: string;
}

interface ChartPanelProps {
  prices: PriceRecord[];
}

export const ChartPanel = (props: ChartPanelProps) => {
  if (!props.prices.length) {
    return (
      <section className="panel chart-panel">
        <div className="panel-header">
          <h2>Price trend</h2>
        </div>
        <div style={{ padding: "20px", textAlign: "center", color: "#999" }}>
          Select filters and click Run Analysis to see data
        </div>
      </section>
    );
  }

  const minPrice = Math.min(...props.prices.map((p) => p.price));
  const maxPrice = Math.max(...props.prices.map((p) => p.price));
  const range = maxPrice - minPrice || 1;
  const avgPrice = (props.prices.reduce((sum, p) => sum + p.price, 0) / props.prices.length).toFixed(2);

  // Generate Y-axis ticks
  const yTicks = [];
  const tickCount = 5;
  for (let i = 0; i <= tickCount; i++) {
    const value = minPrice + (range / tickCount) * i;
    yTicks.push(value.toFixed(1));
  }

  return (
    <section className="panel chart-panel">
      <div className="panel-header">
        <h2>Price trend</h2>
        <div className="pill">
          {props.prices[0]?.commodity} · {props.prices[0]?.region}
        </div>
      </div>
      <div style={{ display: "flex", gap: "12px", height: "280px" }}>
        {/* Y-axis labels */}
        <div style={{ display: "flex", flexDirection: "column", justifyContent: "space-between", width: "40px", textAlign: "right", fontSize: "12px", color: "#999" }}>
          {[...yTicks].reverse().map((tick) => (
            <span key={tick}>{tick}</span>
          ))}
        </div>

        {/* Chart area */}
        <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
          {/* Chart bars */}
          <div style={{ flex: 1, marginBottom: "8px", display: "flex", gap: "6px", alignItems: "flex-end" }}>
            {props.prices.map((price, index) => {
              const normalizedHeight = ((price.price - minPrice) / range) * 100;
              const isAboveAvg = price.price > parseFloat(avgPrice);
              return (
                <div
                  key={index}
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: "4px",
                    flex: 1,
                    height: "100%",
                    justifyContent: "flex-end",
                  }}
                >
                  <span style={{ fontSize: "11px", color: "#666", fontWeight: "500" }}>
                    {price.price.toFixed(1)}
                  </span>
                  <div
                    style={{
                      width: "100%",
                      height: `${Math.max(5, normalizedHeight)}%`,
                      backgroundColor: isAboveAvg ? "#ef4444" : "#3b82f6",
                      borderRadius: "4px 4px 0 0",
                      transition: "background-color 0.2s",
                      minHeight: "5px",
                    }}
                    title={`${price.date}: ${price.price} ${price.unit}`}
                  />
                </div>
              );
            })}
          </div>

          {/* X-axis labels (dates) */}
          <div style={{ display: "flex", gap: "0", height: "24px" }}>
            {props.prices.map((price, index) => {
              const date = new Date(price.date);
              const month = (date.getMonth() + 1).toString().padStart(2, "0");
              const year = date.getFullYear().toString().slice(-2);
              return (
                <div
                  key={index}
                  style={{
                    flex: 1,
                    fontSize: "10px",
                    color: "#999",
                    textAlign: "center",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  {index % Math.ceil(props.prices.length / 6) === 0 ? `${month}/${year}` : ""}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Stats and legend */}
      <div style={{ marginTop: "12px" }}>
        <div style={{ display: "flex", gap: "16px", fontSize: "12px", color: "#666", marginBottom: "8px" }}>
          <span>Min: {minPrice.toFixed(2)}</span>
          <span>Avg: {avgPrice}</span>
          <span>Max: {maxPrice.toFixed(2)}</span>
          <span>{props.prices.length} data points</span>
        </div>
        <div style={{ display: "flex", gap: "16px", fontSize: "12px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <div style={{ width: "16px", height: "16px", backgroundColor: "#3b82f6", borderRadius: "2px" }}></div>
            <span>Below Average</span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <div style={{ width: "16px", height: "16px", backgroundColor: "#ef4444", borderRadius: "2px" }}></div>
            <span>Above Average</span>
          </div>
        </div>
      </div>
    </section>
  );
};
