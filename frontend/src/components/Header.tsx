interface HeaderProps {
  onExport: () => void;
  onCreateAlert: () => void;
}

export const Header = ({ onExport, onCreateAlert }: HeaderProps) => {
  return (
    <header className="app-header">
      <div>
        <p className="eyebrow">Food Price Anomaly Tracker</p>
        <h1>Russia Market Watch</h1>
      </div>
      <div className="header-actions">
        <button className="secondary-button" onClick={onExport}>
          Export Report
        </button>
        <button className="primary-button" onClick={onCreateAlert}>
          Create Alert
        </button>
      </div>
    </header>
  );
};
