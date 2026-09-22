"""
Hotel Booking Analysis — Interactive Dashboard
================================================
Run:  python dashboard.py
Open: http://127.0.0.1:8050  in your browser

Requires:  pip install dash plotly pandas
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# ─────────────────────────────────────────────────────────────────────────────
# 1. DATA
# ─────────────────────────────────────────────────────────────────────────────
df_full = pd.read_csv("hotel_bookings_cleaned.csv", low_memory=False)
df_full["total_nights"] = (
    df_full["stays_in_weekend_nights"] + df_full["stays_in_week_nights"]
)

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
HOTEL_TYPES  = ["All"] + sorted(df_full["hotel"].unique().tolist())
YEARS        = ["All"] + sorted(df_full["arrival_date_year"].unique().tolist())

# ─────────────────────────────────────────────────────────────────────────────
# 2. COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────────────────────
# 3. HELPER — shared figure template
# ─────────────────────────────────────────────────────────────────────────────
def base_layout(title=""):
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

# ─────────────────────────────────────────────────────────────────────────────
# 4. CARD STYLE HELPER  (must be defined before layout uses it)
# ─────────────────────────────────────────────────────────────────────────────
def _card_style():
    return {
        "backgroundColor": C_CARD,
        "border": f"1px solid {C_BORDER}",
        "borderRadius": "8px",
        "overflow": "hidden",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 5. APP LAYOUT
# ─────────────────────────────────────────────────────────────────────────────
app = Dash(__name__, title="Hotel Booking Dashboard")

app.layout = html.Div(
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
                        style={"color": "#fff", "margin": "0",
                               "fontSize": "22px", "fontWeight": "700"},
                    ),
                    html.P(
                        "Source: hotel_bookings_cleaned.csv  |  86,678 bookings  |  2015–2017",
                        style={"color": "rgba(255,255,255,.75)",
                               "margin": "4px 0 0", "fontSize": "13px"},
                    ),
                ]),
            ],
        ),

        # ── Filters ───────────────────────────────────────────────────────
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
                html.Div([
                    html.Label(
                        "Hotel Type",
                        style={"fontSize": "11px", "fontWeight": "700",
                               "color": C_MUTED, "textTransform": "uppercase",
                               "letterSpacing": ".05em", "marginBottom": "4px",
                               "display": "block"},
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
                html.Div([
                    html.Label(
                        "Year",
                        style={"fontSize": "11px", "fontWeight": "700",
                               "color": C_MUTED, "textTransform": "uppercase",
                               "letterSpacing": ".05em", "marginBottom": "4px",
                               "display": "block"},
                    ),
                    dcc.Dropdown(
                        id="filter-year",
                        options=[{"label": str(y), "value": str(y)} for y in YEARS],
                        value="All",
                        clearable=False,
                        style={"width": "140px", "fontSize": "13px",
                               "color": C_TEXT},
                    ),
                ]),
                html.Div(
                    id="filter-note",
                    style={"marginLeft": "auto", "fontSize": "12px",
                           "color": C_MUTED, "alignSelf": "flex-end",
                           "paddingBottom": "2px"},
                ),
            ],
        ),

        # ── Main content ──────────────────────────────────────────────────
        html.Div(
            style={"padding": "24px 32px", "maxWidth": "1400px", "margin": "0 auto"},
            children=[

                # KPI row
                html.Div(
                    id="kpi-row",
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(4, 1fr)",
                        "gap": "16px",
                        "marginBottom": "24px",
                    },
                ),

                # Row 1: Hotel type split + Monthly trend
                html.Div(
                    style={"display": "grid",
                           "gridTemplateColumns": "1fr 2fr",
                           "gap": "16px", "marginBottom": "16px"},
                    children=[
                        html.Div(dcc.Graph(id="chart-hotel-type",
                                           config={"displayModeBar": False}),
                                 style=_card_style()),
                        html.Div(dcc.Graph(id="chart-monthly",
                                           config={"displayModeBar": False}),
                                 style=_card_style()),
                    ],
                ),

                # Row 2: Cancellation status + Cancellation rate by hotel
                html.Div(
                    style={"display": "grid",
                           "gridTemplateColumns": "1fr 1fr",
                           "gap": "16px", "marginBottom": "16px"},
                    children=[
                        html.Div(dcc.Graph(id="chart-cancel-status",
                                           config={"displayModeBar": False}),
                                 style=_card_style()),
                        html.Div(dcc.Graph(id="chart-cancel-hotel",
                                           config={"displayModeBar": False}),
                                 style=_card_style()),
                    ],
                ),

                # Row 3: Market segment + ADR by hotel
                html.Div(
                    style={"display": "grid",
                           "gridTemplateColumns": "1fr 1fr",
                           "gap": "16px", "marginBottom": "16px"},
                    children=[
                        html.Div(dcc.Graph(id="chart-segment",
                                           config={"displayModeBar": False}),
                                 style=_card_style()),
                        html.Div(dcc.Graph(id="chart-adr",
                                           config={"displayModeBar": False}),
                                 style=_card_style()),
                    ],
                ),

                # Footer
                html.P(
                    "Hotel Booking Analysis Dashboard  ·  Data: hotel_bookings_cleaned.csv  ·  Built with Dash + Plotly",
                    style={"textAlign": "center", "fontSize": "12px",
                           "color": C_MUTED, "marginTop": "16px",
                           "paddingTop": "16px",
                           "borderTop": f"1px solid {C_BORDER}"},
                ),
            ],
        ),
    ],
)


# ─────────────────────────────────────────────────────────────────────────────
# 6. CALLBACKS
# ─────────────────────────────────────────────────────────────────────────────
def _filter(hotel_val, year_val):
    """Return the filtered dataframe based on current dropdown selections."""
    d = df_full.copy()
    if hotel_val != "All":
        d = d[d["hotel"] == hotel_val]
    if year_val != "All":
        d = d[d["arrival_date_year"] == int(year_val)]
    return d


@app.callback(
    Output("filter-note", "children"),
    Output("kpi-row", "children"),
    Output("chart-hotel-type", "figure"),
    Output("chart-monthly", "figure"),
    Output("chart-cancel-status", "figure"),
    Output("chart-cancel-hotel", "figure"),
    Output("chart-segment", "figure"),
    Output("chart-adr", "figure"),
    Input("filter-hotel", "value"),
    Input("filter-year", "value"),
)
def update_all(hotel_val, year_val):
    df = _filter(hotel_val, year_val)
    n  = len(df)

    # ── filter note ────────────────────────────────────────────────────────
    note = f"Showing {n:,} bookings"
    if hotel_val != "All":
        note += f"  ·  {hotel_val}"
    if year_val != "All":
        note += f"  ·  {year_val}"

    # ── KPI cards ──────────────────────────────────────────────────────────
    EUR_TO_INR   = 90
    cancel_rate  = df["is_canceled"].mean() * 100
    df_adr       = df[df["is_zero_adr"] == 0]
    avg_adr_inr  = (df_adr["adr"].mean() if len(df_adr) else 0) * EUR_TO_INR
    avg_nights   = df["total_nights"].mean() if n else 0

    kpis = [
        ("Total Bookings",       f"{n:,}",                    C_BLUE,   "#fff"),
        ("Cancellation Rate",    f"{cancel_rate:.1f}%",        C_RED,    "#fff"),
        ("Avg Daily Rate (ADR)", f"\u20b9{avg_adr_inr:,.0f}", C_GREEN,  "#fff"),
        ("Avg Length of Stay",   f"{avg_nights:.2f} nights",   C_PURPLE, "#fff"),
    ]

    kpi_cards = []
    for label, value, bg, fg in kpis:
        kpi_cards.append(
            html.Div(
                style={
                    "backgroundColor": bg,
                    "borderRadius": "8px",
                    "padding": "20px 22px",
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "6px",
                },
                children=[
                    html.Div(label, style={
                        "fontSize": "12px", "fontWeight": "700",
                        "color": "rgba(255,255,255,.8)",
                        "textTransform": "uppercase", "letterSpacing": ".05em",
                    }),
                    html.Div(value, style={
                        "fontSize": "28px", "fontWeight": "800",
                        "color": fg, "lineHeight": "1.1",
                    }),
                ],
            )
        )

    # ── Chart 1: Bookings by hotel type ───────────────────────────────────
    hc = df["hotel"].value_counts().reset_index()
    hc.columns = ["hotel", "count"]
    hc["pct"] = (hc["count"] / hc["count"].sum() * 100).round(1)

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=hc["hotel"], y=hc["count"],
        marker_color=PALETTE_2[:len(hc)],
        text=[f"{v:,}<br>({p}%)" for v, p in zip(hc["count"], hc["pct"])],
        textposition="outside",
        textfont=dict(size=13, color=C_TEXT),
        hovertemplate="<b>%{x}</b><br>Bookings: %{y:,}<extra></extra>",
        width=0.45,
    ))
    lay1 = base_layout("Bookings by Hotel Type")
    lay1["yaxis"]["title"] = "Number of Bookings"
    lay1["yaxis"]["range"] = [0, hc["count"].max() * 1.22]
    lay1["xaxis"]["title"] = ""
    lay1["showlegend"] = False
    fig1.update_layout(**lay1)

    # ── Chart 2: Monthly booking trend ───────────────────────────────────
    monthly = (
        df["arrival_date_month"].value_counts()
        .reindex(MONTH_ORDER)
        .fillna(0)
        .reset_index()
    )
    monthly.columns = ["month", "count"]
    monthly["month_short"] = monthly["month"].str[:3]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=monthly["month_short"], y=monthly["count"],
        marker_color=C_BLUE, opacity=0.80, name="Bookings",
        hovertemplate="<b>%{x}</b><br>Bookings: %{y:,}<extra></extra>",
    ))
    fig2.add_trace(go.Scatter(
        x=monthly["month_short"], y=monthly["count"],
        mode="lines+markers",
        line=dict(color=C_BLUE, width=2.5),
        marker=dict(size=6, color=C_BLUE),
        name="Trend",
        hovertemplate="<b>%{x}</b><br>%{y:,}<extra></extra>",
    ))
    lay2 = base_layout("Monthly Booking Trend")
    lay2["yaxis"]["title"] = "Number of Bookings"
    lay2["xaxis"]["title"] = "Month"
    lay2["bargap"] = 0.25
    fig2.update_layout(**lay2)

    # ── Chart 3: Cancellation status (donut) ─────────────────────────────
    cancel_counts = df["is_canceled"].value_counts().reset_index()
    cancel_counts.columns = ["status", "count"]
    cancel_counts["label"] = cancel_counts["status"].map(
        {0: "Not Cancelled", 1: "Cancelled"}
    )

    fig3 = go.Figure(go.Pie(
        labels=cancel_counts["label"],
        values=cancel_counts["count"],
        hole=0.52,
        marker=dict(colors=[C_GREEN, C_RED],
                    line=dict(color="#fff", width=3)),
        textinfo="label+percent",
        textfont=dict(size=13, color=C_TEXT),
        hovertemplate="<b>%{label}</b><br>%{value:,} bookings (%{percent})<extra></extra>",
        direction="clockwise",
        sort=False,
    ))
    fig3.update_layout(
        title=dict(text="Cancellation Status", font=dict(size=15, color=C_TEXT,
                   family="Segoe UI, sans-serif"), x=0.02, xanchor="left"),
        paper_bgcolor=C_CARD,
        font=dict(family="Segoe UI, sans-serif", color=C_TEXT, size=12),
        margin=dict(t=52, l=20, r=20, b=52),
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.15,
            xanchor="center", x=0.5,
            font=dict(size=12, color=C_TEXT),
            bgcolor="rgba(0,0,0,0)",
        ),
        hoverlabel=dict(bgcolor=C_TEXT, font_color="#fff",
                        font_size=12, bordercolor=C_TEXT),
    )

    # ── Chart 4: Cancellation rate by hotel type ──────────────────────────
    if hotel_val == "All":
        cr = (
            df.groupby("hotel")["is_canceled"]
              .mean()
              .mul(100)
              .round(2)
              .reset_index()
        )
        cr.columns = ["hotel", "cancel_rate"]
        overall = df["is_canceled"].mean() * 100
    else:
        cr = pd.DataFrame({"hotel": [hotel_val],
                           "cancel_rate": [df["is_canceled"].mean() * 100]})
        overall = cancel_rate

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=cr["hotel"], y=cr["cancel_rate"],
        marker_color=[C_BLUE, C_PURPLE][:len(cr)],
        text=[f"{v:.1f}%" for v in cr["cancel_rate"]],
        textposition="outside",
        textfont=dict(size=14, color=C_TEXT),
        width=0.4,
        hovertemplate="<b>%{x}</b><br>Cancellation rate: %{text}<extra></extra>",
    ))
    fig4.add_hline(
        y=overall, line_dash="dash",
        line_color=C_TEXT, line_width=1.5,
        annotation_text=f"Overall avg: {overall:.1f}%",
        annotation_font=dict(size=11, color=C_TEXT),
        annotation_position="top right",
    )
    lay4 = base_layout("Cancellation Rate by Hotel Type")
    lay4["yaxis"]["title"] = "Cancellation Rate (%)"
    lay4["yaxis"]["range"] = [0, max(cr["cancel_rate"].max(), overall) * 1.3]
    lay4["xaxis"]["title"] = ""
    lay4["showlegend"] = False
    fig4.update_layout(**lay4)

    # ── Chart 5: Market segment ───────────────────────────────────────────
    seg = (
        df["market_segment"].value_counts()
          .reset_index()
          .sort_values("count", ascending=True)
    )
    seg.columns = ["segment", "count"]
    seg["pct"] = (seg["count"] / n * 100).round(1)
    bar_colors = [C_BLUE if s == "Online TA" else "#90b4e8" for s in seg["segment"]]

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        y=seg["segment"],
        x=seg["count"],
        orientation="h",
        marker_color=bar_colors,
        text=[f"{v:,}  ({p}%)" for v, p in zip(seg["count"], seg["pct"])],
        textposition="outside",
        textfont=dict(size=11, color=C_TEXT),
        hovertemplate="<b>%{y}</b><br>Bookings: %{x:,} (%{text})<extra></extra>",
    ))
    lay5 = base_layout("Bookings by Market Segment")
    lay5["xaxis"]["title"] = "Number of Bookings"
    lay5["yaxis"]["title"] = ""
    lay5["xaxis"]["range"] = [0, seg["count"].max() * 1.30]
    lay5["showlegend"] = False
    lay5["margin"]["l"] = 120
    fig5.update_layout(**lay5)

    # ── Chart 6: ADR by hotel type (box) ──────────────────────────────────
    EUR_TO_INR = 90
    df_adr2 = df[(df["is_zero_adr"] == 0) & (df["adr"] <= 500)].copy()
    df_adr2["adr"] = df_adr2["adr"] * EUR_TO_INR
    hotels_present = df_adr2["hotel"].unique().tolist()

    fig6 = go.Figure()
    for i, hotel in enumerate(hotels_present):
        sub = df_adr2[df_adr2["hotel"] == hotel]["adr"]
        fig6.add_trace(go.Box(
            y=sub,
            name=hotel,
            marker_color=PALETTE_2[i % 2],
            line_color=PALETTE_2[i % 2],
            fillcolor=PALETTE_2[i % 2] + "55",
            boxmean=True,
            hovertemplate=(
                f"<b>{hotel}</b><br>"
                "Median: %{median:.2f}<br>"
                "Q1: %{q1:.2f} / Q3: %{q3:.2f}<extra></extra>"
            ),
        ))

    lay6 = base_layout("Average Daily Rate (ADR) by Hotel Type")
    lay6["yaxis"]["title"] = "ADR (\u20b9)"
    lay6["xaxis"]["title"] = ""
    lay6["yaxis"]["tickprefix"] = "\u20b9"
    lay6["showlegend"] = True
    fig6.update_layout(**lay6)

    return note, kpi_cards, fig1, fig2, fig3, fig4, fig5, fig6


# ─────────────────────────────────────────────────────────────────────────────
# 6. RUN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import threading
    import webbrowser

    url = "http://127.0.0.1:8050"

    # Open the browser after a short delay so the server is ready first
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()

    print("=" * 55)
    print(" Hotel Booking Analysis Dashboard")
    print(f" Opening {url} in your browser...")
    print("=" * 55)
    app.run(debug=False, host="127.0.0.1", port=8050)
