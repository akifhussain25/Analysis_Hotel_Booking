"""
frontend/layout.py
==================
Defines the complete Dash page layout: header, filter bar, KPI row,
and all six chart panels.  No data or callback logic lives here.
"""

from dash import html, dcc
from frontend.data import (
    C_BLUE, C_BG, C_CARD, C_BORDER, C_TEXT, C_MUTED,
    HOTEL_TYPES, YEARS,
)


# ── Card wrapper ──────────────────────────────────────────────────────────────
def _card(child):
    return html.Div(
        child,
        style={
            "backgroundColor": C_CARD,
            "border": f"1px solid {C_BORDER}",
            "borderRadius": "8px",
            "overflow": "hidden",
        },
    )


# ── Full page layout ──────────────────────────────────────────────────────────
def build_layout() -> html.Div:
    """Return the complete Dash layout tree."""

    return html.Div(
        style={
            "backgroundColor": C_BG,
            "minHeight": "100vh",
            "fontFamily": "Segoe UI, system-ui, sans-serif",
            "color": C_TEXT,
        },
        children=[

            # ── Header ────────────────────────────────────────────────────────
            html.Div(
                style={
                    "backgroundColor": C_BLUE,
                    "padding": "22px 32px",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "space-between",
                    "boxShadow": "0 2px 8px rgba(0,0,0,.12)",
                },
                children=[
                    html.Div([
                        html.H1(
                            "Hotel Booking Analysis Dashboard",
                            style={
                                "color": "#fff",
                                "margin": "0",
                                "fontSize": "22px",
                                "fontWeight": "700",
                            },
                        ),
                        html.P(
                            "Source: hotel_bookings_cleaned.csv  "
                            "|  86,678 bookings  |  2015–2017",
                            style={
                                "color": "rgba(255,255,255,.75)",
                                "margin": "4px 0 0",
                                "fontSize": "13px",
                            },
                        ),
                    ]),
                ],
            ),

            # ── Filter bar ────────────────────────────────────────────────────
            html.Div(
                style={
                    "backgroundColor": C_CARD,
                    "borderBottom": f"1px solid {C_BORDER}",
                    "padding": "14px 32px",
                    "display": "flex",
                    "gap": "32px",
                    "alignItems": "center",
                    "flexWrap": "wrap",
                },
                children=[
                    # Hotel type filter
                    html.Div([
                        html.Label(
                            "Hotel Type",
                            style={
                                "fontSize": "11px", "fontWeight": "700",
                                "color": C_MUTED,
                                "textTransform": "uppercase",
                                "letterSpacing": ".05em",
                                "marginBottom": "4px",
                                "display": "block",
                            },
                        ),
                        dcc.Dropdown(
                            id="filter-hotel",
                            options=[{"label": h, "value": h} for h in HOTEL_TYPES],
                            value="All",
                            clearable=False,
                            style={"width": "200px", "fontSize": "13px",
                                   "color": C_TEXT},
                        ),
                    ]),

                    # Year filter
                    html.Div([
                        html.Label(
                            "Year",
                            style={
                                "fontSize": "11px", "fontWeight": "700",
                                "color": C_MUTED,
                                "textTransform": "uppercase",
                                "letterSpacing": ".05em",
                                "marginBottom": "4px",
                                "display": "block",
                            },
                        ),
                        dcc.Dropdown(
                            id="filter-year",
                            options=[{"label": str(y), "value": str(y)}
                                     for y in YEARS],
                            value="All",
                            clearable=False,
                            style={"width": "140px", "fontSize": "13px",
                                   "color": C_TEXT},
                        ),
                    ]),

                    # Live booking count note (populated by callback)
                    html.Div(
                        id="filter-note",
                        style={
                            "marginLeft": "auto",
                            "fontSize": "12px",
                            "color": C_MUTED,
                            "alignSelf": "flex-end",
                            "paddingBottom": "2px",
                        },
                    ),
                ],
            ),

            # ── Main content ──────────────────────────────────────────────────
            html.Div(
                style={
                    "padding": "24px 32px",
                    "maxWidth": "1400px",
                    "margin": "0 auto",
                },
                children=[

                    # KPI row (populated by callback)
                    html.Div(
                        id="kpi-row",
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "gap": "16px",
                            "marginBottom": "24px",
                        },
                    ),

                    # Row 1 — Hotel type split (1/3) + Monthly trend (2/3)
                    html.Div(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "1fr 2fr",
                            "gap": "16px",
                            "marginBottom": "16px",
                        },
                        children=[
                            _card(dcc.Graph(id="chart-hotel-type",
                                           config={"displayModeBar": False})),
                            _card(dcc.Graph(id="chart-monthly",
                                           config={"displayModeBar": False})),
                        ],
                    ),

                    # Row 2 — Cancellation status + Cancellation rate by hotel
                    html.Div(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "1fr 1fr",
                            "gap": "16px",
                            "marginBottom": "16px",
                        },
                        children=[
                            _card(dcc.Graph(id="chart-cancel-status",
                                           config={"displayModeBar": False})),
                            _card(dcc.Graph(id="chart-cancel-hotel",
                                           config={"displayModeBar": False})),
                        ],
                    ),

                    # Row 3 — Market segment + ADR by hotel
                    html.Div(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "1fr 1fr",
                            "gap": "16px",
                            "marginBottom": "16px",
                        },
                        children=[
                            _card(dcc.Graph(id="chart-segment",
                                           config={"displayModeBar": False})),
                            _card(dcc.Graph(id="chart-adr",
                                           config={"displayModeBar": False})),
                        ],
                    ),

                    # Footer
                    html.P(
                        "Hotel Booking Analysis Dashboard  ·  "
                        "Data: hotel_bookings_cleaned.csv  ·  "
                        "Built with Dash + Plotly",
                        style={
                            "textAlign": "center",
                            "fontSize": "12px",
                            "color": C_MUTED,
                            "marginTop": "16px",
                            "paddingTop": "16px",
                            "borderTop": f"1px solid {C_BORDER}",
                        },
                    ),
                ],
            ),
        ],
    )
