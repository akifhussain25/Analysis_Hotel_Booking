"""
Hotel Bookings — EDA Script
Outputs structured results for all 10 questions.
"""
import pandas as pd
import numpy as np

df = pd.read_csv("hotel_bookings_cleaned.csv", low_memory=False)

# ── 1. Total number of bookings ──────────────────────────────────────────────
q1 = len(df)
print(f"Q1_TOTAL_BOOKINGS={q1}")

# ── 2. Bookings by hotel type ────────────────────────────────────────────────
q2 = df["hotel"].value_counts()
print(f"Q2_CITY_HOTEL={q2.get('City Hotel', 0)}")
print(f"Q2_RESORT_HOTEL={q2.get('Resort Hotel', 0)}")

# ── 3. Overall cancellation rate ─────────────────────────────────────────────
q3_canceled = df["is_canceled"].sum()
q3_pct = round(df["is_canceled"].mean() * 100, 2)
print(f"Q3_CANCELED_COUNT={q3_canceled}")
print(f"Q3_CANCELED_PCT={q3_pct}")

# ── 4. Cancellation rate by hotel type ───────────────────────────────────────
q4 = df.groupby("hotel")["is_canceled"].mean().mul(100).round(2)
for hotel, rate in q4.items():
    key = hotel.replace(" ", "_").upper()
    print(f"Q4_{key}_CANCEL_RATE={rate}")

# ── 5. Bookings by month (highest and lowest) ────────────────────────────────
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
q5 = df["arrival_date_month"].value_counts()
q5_sorted_by_month = df["arrival_date_month"].value_counts().reindex(month_order)
q5_max_month = q5.idxmax()
q5_max_count = int(q5.max())
q5_min_month = q5.idxmin()
q5_min_count = int(q5.min())
print(f"Q5_MAX_MONTH={q5_max_month}")
print(f"Q5_MAX_COUNT={q5_max_count}")
print(f"Q5_MIN_MONTH={q5_min_month}")
print(f"Q5_MIN_COUNT={q5_min_count}")
for m in month_order:
    print(f"Q5_MONTH_{m.upper()}={int(q5_sorted_by_month.get(m, 0))}")

# ── 6. Average length of stay ─────────────────────────────────────────────────
df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
q6_overall = round(df["total_nights"].mean(), 2)
q6_city = round(df.loc[df["hotel"]=="City Hotel","total_nights"].mean(), 2)
q6_resort = round(df.loc[df["hotel"]=="Resort Hotel","total_nights"].mean(), 2)
print(f"Q6_AVG_NIGHTS_OVERALL={q6_overall}")
print(f"Q6_AVG_NIGHTS_CITY={q6_city}")
print(f"Q6_AVG_NIGHTS_RESORT={q6_resort}")

# ── 7. Average Daily Rate ─────────────────────────────────────────────────────
# Use only rows where adr > 0 and is_zero_adr == 0 for a meaningful average
df_adr = df[df["is_zero_adr"] == 0]
q7_overall = round(df_adr["adr"].mean(), 2)
q7_city = round(df_adr.loc[df_adr["hotel"]=="City Hotel","adr"].mean(), 2)
q7_resort = round(df_adr.loc[df_adr["hotel"]=="Resort Hotel","adr"].mean(), 2)
q7_median = round(df_adr["adr"].median(), 2)
q7_min = round(df_adr["adr"].min(), 2)
q7_max = round(df_adr["adr"].max(), 2)
print(f"Q7_ADR_MEAN={q7_overall}")
print(f"Q7_ADR_MEDIAN={q7_median}")
print(f"Q7_ADR_MIN={q7_min}")
print(f"Q7_ADR_MAX={q7_max}")
print(f"Q7_ADR_CITY={q7_city}")
print(f"Q7_ADR_RESORT={q7_resort}")

# ── 8. Market segment with most bookings ─────────────────────────────────────
q8 = df["market_segment"].value_counts()
for seg, cnt in q8.items():
    pct = round(cnt / len(df) * 100, 2)
    key = seg.replace(" ", "_").replace("/", "_").upper()
    print(f"Q8_SEG_{key}={cnt}|{pct}")

# ── 9. Repeated guests ────────────────────────────────────────────────────────
q9_count = int(df["is_repeated_guest"].sum())
q9_pct = round(df["is_repeated_guest"].mean() * 100, 2)
print(f"Q9_REPEATED_GUEST_COUNT={q9_count}")
print(f"Q9_REPEATED_GUEST_PCT={q9_pct}")

# ── 10. Lead time vs cancellation ────────────────────────────────────────────
# Mean lead time for canceled vs not canceled
q10_mean_lead_canceled = round(df.loc[df["is_canceled"]==1,"lead_time"].mean(), 2)
q10_mean_lead_not_canceled = round(df.loc[df["is_canceled"]==0,"lead_time"].mean(), 2)

# Pearson correlation between lead_time and is_canceled
q10_corr = round(df["lead_time"].corr(df["is_canceled"]), 4)

# Binned cancellation rates
bins = [0, 7, 30, 90, 180, 365, df["lead_time"].max()+1]
labels = ["0–7d","8–30d","31–90d","91–180d","181–365d","365d+"]
df["lead_bin"] = pd.cut(df["lead_time"], bins=bins, labels=labels, right=True)
q10_bins = df.groupby("lead_bin", observed=True)["is_canceled"].agg(["mean","count"])
q10_bins["cancel_rate_pct"] = (q10_bins["mean"] * 100).round(2)

print(f"Q10_CORR_LEAD_CANCEL={q10_corr}")
print(f"Q10_MEAN_LEAD_CANCELED={q10_mean_lead_canceled}")
print(f"Q10_MEAN_LEAD_NOT_CANCELED={q10_mean_lead_not_canceled}")
for label, row in q10_bins.iterrows():
    key = str(label).replace("–","_").replace("+","plus").replace("d","")
    print(f"Q10_BIN_{key}_RATE={row['cancel_rate_pct']}|COUNT={int(row['count'])}")

print("DONE")
