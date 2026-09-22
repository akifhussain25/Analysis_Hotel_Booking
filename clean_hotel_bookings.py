"""
Hotel Bookings — Data Cleaning Script
======================================
Loads hotel_bookings.csv, applies every cleaning step from the data-cleaning
plan, and writes the result to hotel_bookings_cleaned.csv.

The original file is never modified.
"""

import pandas as pd
import re

# ─────────────────────────────────────────────────────────────────────────────
# 1. LOAD
# ─────────────────────────────────────────────────────────────────────────────
INPUT_FILE  = "hotel_bookings.csv"
OUTPUT_FILE = "hotel_bookings_cleaned.csv"

df = pd.read_csv(INPUT_FILE, low_memory=False)

print("=" * 60)
print("HOTEL BOOKINGS — DATA CLEANING REPORT")
print("=" * 60)
print(f"\n[LOAD] Rows loaded  : {len(df):,}")
print(f"[LOAD] Columns      : {len(df.columns)}")

# Keep a snapshot of initial counts for reporting
initial_rows = len(df)

# ─────────────────────────────────────────────────────────────────────────────
# 2. MISSING VALUES
# ─────────────────────────────────────────────────────────────────────────────

# 2a. agent — missing means "no agent"; fill with 0
agent_missing = df["agent"].isna().sum()
df["agent"] = df["agent"].fillna(0).astype(int)
print(f"\n[MISSING] agent     : {agent_missing:,} blanks -> filled with 0")

# 2b. company — missing means "no company"; fill with 0
company_missing = df["company"].isna().sum()
df["company"] = df["company"].fillna(0).astype(int)
print(f"[MISSING] company   : {company_missing:,} blanks -> filled with 0")

# 2c. country — unknown origin; fill with "Unknown"
country_missing = df["country"].isna().sum()
df["country"] = df["country"].fillna("Unknown")
print(f"[MISSING] country   : {country_missing:,} blanks -> filled with 'Unknown'")

# 2d. children — fill with 0 (no children)
children_missing = df["children"].isna().sum()
df["children"] = df["children"].fillna(0).astype(int)
print(f"[MISSING] children  : {children_missing:,} blanks -> filled with 0")

# ─────────────────────────────────────────────────────────────────────────────
# 3. DUPLICATE ROWS
# ─────────────────────────────────────────────────────────────────────────────
# Drop exact duplicates across all columns except the row index.
# 'index' is just the original CSV row number and is not a booking identifier.
cols_for_dedup = [c for c in df.columns if c != "index"]
before_dedup = len(df)
df = df.drop_duplicates(subset=cols_for_dedup, keep="first")
dupes_removed = before_dedup - len(df)
print(f"\n[DUPES] Duplicate rows removed : {dupes_removed:,}"
      f"  ({before_dedup:,} -> {len(df):,})")

# ─────────────────────────────────────────────────────────────────────────────
# 4. INVALID / INCONSISTENT VALUES
# ─────────────────────────────────────────────────────────────────────────────

# 4a. reservation_status_date — normalise two coexisting formats:
#       • D/M/YYYY  (e.g. 1/7/2015, 12/6/2015)
#       • DD-MM-YY  (e.g. 22-04-15, 13-07-15)
#     Both are European-style (day-first).  We parse with dayfirst=True and
#     coerce any remaining failures to NaT, then report them.

def parse_mixed_dates(series: pd.Series) -> pd.Series:
    """
    Parse a date column that contains two coexisting formats:
      - D/M/YYYY   e.g. 1/7/2015, 22/12/2016
      - DD-MM-YY   e.g. 22-04-15, 13-07-16
    Returns a Series of datetime64 values, coercing unparseable entries to NaT.
    """
    def _parse_one(val):
        if pd.isna(val) or val == "nan":
            return pd.NaT
        val = str(val).strip()
        if "-" in val:
            # DD-MM-YY  -> expand 2-digit year to 4 digits (20xx)
            parts = val.split("-")
            if len(parts) == 3 and len(parts[2]) == 2:
                parts[2] = "20" + parts[2]
            val = "/".join(parts)
        # Now uniformly D/M/YYYY or DD/MM/YYYY
        try:
            return pd.to_datetime(val, dayfirst=True)
        except Exception:
            return pd.NaT

    return series.map(_parse_one)

raw_dates = df["reservation_status_date"].copy()
df["reservation_status_date"] = parse_mixed_dates(df["reservation_status_date"])
unparseable = df["reservation_status_date"].isna().sum()
print(f"\n[FORMAT] reservation_status_date : standardised to datetime"
      f"  (unparseable / coerced to NaT: {unparseable})")

# 4b. adr — negative values are impossible; replace with 0
neg_adr_mask = df["adr"] < 0
neg_adr_count = neg_adr_mask.sum()
df.loc[neg_adr_mask, "adr"] = 0
print(f"\n[INVALID] adr < 0   : {neg_adr_count} row(s) -> set to 0")

# 4c. adr == 0 on completed, non-complimentary bookings — add a flag column
#     so analysts can exclude these from revenue calculations without losing the rows.
zero_adr_flag_mask = (
    (df["adr"] == 0) &
    (df["reservation_status"] == "Check-Out") &
    (df["market_segment"] != "Complementary")
)
df["is_zero_adr"] = zero_adr_flag_mask.astype(int)
print(f"[FLAG]  is_zero_adr : {zero_adr_flag_mask.sum():,} Check-Out rows "
      f"with adr=0 flagged  (new column added)")

# 4d. meal == "Undefined" — replace with "SC" (Self Catering / no meal plan)
undefined_meal = (df["meal"] == "Undefined").sum()
df["meal"] = df["meal"].replace("Undefined", "SC")
print(f"\n[INVALID] meal='Undefined' : {undefined_meal:,} rows -> replaced with 'SC'")

# 4e. Zero-guest rows where reservation_status == "Check-Out"
#     A completed stay with zero registered guests is logically impossible.
df["_total_guests"] = df["adults"] + df["children"] + df["babies"]
zero_guest_checkout = (
    (df["_total_guests"] == 0) & (df["reservation_status"] == "Check-Out")
)
zero_guest_count = zero_guest_checkout.sum()
df = df[~zero_guest_checkout]
print(f"\n[INVALID] Zero-guest Check-Out rows dropped : {zero_guest_count:,}")

# 4f. Zero-night rows where reservation_status == "Check-Out"
#     A completed stay must have at least one night.
df["_total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
zero_night_checkout = (
    (df["_total_nights"] == 0) & (df["reservation_status"] == "Check-Out")
)
zero_night_count = zero_night_checkout.sum()
df = df[~zero_night_checkout]
print(f"[INVALID] Zero-night Check-Out rows dropped : {zero_night_count:,}")

# Drop the temporary helper columns
df = df.drop(columns=["_total_guests", "_total_nights"])

# 4g. is_canceled ↔ reservation_status — ensure logical consistency.
#     Ground truth: reservation_status.
#     Rule: if status is "Check-Out"  -> is_canceled must be 0
#           if status is "Canceled" or "No-Show" -> is_canceled must be 1
status_cancel_map = {
    "Check-Out": 0,
    "Canceled":  1,
    "No-Show":   1,
}
expected_canceled = df["reservation_status"].map(status_cancel_map)
mismatch_mask = expected_canceled.notna() & (df["is_canceled"] != expected_canceled)
mismatch_count = mismatch_mask.sum()
df.loc[mismatch_mask, "is_canceled"] = expected_canceled[mismatch_mask]
print(f"\n[INCONSISTENT] is_canceled fixed : {mismatch_count:,} rows corrected "
      f"using reservation_status as ground truth")

# 4h. adults outlier flag — group block rows (adults > 10)
#     Not dropped; flagged so individual-level analyses can exclude them.
group_block_mask = df["adults"] > 10
df["is_group_block"] = group_block_mask.astype(int)
print(f"\n[FLAG]  is_group_block : {group_block_mask.sum():,} rows with adults > 10 "
      f"flagged  (new column added)")

# ─────────────────────────────────────────────────────────────────────────────
# 5. FINAL SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
final_rows = len(df)
rows_removed = initial_rows - final_rows

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  Rows in original dataset   : {initial_rows:,}")
print(f"  Rows removed (total)       : {rows_removed:,}")
print(f"  Rows in cleaned dataset    : {final_rows:,}")
print(f"  Columns in cleaned dataset : {len(df.columns)}")
print(f"\n  New columns added:")
print(f"    • is_zero_adr    — 1 if adr=0 on a non-complimentary Check-Out")
print(f"    • is_group_block — 1 if adults > 10 (bulk group booking row)")
print(f"\n  Remaining missing values per column:")
remaining_missing = df.isnull().sum()
remaining_missing = remaining_missing[remaining_missing > 0]
if remaining_missing.empty:
    print("    None")
else:
    for col, n in remaining_missing.items():
        print(f"    {col}: {n:,}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. SAVE
# ─────────────────────────────────────────────────────────────────────────────
df.to_csv(OUTPUT_FILE, index=False)
print(f"\n[SAVE] Cleaned dataset written to: {OUTPUT_FILE}")
print("=" * 60)
