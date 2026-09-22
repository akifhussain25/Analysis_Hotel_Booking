# -*- coding: utf-8 -*-
"""
app.py  —  Hotel Booking Analysis · Application Entry Point
============================================================
Run:
    python app.py

Opens http://127.0.0.1:8050 automatically in your default browser.

Project layout
--------------
hotel_bookings.csv/          ← project root (this file lives here)
├── app.py                   ← YOU ARE HERE — run this to start the app
├── dashboard.py             ← original standalone dashboard (untouched)
├── hotel_bookings.csv       ← raw dataset (never modified)
├── hotel_bookings_cleaned.csv
├── clean_hotel_bookings.py
├── eda_hotel_bookings.py
├── visualize_hotel_bookings.py
├── charts/                  ← static chart PNGs
└── frontend/                ← modular app package
    ├── __init__.py
    ├── data.py              ← data loading, palette, shared helpers
    ├── layout.py            ← Dash HTML layout tree
    └── callbacks.py         ← all Dash callbacks
"""

import threading
import webbrowser

from dash import Dash

from frontend.layout import build_layout
from frontend.callbacks import register_callbacks

# ─────────────────────────────────────────────────────────────────────────────
# Build the app
# ─────────────────────────────────────────────────────────────────────────────
app = Dash(
    __name__,
    title="Hotel Booking Dashboard",
)

app.layout = build_layout()
register_callbacks(app)

# ─────────────────────────────────────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────────────────────────────────────
HOST = "127.0.0.1"
PORT = 8050
URL  = f"http://{HOST}:{PORT}"

if __name__ == "__main__":
    # Schedule browser open 1.5 s after server starts (server needs to bind first)
    threading.Timer(1.5, lambda: webbrowser.open(URL)).start()

    print("=" * 55)
    print("  Hotel Booking Analysis Dashboard")
    print(f"  Opening {URL} in your browser ...")
    print("  Press Ctrl+C to stop the server.")
    print("=" * 55)

    app.run(debug=False, host=HOST, port=PORT)
