import breadImg from "../assets/bread.jpg";
import milkImg from "../assets/milk.jpg";
import eggsImg from "../assets/eggs.jpg";
import tomatoesImg from "../assets/tomatoes.jpg";
import cucumbersImg from "../assets/cucumbers.jpg";
import bananasImg from "../assets/bananas.jpg";
import chickenImg from "../assets/chicken.jpg";
import moscowImg from "../assets/moscow.jpg";
import stpetersburgImg from "../assets/stpetersburg.jpg";
import novosibirskImg from "../assets/novosibirsk.jpg";
import yekaterinburgImg from "../assets/yekaterinburg.jpg";
import kazanImg from "../assets/kazan.jpg";

interface MapPanelProps {
  selectedCommodity: string;
  selectedRegion: string;
  prices: Array<{ date: string; region: string; commodity: string; price: number; unit: string }>;
}

const COMMODITY_IMAGES: Record<string, string> = {
  Bread: breadImg,
  Milk: milkImg,
  Eggs: eggsImg,
  Tomatoes: tomatoesImg,
  Cucumbers: cucumbersImg,
  Bananas: bananasImg,
  "Chicken Breast": chickenImg,
};

const CITY_IMAGES: Record<string, string> = {
  Moscow: moscowImg,
  "St. Petersburg": stpetersburgImg,
  Novosibirsk: novosibirskImg,
  Yekaterinburg: yekaterinburgImg,
  Kazan: kazanImg,
};

const CITY_COLORS: Record<string, string> = {
  Moscow: "#ef4444",
  "St. Petersburg": "#f97316",
  Novosibirsk: "#eab308",
  Yekaterinburg: "#06b6d4",
  Kazan: "#8b5cf6",
};

const getSeverityColor = (price: number, minPrice: number, maxPrice: number): string => {
  if (minPrice === maxPrice) return "#22c55e";
  const ratio = (price - minPrice) / (maxPrice - minPrice);
  if (ratio > 0.75) return "#ef4444"; // Critical
  if (ratio > 0.5) return "#f97316"; // High
  if (ratio > 0.25) return "#eab308"; // Medium
  return "#22c55e"; // Normal
};

export const MapPanel = ({ selectedCommodity, selectedRegion, prices }: MapPanelProps) => {
  const commodityImage = COMMODITY_IMAGES[selectedCommodity] || breadImg;
  const cityImage = CITY_IMAGES[selectedRegion] || moscowImg;
  const cityColor = CITY_COLORS[selectedRegion] || "#0f172a";

  // Get unique regions from prices data
  const regions = [...new Set(prices.map(p => p.region))];
  const minPrice = prices.length > 0 ? Math.min(...prices.map(p => p.price)) : 0;
  const maxPrice = prices.length > 0 ? Math.max(...prices.map(p => p.price)) : 100;

  // Get latest price for each region
  const latestByRegion = regions.map(region => {
    const regionPrices = prices.filter(p => p.region === region).sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    return regionPrices[0] || null;
  }).filter(Boolean);

  return (
    <section className="panel map-panel">
      <div className="panel-header">
        <h2>Market Preview</h2>
        <div className="pill">{selectedCommodity} in {selectedRegion}</div>
      </div>
      <div style={{ display: "flex", gap: "20px", justifyContent: "center", alignItems: "center", padding: "32px 24px", flexWrap: "wrap" }}>
        <div style={{ textAlign: "center" }}>
          <img
            src={commodityImage}
            alt={selectedCommodity}
            style={{
              width: "140px",
              height: "140px",
              borderRadius: "12px",
              objectFit: "cover",
              boxShadow: "0 8px 20px rgba(0, 0, 0, 0.15)",
            }}
          />
          <p style={{ marginTop: "12px", fontSize: "14px", fontWeight: "600", color: "#0f172a" }}>
            {selectedCommodity}
          </p>
        </div>
        <div style={{ fontSize: "32px", color: "#cbd5e1", fontWeight: "300" }}>→</div>
        <div style={{ textAlign: "center" }}>
          <img
            src={cityImage}
            alt={selectedRegion}
            style={{
              width: "140px",
              height: "140px",
              borderRadius: "12px",
              objectFit: "cover",
              boxShadow: "0 8px 20px rgba(0, 0, 0, 0.15)",
            }}
          />
          <p style={{ marginTop: "12px", fontSize: "14px", fontWeight: "600", color: "#0f172a" }}>
            {selectedRegion}
          </p>
        </div>
      </div>

      <div style={{ marginTop: "24px", padding: "16px" }}>
        <h3 style={{ fontSize: "14px", fontWeight: "600", marginBottom: "12px", color: "#0f172a" }}>
          Price Heatmap: {selectedCommodity} Across Regions
        </h3>
        {latestByRegion.length === 0 ? (
          <p style={{ textAlign: "center", color: "#94a3b8", fontSize: "12px", padding: "16px" }}>
            💡 Run analysis to see heatmap
          </p>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            {latestByRegion.map((priceData) => (
              <div key={priceData.region} style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <div style={{ width: "90px", fontSize: "12px", fontWeight: "500", color: "#0f172a" }}>
                  {priceData.region}
                </div>
                <div
                  style={{
                    flex: 1,
                    height: "32px",
                    borderRadius: "6px",
                    background: getSeverityColor(priceData.price, minPrice, maxPrice),
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "white",
                    fontSize: "12px",
                    fontWeight: "600",
                    transition: "all 0.2s ease",
                  }}
                  title={`${priceData.price.toFixed(2)} RUB - Last: ${priceData.date}`}
                >
                  {priceData.price.toFixed(2)} RUB
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
};
