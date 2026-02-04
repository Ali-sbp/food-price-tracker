# Food Price Anomaly Tracker

Mid-level data application that monitors food price anomalies across 5 Russian cities (Moscow, St Petersburg, Novosibirsk, Yekaterinburg, Kazan). Backend provides API endpoints for prices, anomalies, and metadata. Frontend offers a clean, modular React UI. Optional PyQt6 desktop application for local analysis.

## Features

- **5-City Coverage**: Real-time price data for Moscow, St Petersburg, Novosibirsk, Yekaterinburg, and Kazan
- **Multi-Commodity Tracking**: Bread and Milk price monitoring from 2023-2024
- **Anomaly Detection**: Automatic detection of price spikes and irregularities
- **Web Interface**: React-based dashboard with filters, charts, and alerts
- **Desktop Option**: PyQt6 GUI application for local data analysis
- **REST API**: Extensible backend API for custom integrations

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API base: http://localhost:8000/api

Endpoints:
- `GET /api/prices` - Retrieve price data
- `GET /api/anomalies` - Get detected anomalies
- `GET /api/metadata` - System metadata

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Desktop Application (PyQt6)

```bash
cd desktop
python gui.py
```

## Data

- CSV source: `backend/app/data/sample_prices.csv`
- Time range: January 2023 - December 2024
- Update frequency: Monthly data points for each city/commodity
- Ready to integrate with Rosstat/EMISS data feeds

## Architecture

- **backend/**: FastAPI server with price ingestion and anomaly detection
- **frontend/**: React + TypeScript with Vite bundler
- **desktop/**: PyQt6 GUI for standalone analysis
- **api/**: RESTful endpoints for data access

## Notes
- Replace the CSV in backend/app/data with Rosstat/EMISS data when ready.
- UI components are modular; edit files in frontend/src/components for quick customization.
- Desktop app requires PyQt6 library for GUI rendering.
