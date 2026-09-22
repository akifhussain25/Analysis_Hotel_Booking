"""
Hotel Bookings — Visualization Script
=======================================
Generates 8 professional charts from hotel_bookings_cleaned.csv and saves
each as a PNG file in the charts/ subdirectory.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend — no display needed
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np

# ── Output directory ────────────────────────────────────────────────────────
os.makedirs("charts", exist_ok=True)

# ── Shared style ────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   14,
    "axes.titleweight": "bold",
    "axes.labelsize":   11,
    "xtick.labelsize":  10,
    "ytick.labelsize":  10,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "figure.dpi":         150,
    "savefig.dpi":        150,
    "savefig.bbox":       "tight",
})

BLUE   = "#3B82D4"
PURPLE = "#7C5CD8"
RED    = "#E05252"
GREEN  = "#3BA876"
COLORS_2 = [BLUE, PURPLE]
FONT_CAPTION = dict(fontsize=9, color="#57606a", style="italic")

# ── Load data ────────────────────────────────────────────────────────────────
df = pd.read_csv("hotel_bookings_cleaned.csv", low_memory=False)
df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]

MONTH_ORDER = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

print(f"Loaded {len(df):,} rows from hotel_bookings_cleaned.csv")
print("Generating charts...\n")


# ════════════════════════════════════════════════════════════════════════════
# Chart 1 — Bookings by Hotel Type (donut + bar combo)
# ════════════════════════════════════════════════════════════════════════════
hotel_counts = df["hotel"].value_counts()
labels  = hotel_counts.index.tolist()
sizes   = hotel_counts.values
total   = sizes.sum()

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
fig.suptitle("Bookings by Hotel Type", fontsize=15, fontweight="bold", y=1.01)

# Donut
wedge_props = dict(width=0.45, edgecolor="white", linewidth=2)
axes[0].pie(sizes, labels=None, colors=COLORS_2, autopct="%1.1f%%",
            pctdistance=0.75, startangle=90, wedgeprops=wedge_props,
            textprops=dict(fontsize=11, fontweight="bold"))
axes[0].legend(labels, loc="lower center", bbox_to_anchor=(0.5, -0.08),
               ncol=2, frameon=False, fontsize=10)
axes[0].set_title("Share of Bookings", pad=10)

# Bar with count labels
bars = axes[1].bar(labels, sizes, color=COLORS_2, width=0.5,
                   edgecolor="white", linewidth=1.2)
for bar, val in zip(bars, sizes):
    axes[1].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 400,
                 f"{val:,}", ha="center", va="bottom",
                 fontsize=11, fontweight="bold")
axes[1].set_ylabel("Number of Bookings")
axes[1].set_title("Absolute Count", pad=10)
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
axes[1].set_ylim(0, max(sizes) * 1.12)

fig.text(0.5, -0.03,
         "City Hotel accounts for 61.2% of all bookings vs 38.8% for Resort Hotel.",
         ha="center", **FONT_CAPTION)

plt.tight_layout()
plt.savefig("charts/01_bookings_by_hotel_type.png")
plt.close()
print("  [1/8] charts/01_bookings_by_hotel_type.png")


# ════════════════════════════════════════════════════════════════════════════
# Chart 2 — Monthly Booking Trends
# ════════════════════════════════════════════════════════════════════════════
monthly = (df["arrival_date_month"]
           .value_counts()
           .reindex(MONTH_ORDER))

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(monthly.index, monthly.values, color=BLUE, edgecolor="white",
       linewidth=0.8, alpha=0.85, label="All Hotels")

# Line overlay
ax.plot(monthly.index, monthly.values, color=BLUE, linewidth=2,
        marker="o", markersize=5, zorder=5)

# Annotate peak and trough
peak_m = monthly.idxmax()
low_m  = monthly.idxmin()
ax.annotate(f"Peak\n{monthly[peak_m]:,}",
            xy=(peak_m, monthly[peak_m]),
            xytext=(0, 14), textcoords="offset points",
            ha="center", fontsize=9, fontweight="bold", color=BLUE,
            arrowprops=dict(arrowstyle="-", color=BLUE, lw=1.2))
ax.annotate(f"Low\n{monthly[low_m]:,}",
            xy=(low_m, monthly[low_m]),
            xytext=(0, -28), textcoords="offset points",
            ha="center", fontsize=9, fontweight="bold", color=RED,
            arrowprops=dict(arrowstyle="-", color=RED, lw=1.2))

ax.set_title("Monthly Booking Trend (All Years Combined)")
ax.set_xlabel("Month of Arrival")
ax.set_ylabel("Number of Bookings")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.xticks(rotation=30, ha="right")
fig.text(0.5, -0.04,
         "August is the busiest month (11,195 bookings); January is the quietest (4,642).",
         ha="center", **FONT_CAPTION)
plt.tight_layout()
plt.savefig("charts/02_monthly_booking_trend.png")
plt.close()
print("  [2/8] charts/02_monthly_booking_trend.png")


# ════════════════════════════════════════════════════════════════════════════
# Chart 3 — Cancellation vs Non-Cancellation
# ════════════════════════════════════════════════════════════════════════════
status_map  = {0: "Not Cancelled", 1: "Cancelled"}
status_vals = df["is_canceled"].map(status_map).value_counts()
status_pct  = (status_vals / status_vals.sum() * 100).round(1)

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
fig.suptitle("Cancellation vs Non-Cancellation", fontsize=15, fontweight="bold", y=1.01)

colors_cn = [GREEN, RED]
wedge_props = dict(width=0.45, edgecolor="white", linewidth=2)
axes[0].pie(status_vals, labels=None, colors=colors_cn, autopct="%1.1f%%",
            pctdistance=0.75, startangle=90, wedgeprops=wedge_props,
            textprops=dict(fontsize=12, fontweight="bold"))
axes[0].legend(status_vals.index.tolist(), loc="lower center",
               bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=False, fontsize=10)
axes[0].set_title("Share")

bars = axes[1].barh(status_vals.index, status_vals.values,
                    color=colors_cn, edgecolor="white", linewidth=1.2, height=0.45)
for bar, val, pct in zip(bars, status_vals.values, status_pct.values):
    axes[1].text(bar.get_width() + 300, bar.get_y() + bar.get_height() / 2,
                 f"{val:,}  ({pct}%)", va="center", fontsize=10, fontweight="bold")
axes[1].set_xlabel("Number of Bookings")
axes[1].set_title("Absolute Count")
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
axes[1].set_xlim(0, max(status_vals.values) * 1.22)

fig.text(0.5, -0.03,
         "27.72% of bookings were cancelled (24,025); 72.28% completed (62,653).",
         ha="center", **FONT_CAPTION)
plt.tight_layout()
plt.savefig("charts/03_cancellation_vs_non_cancellation.png")
plt.close()
print("  [3/8] charts/03_cancellation_vs_non_cancellation.png")


# ════════════════════════════════════════════════════════════════════════════
# Chart 4 — Cancellation Rate by Hotel Type
# ════════════════════════════════════════════════════════════════════════════
cancel_by_hotel = (df.groupby("hotel")["is_canceled"]
                     .mean().mul(100).round(2)
                     .reindex(["City Hotel", "Resort Hotel"]))

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(cancel_by_hotel.index, cancel_by_hotel.values,
              color=COLORS_2, width=0.45, edgecolor="white", linewidth=1.2)
for bar, val in zip(bars, cancel_by_hotel.values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.4,
            f"{val}%", ha="center", va="bottom",
            fontsize=13, fontweight="bold")

# Overall average reference line
overall_rate = df["is_canceled"].mean() * 100
ax.axhline(overall_rate, linestyle="--", color="#1f2328", linewidth=1.2,
           label=f"Overall avg: {overall_rate:.1f}%")
ax.legend(frameon=False, fontsize=10)

ax.set_title("Cancellation Rate by Hotel Type")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_ylim(0, max(cancel_by_hotel.values) * 1.2)
fig.text(0.5, -0.03,
         "City Hotel has a 6.51 pp higher cancellation rate than Resort Hotel.",
         ha="center", **FONT_CAPTION)
plt.tight_layout()
plt.savefig("charts/04_cancellation_rate_by_hotel.png")
plt.close()
print("  [4/8] charts/04_cancellation_rate_by_hotel.png")


# ════════════════════════════════════════════════════════════════════════════
# Chart 5 — Bookings by Market Segment
# ════════════════════════════════════════════════════════════════════════════
seg = (df["market_segment"].value_counts()
       .sort_values(ascending=True))   # ascending so largest is at top in barh
seg_pct = (seg / len(df) * 100).round(1)
bar_colors = [BLUE if s == "Online TA" else "#90b4e8" for s in seg.index]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(seg.index, seg.values, color=bar_colors,
               edgecolor="white", linewidth=0.8, height=0.65)
for bar, val, pct in zip(bars, seg.values, seg_pct.values):
    ax.text(bar.get_width() + 200, bar.get_y() + bar.get_height() / 2,
            f"{val:,}  ({pct}%)", va="center", fontsize=9.5)

ax.set_title("Bookings by Market Segment")
ax.set_xlabel("Number of Bookings")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_xlim(0, seg.max() * 1.25)
fig.text(0.5, -0.03,
         "Online Travel Agents (TA) dominate with 59.18% of all bookings.",
         ha="center", **FONT_CAPTION)
plt.tight_layout()
plt.savefig("charts/05_bookings_by_market_segment.png")
plt.close()
print("  [5/8] charts/05_bookings_by_market_segment.png")


# ════════════════════════════════════════════════════════════════════════════
# Chart 6 — ADR by Hotel Type (box + violin)
# ════════════════════════════════════════════════════════════════════════════
df_adr = df[df["is_zero_adr"] == 0].copy()

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
fig.suptitle("Average Daily Rate (ADR) by Hotel Type", fontsize=15, fontweight="bold")

# Box plot
sns.boxplot(data=df_adr, x="hotel", y="adr", hue="hotel",
            palette=COLORS_2, legend=False,
            width=0.45, flierprops=dict(marker=".", alpha=0.3, markersize=3),
            ax=axes[0])
axes[0].set_title("Distribution (Boxplot)")
axes[0].set_xlabel("Hotel Type")
axes[0].set_ylabel("ADR (EUR)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{int(x):,}"))

# Add mean annotation
for i, hotel in enumerate(["City Hotel", "Resort Hotel"]):
    m = df_adr.loc[df_adr["hotel"] == hotel, "adr"].mean()
    axes[0].text(i, m + 5, f"Mean\n€{m:.0f}",
                 ha="center", fontsize=8.5, color="white",
                 bbox=dict(boxstyle="round,pad=0.3",
                           facecolor=COLORS_2[i], edgecolor="none", alpha=0.9))

# Violin plot (capped at 500 for readability)
df_adr_cap = df_adr[df_adr["adr"] <= 500]
sns.violinplot(data=df_adr_cap, x="hotel", y="adr", hue="hotel",
               palette=COLORS_2, legend=False,
               inner="quartile", cut=0, ax=axes[1])
axes[1].set_title("Density (Violin, ADR <= €500)")
axes[1].set_xlabel("Hotel Type")
axes[1].set_ylabel("ADR (EUR)")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{int(x):,}"))

fig.text(0.5, -0.03,
         "City Hotel mean ADR: €112.18  |  Resort Hotel mean ADR: €100.49 "
         "(rows with adr=0 excluded).",
         ha="center", **FONT_CAPTION)
plt.tight_layout()
plt.savefig("charts/06_adr_by_hotel_type.png")
plt.close()
print("  [6/8] charts/06_adr_by_hotel_type.png")


# ════════════════════════════════════════════════════════════════════════════
# Chart 7 — Average Length of Stay by Hotel Type
# ════════════════════════════════════════════════════════════════════════════
stay_by_hotel = df.groupby("hotel")["total_nights"].mean().round(2)
# Breakdown: weekend vs weekday nights
weekend_avg = df.groupby("hotel")["stays_in_weekend_nights"].mean().round(2)
weekday_avg = df.groupby("hotel")["stays_in_week_nights"].mean().round(2)

hotels = ["City Hotel", "Resort Hotel"]
x = np.arange(len(hotels))
w = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
bars1 = ax.bar(x - w/2, [weekday_avg[h] for h in hotels],
               width=w, label="Weekday Nights", color=BLUE, edgecolor="white")
bars2 = ax.bar(x + w/2, [weekend_avg[h] for h in hotels],
               width=w, label="Weekend Nights", color=PURPLE, edgecolor="white")

# Total-stay annotation above each pair
for i, hotel in enumerate(hotels):
    total = stay_by_hotel[hotel]
    ax.text(i, max(weekday_avg[hotel], weekend_avg[hotel]) + 0.12,
            f"Total avg\n{total} nights",
            ha="center", fontsize=9, fontweight="bold", color="#1f2328")

for bar in list(bars1) + list(bars2):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.04,
            f"{bar.get_height():.2f}",
            ha="center", va="bottom", fontsize=9)

ax.set_title("Average Length of Stay by Hotel Type")
ax.set_ylabel("Average Nights")
ax.set_xticks(x)
ax.set_xticklabels(hotels)
ax.set_ylim(0, max(weekday_avg.values) * 1.35)
ax.legend(frameon=False, fontsize=10)
fig.text(0.5, -0.03,
         "Resort Hotel guests stay 4.44 nights on average vs 3.15 for City Hotel.",
         ha="center", **FONT_CAPTION)
plt.tight_layout()
plt.savefig("charts/07_avg_stay_by_hotel_type.png")
plt.close()
print("  [7/8] charts/07_avg_stay_by_hotel_type.png")


# ════════════════════════════════════════════════════════════════════════════
# Chart 8 — Lead Time vs Cancellation
# ════════════════════════════════════════════════════════════════════════════
bins   = [0, 7, 30, 90, 180, 365, df["lead_time"].max() + 1]
labels_b = ["0–7", "8–30", "31–90", "91–180", "181–365", "365+"]
df["lead_bin"] = pd.cut(df["lead_time"], bins=bins, labels=labels_b, right=True)

bin_stats = (df.groupby("lead_bin", observed=True)["is_canceled"]
               .agg(["mean", "count"])
               .rename(columns={"mean": "cancel_rate", "count": "n_bookings"}))
bin_stats["cancel_rate_pct"] = (bin_stats["cancel_rate"] * 100).round(2)

fig, ax1 = plt.subplots(figsize=(10, 5))

# Bar — volume
bars = ax1.bar(bin_stats.index, bin_stats["n_bookings"],
               color=BLUE, alpha=0.65, edgecolor="white",
               linewidth=0.8, label="Number of Bookings")
ax1.set_xlabel("Lead Time (days before arrival)")
ax1.set_ylabel("Number of Bookings", color=BLUE)
ax1.tick_params(axis="y", labelcolor=BLUE)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# Secondary axis — cancellation rate line
ax2 = ax1.twinx()
ax2.plot(bin_stats.index, bin_stats["cancel_rate_pct"],
         color=RED, linewidth=2.5, marker="o", markersize=7,
         label="Cancellation Rate (%)")
for i, (idx, row) in enumerate(bin_stats.iterrows()):
    ax2.text(i, row["cancel_rate_pct"] + 1.2,
             f"{row['cancel_rate_pct']}%",
             ha="center", fontsize=9, fontweight="bold", color=RED)
ax2.set_ylabel("Cancellation Rate (%)", color=RED)
ax2.tick_params(axis="y", labelcolor=RED)
ax2.set_ylim(0, bin_stats["cancel_rate_pct"].max() * 1.25)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2,
           loc="upper left", frameon=False, fontsize=10)

ax1.set_title("Lead Time vs Cancellation Rate")
fig.text(0.5, -0.03,
         "Cancellation rate rises monotonically from 9.77% (same-week) to 41.10% (365+ days). "
         "Pearson r = 0.183.",
         ha="center", **FONT_CAPTION)
plt.tight_layout()
plt.savefig("charts/08_lead_time_vs_cancellation.png")
plt.close()
print("  [8/8] charts/08_lead_time_vs_cancellation.png")

print("\nAll 8 charts saved to the charts/ folder.")
