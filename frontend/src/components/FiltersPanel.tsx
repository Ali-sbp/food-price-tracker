interface FiltersPanelProps {
  commodities: string[];
  regions: string[];
  selectedCommodity: string;
  selectedRegion: string;
  window: number;
  zThreshold: number;
  onCommodityChange: (v: string) => void;
  onRegionChange: (v: string) => void;
  onWindowChange: (v: number) => void;
  onZThresholdChange: (v: number) => void;
  onRunAnalysis: () => void;
  loading: boolean;
}

export const FiltersPanel = (props: FiltersPanelProps) => {
  return (
    <aside className="panel filters-panel">
      <h2>Filters</h2>
      <label>
        Commodity
        <select 
          value={props.selectedCommodity} 
          onChange={(e) => props.onCommodityChange(e.target.value)}
          disabled={props.commodities.length === 0}
        >
          {props.commodities.length === 0 ? (
            <option value="">Loading...</option>
          ) : (
            props.commodities.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))
          )}
        </select>
      </label>
      <label>
        Region
        <select 
          value={props.selectedRegion} 
          onChange={(e) => props.onRegionChange(e.target.value)}
          disabled={props.regions.length === 0}
        >
          {props.regions.length === 0 ? (
            <option value="">Loading...</option>
          ) : (
            props.regions.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))
          )}
        </select>
      </label>
      <label>
        Time window (months)
        <input
          type="number"
          min={3}
          max={24}
          value={props.window}
          onChange={(e) => props.onWindowChange(Number(e.target.value))}
        />
      </label>
      <label>
        Z-score threshold
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <input
            type="range"
            min={1}
            max={5}
            step={0.1}
            value={props.zThreshold}
            onChange={(e) => props.onZThresholdChange(Number(e.target.value))}
          />
          <span>{props.zThreshold.toFixed(1)}</span>
        </div>
      </label>
      <button
        className="primary-button"
        onClick={props.onRunAnalysis}
        disabled={props.loading || props.commodities.length === 0}
        style={{ opacity: props.loading || props.commodities.length === 0 ? 0.6 : 1 }}
      >
        {props.loading ? "Analyzing..." : "Run Analysis"}
      </button>
    </aside>
  );
};
