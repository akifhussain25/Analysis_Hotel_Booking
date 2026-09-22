# Hotel Booking Analysis

A complete end-to-end data analysis project on hotel booking demand using a real-world dataset covering two hotel types across 2015–2017. The project covers data cleaning, exploratory data analysis, static visualisations, an interactive Dash dashboard, and a structured Jupyter notebook.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Objectives](#objectives)
4. [Dataset](#dataset)
5. [Technologies Used](#technologies-used)
6. [Project Structure](#project-structure)
7. [Installation & Setup](#installation--setup)
8. [How to Run](#how-to-run)
9. [Dashboard Information](#dashboard-information)
10. [Key Analysis Questions & Findings](#key-analysis-questions--findings)
11. [Business Insights](#business-insights)
12. [Conclusion](#conclusion)

---

## Project Overview

This project analyses **119,390 hotel bookings** (86,678 after cleaning) from a City Hotel and a Resort Hotel to understand booking patterns, cancellation behaviour, pricing trends, and guest loyalty. The analysis is delivered through:

- A Python data-cleaning pipeline (`clean_hotel_bookings.py`)
- An EDA script with computed results (`eda_hotel_bookings.py`)
- Eight publication-quality static charts (`visualize_hotel_bookings.py`)
- An interactive Dash dashboard with filters (`app.py` / `dashboard.py`)
- A complete Jupyter notebook (`Hotel_Booking_Analysis.ipynb`)

---

## Problem Statement

The hotel industry faces significant revenue losses from booking cancellations, seasonal demand swings, and heavy dependence on third-party Online Travel Agents (OTAs). This project aims to quantify these issues, identify their root drivers, and translate findings into practical revenue-management recommendations.

---

## Objectives

1. Clean and validate a raw hotel booking dataset (handle missing values, duplicates, inconsistent formats, and invalid records)
2. Answer 10 key business questions using pandas and actual computed statistics
3. Visualise findings with professional charts using matplotlib and seaborn
4. Build an interactive dashboard that allows filtering by hotel type and year
5. Derive 8 actionable business insights grounded in the data

---

## Dataset

| Property | Value |
|---|---|
| File | `hotel_bookings.csv` |
| Raw rows | 119,390 |
| Cleaned rows | 86,678 |
| Columns (raw) | 33 |
| Columns (cleaned) | 35 (2 new flag columns added) |
| Hotel types | Resort Hotel, City Hotel |
| Years | 2015, 2016, 2017 |
| ADR currency | EUR (converted to INR at ×90 in dashboard) |

**Key columns:**

| Column | Description |
|---|---|
| `hotel` | Hotel type |
| `is_canceled` | 1 = cancelled, 0 = completed |
| `lead_time` | Days between booking date and arrival |
| `arrival_date_year/month` | Arrival period |
| `stays_in_weekend_nights` | Weekend nights in stay |
| `stays_in_week_nights` | Weekday nights in stay |
| `adults / children / babies` | Guest counts |
| `meal` | Meal plan (BB, HB, FB, SC) |
| `country` | Guest country of origin |
| `market_segment` | Booking channel |
| `adr` | Average Daily Rate (EUR) |
| `reservation_status` | Check-Out / Canceled / No-Show |
| `agent` | Travel agent ID |
| `company` | Corporate company ID |
| `is_zero_adr` | Flag: ADR = 0 on non-complementary Check-Out *(added during cleaning)* |
| `is_group_block` | Flag: adults > 10 *(added during cleaning)* |

---

## Technologies Used

| Library | Version | Used for |
|---|---|---|
| Python | 3.13.4 | Runtime |
| pandas | 3.0.6 | Data loading, cleaning, EDA |
| numpy | 2.5.3 | Numerical operations |
| matplotlib | 3.11.2 | Static chart generation |
| seaborn | 0.13.2 | Statistical charts (box/violin) |
| plotly | 7.1.0 | Interactive dashboard charts |
| dash | 4.4.1 | Web dashboard framework |
| jupyter | — | Notebook environment |

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
hotel_bookings.csv/                   ← project root
│
├── app.py                            ← main entry point — run this
├── dashboard.py                      ← original standalone dashboard
│
├── clean_hotel_bookings.py           ← data cleaning script
├── eda_hotel_bookings.py             ← EDA with computed results
├── visualize_hotel_bookings.py       ← generates 8 static PNG charts
│
├── Hotel_Booking_Analysis.ipynb      ← complete project notebook
├── requirements.txt                  ← all Python dependencies
├── README.md                         ← this file
│
├── hotel_bookings.csv                ← raw dataset (never modified)
├── hotel_bookings_cleaned.csv        ← cleaned dataset (86,678 rows, 35 cols)
│
├── frontend/                         ← modular dashboard package
│   ├── __init__.py
│   ├── data.py                       ← data loading, constants, colour palette
│   ├── layout.py                     ← Dash HTML layout
│   └── callbacks.py                  ← all Dash reactive callbacks
│
└── charts/                           ← static PNGs at 150 dpi
    ├── 01_bookings_by_hotel_type.png
    ├── 02_monthly_booking_trend.png
    ├── 03_cancellation_vs_non_cancellation.png
    ├── 04_cancellation_rate_by_hotel.png
    ├── 05_bookings_by_market_segment.png
    ├── 06_adr_by_hotel_type.png
    ├── 07_avg_stay_by_hotel_type.png
    └── 08_lead_time_vs_cancellation.png
```

---

## Installation & Setup

**Prerequisites:** Python 3.10 or later

```bash
# 1. Navigate to the project folder
cd "c:\Users\Lenovo\Downloads\hotel_bookings.csv"

# 2. (Recommended) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## How to Run

### Interactive Dashboard (recommended)

```bash
python app.py
```

The browser opens automatically at **http://127.0.0.1:8050**. Press `Ctrl+C` to stop.

### Original Standalone Dashboard

```bash
python dashboard.py
```

Opens the same dashboard directly without the modular `frontend/` package.

### Data Cleaning Pipeline

```bash
python clean_hotel_bookings.py
```

Reads `hotel_bookings.csv`, applies all cleaning steps, writes `hotel_bookings_cleaned.csv`. Safe to re-run — the raw file is never touched.

### Static Charts

```bash
python visualize_hotel_bookings.py
```

Generates all 8 PNG charts in the `charts/` folder.

### EDA Script

```bash
python eda_hotel_bookings.py
```

Prints all 10 analysis results to the console.

### Jupyter Notebook

```bash
jupyter notebook Hotel_Booking_Analysis.ipynb
```

---

## Dashboard Information

The dashboard is built with **Dash 4.4.1** and **Plotly 7.1.0**.

**Filters** (both combinable):
- **Hotel Type** — All / City Hotel / Resort Hotel
- **Year** — All / 2015 / 2016 / 2017

**KPI Cards** (update live on filter change):
| KPI | Full-dataset Value |
|---|---|
| Total Bookings | 86,678 |
| Cancellation Rate | 27.72% |
| Avg Daily Rate (ADR) | ₹9,689 (€107.65) |
| Avg Length of Stay | 3.65 nights |

**Charts included:**
1. Bookings by Hotel Type — vertical bar + donut
2. Monthly Booking Trend — bar with line overlay
3. Cancellation Status — donut chart
4. Cancellation Rate by Hotel Type — bar with overall-average reference line
5. Bookings by Market Segment — horizontal bar
6. Average Daily Rate by Hotel Type — box plot (ADR displayed in ₹)

---

## Key Analysis Questions & Findings

All values computed from `hotel_bookings_cleaned.csv` (86,678 rows).

| # | Question | Result |
|---|---|---|
| 1 | Total bookings | **86,678** |
| 2 | City Hotel vs Resort Hotel | City: **53,070** (61.2%) · Resort: **33,608** (38.8%) |
| 3 | Overall cancellation rate | **27.72%** — 24,025 bookings |
| 4 | Higher cancellation by hotel | **City Hotel: 30.24%** vs Resort: 23.73% |
| 5 | Peak / lowest booking month | Peak: **August (11,195)** · Lowest: **January (4,642)** |
| 6 | Average length of stay | Overall: **3.65 nights** · City: 3.15 · Resort: 4.44 |
| 7 | Average Daily Rate (ADR) | Mean: **€107.65 (₹9,689)** · Median: €99.00 · Max: €5,400 |
| 8 | Top market segment | **Online TA: 59.18%** (51,300 bookings) |
| 9 | Repeated guest rate | **3.63%** (3,147 bookings) |
| 10 | Lead time vs cancellation | r = **0.183** · 0–7 days: 9.77% → 365+ days: 41.10% |

---

## Business Insights

| # | Insight | Key Figure | Action |
|---|---|---|---|
| 1 | High cancellation is a revenue leak | 27.72% (24,025 bookings) | Tiered cancellation policy with non-refundable incentives |
| 2 | City Hotel cancels 6.51 pp more than Resort | 30.24% vs 23.73% | Stricter City Hotel overbooking buffer |
| 3 | Lead time predicts cancellation monotonically | 9.77% → 41.10% as lead time grows | Flag long-lead bookings; early-bird non-refundable discounts |
| 4 | 2.4× seasonal demand swing | August 11,195 vs January 4,642 | Dynamic pricing peaks + off-peak promotions Nov–Feb |
| 5 | OTAs control 59.18% of bookings | 51,300 via Online TA | Book-direct campaign with best-rate guarantee |
| 6 | Near-zero repeat guest rate | Only 3.63% (3,147 guests) | Post-checkout loyalty email with 10% direct-booking discount |
| 7 | Resort guests stay 41% longer | 4.44 vs 3.15 nights | Minimum-stay packages for Resort; express services for City |
| 8 | City Hotel higher ADR but higher risk | €112.18 vs €100.49 | City overbook 8–10%; Resort 5–6% |

---

## Conclusion

Analysis of 86,678 cleaned hotel bookings reveals four core challenges:

1. **Cancellation risk** — 27.72% of bookings do not result in a stay, with City Hotel significantly worse (30.24%). Lead time is the strongest available predictor, with cancellation rates rising from 9.77% (same-week) to 41.10% (365+ days ahead).

2. **Seasonal concentration** — July and August alone account for 24.5% of annual bookings. The four winter months (Nov–Feb) hold only 23.8%, leaving significant capacity underutilised.

3. **OTA channel dependency** — 59.18% of bookings flow through Online Travel Agents at high commission cost. Direct bookings at 13.45% represent a high-margin channel with room to grow.

4. **Guest retention gap** — Only 3.63% of bookings come from repeat guests, indicating the hotels are on a costly perpetual new-acquisition cycle.

The two hotel types serve fundamentally different customer segments and require separate pricing, cancellation, and marketing strategies rather than a one-size-fits-all approach.

---

*Project built with Python 3.13.4 · pandas 3.0.6 · Dash 4.4.1 · Plotly 7.1.0 · matplotlib 3.11.2 · seaborn 0.13.2*
