import sys
import requests
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QTabWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


API_URL = "http://localhost:8000/api"


class DataFetcher(QThread):
    prices_fetched = pyqtSignal(dict)
    anomalies_fetched = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, endpoint, params):
        super().__init__()
        self.endpoint = endpoint
        self.params = params

    def run(self):
        try:
            resp = requests.get(f"{API_URL}{self.endpoint}", params=self.params, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            if "records" in data:
                self.prices_fetched.emit(data)
            elif "points" in data:
                self.anomalies_fetched.emit(data)
        except Exception as e:
            self.error.emit(str(e))


class FoodPriceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Food Price Anomaly Tracker")
        self.setGeometry(100, 100, 1200, 700)

        self.commodities = []
        self.regions = []
        self.current_prices = {}
        self.current_anomalies = {}

        self.init_ui()
        self.load_metadata()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()

        # Left panel: filters
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Commodity:"))
        self.commodity_combo = QComboBox()
        self.commodity_combo.currentIndexChanged.connect(self.on_selection_changed)
        left_panel.addWidget(self.commodity_combo)

        left_panel.addWidget(QLabel("Region:"))
        self.region_combo = QComboBox()
        self.region_combo.currentIndexChanged.connect(self.on_selection_changed)
        left_panel.addWidget(self.region_combo)

        left_panel.addWidget(QLabel("Window (months):"))
        self.window_spin = QSpinBox()
        self.window_spin.setValue(12)
        self.window_spin.setRange(3, 52)
        left_panel.addWidget(self.window_spin)

        left_panel.addWidget(QLabel("Z-score threshold:"))
        self.z_spin = QDoubleSpinBox()
        self.z_spin.setValue(2.0)
        self.z_spin.setRange(1.0, 5.0)
        self.z_spin.setSingleStep(0.1)
        left_panel.addWidget(self.z_spin)

        fetch_btn = QPushButton("Fetch Data")
        fetch_btn.clicked.connect(self.on_selection_changed)
        left_panel.addWidget(fetch_btn)

        left_panel.addStretch()

        # Right panel: tabs
        tabs = QTabWidget()

        # Prices tab
        prices_widget = QWidget()
        prices_layout = QVBoxLayout()
        self.prices_table = QTableWidget()
        self.prices_table.setColumnCount(5)
        self.prices_table.setHorizontalHeaderLabels(["Date", "Region", "Commodity", "Price", "Unit"])
        prices_layout.addWidget(self.prices_table)
        prices_widget.setLayout(prices_layout)
        tabs.addTab(prices_widget, "Prices")

        # Anomalies tab
        anomalies_widget = QWidget()
        anomalies_layout = QVBoxLayout()
        self.anomalies_table = QTableWidget()
        self.anomalies_table.setColumnCount(4)
        self.anomalies_table.setHorizontalHeaderLabels(["Date", "Price", "Z-Score", "Severity"])
        anomalies_layout.addWidget(self.anomalies_table)
        anomalies_widget.setLayout(anomalies_layout)
        tabs.addTab(anomalies_widget, "Anomalies")

        # Summary tab
        summary_widget = QWidget()
        summary_layout = QVBoxLayout()
        self.summary_label = QLabel()
        self.summary_label.setStyleSheet("font-size: 14px; padding: 10px;")
        summary_layout.addWidget(self.summary_label)
        summary_layout.addStretch()
        summary_widget.setLayout(summary_layout)
        tabs.addTab(summary_widget, "Summary")

        main_layout.addLayout(left_panel, 1)
        main_layout.addWidget(tabs, 3)

        central_widget.setLayout(main_layout)

    def load_metadata(self):
        try:
            commodities_resp = requests.get(f"{API_URL}/commodities", timeout=5)
            self.commodities = commodities_resp.json().get("items", [])
            self.commodity_combo.addItems(self.commodities)

            regions_resp = requests.get(f"{API_URL}/regions", timeout=5)
            self.regions = regions_resp.json().get("items", [])
            self.region_combo.addItems(self.regions)

            summary_resp = requests.get(f"{API_URL}/summary", timeout=5)
            summary_data = summary_resp.json()
            summary_text = "\n".join([f"{card['label']}: {card['value']}" for card in summary_data.get("cards", [])])
            self.summary_label.setText(summary_text)
        except Exception as e:
            self.statusBar().showMessage(f"Error loading metadata: {e}")

    def on_selection_changed(self):
        commodity = self.commodity_combo.currentText()
        region = self.region_combo.currentText()

        if not commodity or not region:
            return

        # Fetch prices
        fetcher = DataFetcher("/prices", {"commodity": commodity, "region": region})
        fetcher.prices_fetched.connect(self.display_prices)
        fetcher.error.connect(lambda msg: self.statusBar().showMessage(f"Error: {msg}"))
        fetcher.start()

        # Fetch anomalies
        fetcher2 = DataFetcher(
            "/anomalies",
            {
                "commodity": commodity,
                "region": region,
                "window": self.window_spin.value(),
                "z": self.z_spin.value(),
            },
        )
        fetcher2.anomalies_fetched.connect(self.display_anomalies)
        fetcher2.error.connect(lambda msg: self.statusBar().showMessage(f"Error: {msg}"))
        fetcher2.start()

    def display_prices(self, data):
        self.prices_table.setRowCount(0)
        for record in data.get("records", []):
            row = self.prices_table.rowCount()
            self.prices_table.insertRow(row)
            self.prices_table.setItem(row, 0, QTableWidgetItem(record["date"]))
            self.prices_table.setItem(row, 1, QTableWidgetItem(record["region"]))
            self.prices_table.setItem(row, 2, QTableWidgetItem(record["commodity"]))
            self.prices_table.setItem(row, 3, QTableWidgetItem(f"{record['price']:.2f}"))
            self.prices_table.setItem(row, 4, QTableWidgetItem(record["unit"]))

    def display_anomalies(self, data):
        self.anomalies_table.setRowCount(0)
        for point in data.get("points", []):
            row = self.anomalies_table.rowCount()
            self.anomalies_table.insertRow(row)
            self.anomalies_table.setItem(row, 0, QTableWidgetItem(point["date"]))
            self.anomalies_table.setItem(row, 1, QTableWidgetItem(f"{point['price']:.2f}"))
            z_score = point["z_score"]
            self.anomalies_table.setItem(row, 2, QTableWidgetItem(f"{z_score:.2f}"))
            severity = "Critical" if abs(z_score) > 3 else ("High" if abs(z_score) > 2 else "Medium")
            self.anomalies_table.setItem(row, 3, QTableWidgetItem(severity))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FoodPriceApp()
    window.show()
    sys.exit(app.exec())
