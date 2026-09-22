"""
frontend/data.py
================
Loads hotel_bookings_cleaned.csv and exposes the shared DataFrame,
constants, colour palette, and helper functions used across the app.
The CSV path is resolved relative to the project root (parent of this file).
"""

import pathlib
import pandas as pd

# ── Resolve CSV path from project root ───────────────────────────────────────
_ROOT = pathlib.Path(__file__).parent.parent          # project root
DATA_FILE = _ROOT / "hotel_bookings_cleaned.csv"

# ── Load & enrich ─────────────────────────────────────────────────────────────
df_full = pd.read_csv(DATA_FILE, low_memory=False)
df_full["total_nights"] = (
    df_full["stays_in_weekend_nights"] + df_full["stays_in_week_nights"]
)

# ── Dimension constants ───────────────────────────────────────────────────────
MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
HOTEL_TYPES = ["All"] + sorted(df_full["hotel"].unique().tolist())
YEARS       = ["All"] + sorted(df_full["arrival_date_year"].unique().tolist())

# ── Colour palette ────────────────────────────────────────────────────────────
C_BLUE   = "#3B82D4"
C_PURPLE = "#7C5CD8"
C_RED    = "#E05252"
C_GREEN  = "#3BA876"
C_AMBER  = "#F59E0B"
C_BG     = "#F7F8FA"
C_CARD   = "#FFFFFF"
C_BORDER = "#E5E7EB"
C_TEXT   = "#1F2328"
C_MUTED  = "#57606A"
PALETTE_2 = [C_BLUE, C_PURPLE]


# ── Shared figure template ────────────────────────────────────────────────────
def base_layout(title: str = "") -> dict:
    """Return a Plotly layout dict with the project's shared styling."""
    return dict(
        title=dict(
            text=title,
            font=dict(size=15, color=C_TEXT, family="Segoe UI, sans-serif"),
            x=0.02, xanchor="left",
        ),
        paper_bgcolor=C_CARD,
        plot_bgcolor=C_CARD,
        font=dict(family="Segoe UI, sans-serif", color=C_TEXT, size=12),
        margin=dict(t=52, l=52, r=20, b=52),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.25,
            xanchor="center", x=0.5,
            font=dict(size=12, color=C_TEXT),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            showgrid=False,
            linecolor=C_BORDER,
            tickfont=dict(size=11, color=C_TEXT),
            title_font=dict(size=12, color=C_MUTED),
        ),
        yaxis=dict(
            gridcolor=C_BORDER,
            linecolor=C_BORDER,
            tickfont=dict(size=11, color=C_TEXT),
            title_font=dict(size=12, color=C_MUTED),
        ),
        hoverlabel=dict(
            bgcolor=C_TEXT,
            font_color="#FFFFFF",
            font_size=12,
            bordercolor=C_TEXT,
        ),
    )


def filter_df(hotel_val: str, year_val: str) -> pd.DataFrame:
    """Return df_full filtered by the given dropdown selections."""
    d = df_full.copy()
    if hotel_val != "All":
        d = d[d["hotel"] == hotel_val]
    if year_val != "All":
        d = d[d["arrival_date_year"] == int(year_val)]
    return d
