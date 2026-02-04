import { useState, useEffect } from "react";
import "./styles/app.css";
import { Header } from "./components/Header";
import { FiltersPanel } from "./components/FiltersPanel";
import { MapPanel } from "./components/MapPanel";
import { ChartPanel } from "./components/ChartPanel";
import { AlertsPanel } from "./components/AlertsPanel";
import { SummaryCards } from "./components/SummaryCards";

const API_URL = "/api";

interface PriceRecord {
  date: string;
  region: string;
  commodity: string;
  price: number;
  unit: string;
}

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

const App = () => {
  const [commodities, setCommodities] = useState<string[]>([]);
  const [regions, setRegions] = useState<string[]>([]);
  const [selectedCommodity, setSelectedCommodity] = useState("Bread");
  const [selectedRegion, setSelectedRegion] = useState("Moscow");
  const [window, setWindow] = useState(12);
  const [zThreshold, setZThreshold] = useState(2.0);
  const [prices, setPrices] = useState<PriceRecord[]>([]);
  const [anomalies, setAnomalies] = useState<AnomalyPoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [userAlerts, setUserAlerts] = useState<UserAlert[]>(() => {
    try {
      const saved = localStorage.getItem('userAlerts');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  // Calculate latest date from prices
  const latestDate = prices.length > 0
    ? new Date(prices[prices.length - 1].date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    : 'No data';

  const exportData = () => {
    if (prices.length === 0) {
      alert('No data to export. Please run an analysis first.');
      return;
    }

    const csv = [
      ['Date', 'Region', 'Commodity', 'Price', 'Unit', 'Is Anomaly', 'Z-Score'].join(','),
      ...prices.map(p => {
        const anomaly = anomalies.find(a => a.date === p.date);
        return [
          p.date,
          p.region,
          p.commodity,
          p.price,
          p.unit,
          anomaly ? 'Yes' : 'No',
          anomaly ? anomaly.z_score.toFixed(2) : ''
        ].join(',');
      })
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `price-analysis-${selectedCommodity}-${selectedRegion}-${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const createAlert = () => {
    const threshold = prompt(
      `Create alert for ${selectedCommodity} in ${selectedRegion}\n\nEnter price threshold (current range: ${prices.length > 0 ? `${Math.min(...prices.map(p => p.price)).toFixed(2)} - ${Math.max(...prices.map(p => p.price)).toFixed(2)}` : 'N/A'}):`,
      prices.length > 0 ? Math.max(...prices.map(p => p.price)).toFixed(2) : ''
    );

    if (threshold && !isNaN(parseFloat(threshold))) {
      const newAlert: UserAlert = {
        id: Date.now().toString(),
        commodity: selectedCommodity,
        region: selectedRegion,
        threshold: parseFloat(threshold),
        createdAt: new Date().toLocaleDateString()
      };
      const updatedAlerts = [...userAlerts, newAlert];
      setUserAlerts(updatedAlerts);
      localStorage.setItem('userAlerts', JSON.stringify(updatedAlerts));
      alert(`✅ Alert created for ${selectedCommodity} in ${selectedRegion} at ${parseFloat(threshold).toFixed(2)} RUB`);
    }
  };

  const deleteUserAlert = (alertId: string) => {
    const updatedAlerts = userAlerts.filter(a => a.id !== alertId);
    setUserAlerts(updatedAlerts);
    localStorage.setItem('userAlerts', JSON.stringify(updatedAlerts));
  };

  // Load metadata
  useEffect(() => {
    Promise.all([
      fetch(`${API_URL}/commodities`).then((r) => r.json()),
      fetch(`${API_URL}/regions`).then((r) => r.json()),
    ])
      .then(([comData, regData]) => {
        console.log("Loaded commodities:", comData);
        console.log("Loaded regions:", regData);
        setCommodities(comData.items || []);
        setRegions(regData.items || []);
        if (comData.items?.length) setSelectedCommodity(comData.items[0]);
        if (regData.items?.length) setSelectedRegion(regData.items[0]);
      })
      .catch((err) => console.error("Error loading metadata:", err));
  }, []);

  const runAnalysis = async () => {
    setLoading(true);
    try {
      const [priceRes, anomalRes] = await Promise.all([
        fetch(
          `${API_URL}/prices?commodity=${selectedCommodity}&region=${selectedRegion}&window=${window}`
        ),
        fetch(
          `${API_URL}/anomalies?commodity=${selectedCommodity}&region=${selectedRegion}&window=${window}&z=${zThreshold}`
        ),
      ]);

      if (priceRes.ok) {
        const priceData = await priceRes.json();
        setPrices(priceData.records || []);
      }
      if (anomalRes.ok) {
        const anomalyData = await anomalRes.json();
        setAnomalies(anomalyData.points || []);
      }
    } catch (err) {
      console.error("Error running analysis:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <Header onExport={exportData} onCreateAlert={createAlert} />
      <main className="app-main">
        <SummaryCards
          latestDate={latestDate}
          commoditiesCount={commodities.length}
          regionsCount={regions.length}
          activeAlerts={userAlerts.length}
        />
        <div className="content-grid">
          <FiltersPanel
            commodities={commodities}
            regions={regions}
            selectedCommodity={selectedCommodity}
            selectedRegion={selectedRegion}
            window={window}
            zThreshold={zThreshold}
            onCommodityChange={setSelectedCommodity}
            onRegionChange={setSelectedRegion}
            onWindowChange={setWindow}
            onZThresholdChange={setZThreshold}
            onRunAnalysis={runAnalysis}
            loading={loading}
          />
          <div className="center-stack">
            <MapPanel selectedCommodity={selectedCommodity} selectedRegion={selectedRegion} prices={prices} />
            <ChartPanel prices={prices} />
          </div>
          <AlertsPanel anomalies={anomalies} userAlerts={userAlerts} onDeleteAlert={deleteUserAlert} />
        </div>
      </main>
    </div>
  );
};

export default App;
