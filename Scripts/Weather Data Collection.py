"""
=============================================================================
  Weather Data Extractor for Agriculture
  -----------------------------------------------------------------------
  - Reads all district CSV files from the Soil Data folder.
  - Extracts unique Block names (locations) with their District.
  - Geocodes each block (Tamil Nadu, India) using Nominatim (OSM).
  - Fetches comprehensive agriculture-relevant weather data from Open-Meteo.
  - Saves a consolidated CSV:  Data/Weather Data (District Wise)/weather_data_all_blocks.csv
  - A 15-second sleep is added between every API call to avoid rate-limiting.
=============================================================================
"""

import os
import time
import glob
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).resolve().parent
SOIL_CSV_DIR = BASE_DIR / "Data" / "Soil Data ( District Wise)" / "CSV Format"
WEATHER_DIR  = BASE_DIR / "Data" / "Weather Data (District Wise)"
WEATHER_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV   = WEATHER_DIR / "weather_data_all_blocks.csv"

# ── Date range (last 1 year — Open-Meteo free historical API) ─────────────────
END_DATE   = datetime.today().strftime("%Y-%m-%d")
START_DATE = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")

# ── Nominatim Geocoder ─────────────────────────────────────────────────────────
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
GEOCODE_HEADERS = {"User-Agent": "AgriWeatherFetcher/1.0 (agriculture-research)"}

# ── Open-Meteo Historical API ──────────────────────────────────────────────────
OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"

# All agriculture-relevant weather variables (daily — Open-Meteo Archive API)
DAILY_VARIABLES = [
    "temperature_2m_max",            # Max temperature (°C)
    "temperature_2m_min",            # Min temperature (°C)
    "temperature_2m_mean",           # Mean temperature (°C)
    "precipitation_sum",             # Total rainfall/precipitation (mm)
    "rain_sum",                      # Rain only (mm)
    "snowfall_sum",                  # Snowfall (cm) — usually 0 in Tamil Nadu
    "precipitation_hours",           # Hours of precipitation
    "wind_speed_10m_max",            # Max wind speed (km/h)
    "wind_gusts_10m_max",            # Max wind gusts (km/h)
    "wind_direction_10m_dominant",   # Dominant wind direction (°)
    "shortwave_radiation_sum",       # Solar radiation (MJ/m²)
    "et0_fao_evapotranspiration",    # Reference evapotranspiration (mm)
    "daylight_duration",             # Daylight duration (seconds)
    "sunshine_duration",             # Sunshine duration (seconds)
    "relative_humidity_2m_max",      # Max relative humidity (%)
    "relative_humidity_2m_min",      # Min relative humidity (%)
    "dewpoint_2m_max",               # Max dew point (°C)
    "dewpoint_2m_min",               # Min dew point (°C)
    "vapor_pressure_deficit_max",    # Max vapor pressure deficit (kPa)
]

# Soil variables are only available as HOURLY in the archive API.
# We fetch them separately and compute daily mean/max/min ourselves.
HOURLY_SOIL_VARIABLES = [
    "soil_temperature_0_to_7cm",     # Soil temp 0-7 cm (°C)
    "soil_moisture_0_to_7cm",        # Soil moisture 0-7 cm (m³/m³)
]

SLEEP_BETWEEN_CALLS = 15  # seconds


# ══════════════════════════════════════════════════════════════════════════════
def load_all_blocks() -> pd.DataFrame:
    """Read all soil-data CSVs and return unique (District, Block) pairs."""
    all_csv = glob.glob(str(SOIL_CSV_DIR / "*.csv"))
    if not all_csv:
        raise FileNotFoundError(f"No CSV files found in: {SOIL_CSV_DIR}")

    frames = []
    for f in all_csv:
        try:
            df = pd.read_csv(f)
            if "Block" not in df.columns or "District" not in df.columns:
                print(f"  ⚠  Skipping {os.path.basename(f)} — missing Block/District columns")
                continue
            frames.append(df[["District", "Block"]].drop_duplicates())
        except Exception as exc:
            print(f"  ✘  Could not read {os.path.basename(f)}: {exc}")

    if not frames:
        raise ValueError("No valid CSV data could be loaded.")

    combined = pd.concat(frames, ignore_index=True).drop_duplicates()
    combined["District"] = combined["District"].str.strip().str.title()
    combined["Block"]    = combined["Block"].str.strip().str.title()
    print(f"\n✔  Loaded {len(combined)} unique Block entries across {combined['District'].nunique()} districts.\n")
    return combined


# ══════════════════════════════════════════════════════════════════════════════
def geocode_block(block: str, district: str, state: str = "Tamil Nadu",
                  country: str = "India", retries: int = 3) -> tuple[float, float] | None:
    """
    Return (latitude, longitude) for a block using Nominatim.
    Tries progressively broader queries if precise match fails.
    """
    queries = [
        f"{block}, {district}, {state}, {country}",
        f"{block}, {district}, {state}",
        f"{block}, {state}, {country}",
        f"{district}, {state}, {country}",
    ]

    for query in queries:
        for attempt in range(retries):
            try:
                resp = requests.get(
                    GEOCODE_URL,
                    params={"q": query, "format": "json", "limit": 1},
                    headers=GEOCODE_HEADERS,
                    timeout=10,
                )
                resp.raise_for_status()
                data = resp.json()
                if data:
                    lat = float(data[0]["lat"])
                    lon = float(data[0]["lon"])
                    return lat, lon
                break   # empty result — try next query string
            except requests.RequestException as exc:
                print(f"    Geocode attempt {attempt+1} failed for '{query}': {exc}")
                time.sleep(5)

    return None  # could not geocode


# ══════════════════════════════════════════════════════════════════════════════
def fetch_weather(lat: float, lon: float,
                  start: str = START_DATE, end: str = END_DATE) -> pd.DataFrame | None:
    """
    Fetch daily weather data from Open-Meteo Historical Archive API.
    Returns a DataFrame with one row per day, or None on failure.
    """
    params = {
        "latitude":  lat,
        "longitude": lon,
        "start_date": start,
        "end_date":   end,
        "daily":      ",".join(DAILY_VARIABLES),
        "timezone":   "Asia/Kolkata",
    }

    try:
        resp = requests.get(OPEN_METEO_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        daily = data.get("daily", {})
        if not daily or "time" not in daily:
            return None

        df = pd.DataFrame(daily)
        df.rename(columns={"time": "date"}, inplace=True)
        return df

    except requests.RequestException as exc:
        print(f"    Open-Meteo fetch failed: {exc}")
        return None


# ══════════════════════════════════════════════════════════════════════════════
def fetch_soil_hourly(lat: float, lon: float,
                      start: str = START_DATE, end: str = END_DATE) -> pd.DataFrame | None:
    """
    Fetch hourly soil temperature & moisture from Open-Meteo Archive API,
    then resample to daily mean / max / min.
    Returns a DataFrame indexed by date, or None on failure.
    """
    params = {
        "latitude":   lat,
        "longitude":  lon,
        "start_date": start,
        "end_date":   end,
        "hourly":     ",".join(HOURLY_SOIL_VARIABLES),
        "timezone":   "Asia/Kolkata",
    }

    try:
        resp = requests.get(OPEN_METEO_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        hourly = data.get("hourly", {})
        if not hourly or "time" not in hourly:
            return None

        df_h = pd.DataFrame(hourly)
        df_h["time"] = pd.to_datetime(df_h["time"])
        df_h["date"] = df_h["time"].dt.strftime("%Y-%m-%d")

        # Resample to daily stats
        daily_rows = []
        for date, grp in df_h.groupby("date"):
            row = {"date": date}
            for col in HOURLY_SOIL_VARIABLES:
                if col in grp.columns:
                    series = grp[col].dropna()
                    row[f"{col}_mean"] = round(series.mean(), 4) if len(series) else None
                    row[f"{col}_max"]  = round(series.max(),  4) if len(series) else None
                    row[f"{col}_min"]  = round(series.min(),  4) if len(series) else None
            daily_rows.append(row)

        return pd.DataFrame(daily_rows)

    except requests.RequestException as exc:
        print(f"    Soil hourly fetch failed: {exc}")
        return None


# ══════════════════════════════════════════════════════════════════════════════
def summarise_weather(df: pd.DataFrame) -> dict:
    """
    Summarise a daily-weather DataFrame into a single-row dict of
    annual / seasonal statistics useful for agriculture.
    """
    s = {}

    def safe(col, fn):
        try:
            return round(fn(df[col].dropna()), 4) if col in df.columns else None
        except Exception:
            return None

    s["temp_max_mean"]       = safe("temperature_2m_max",  lambda x: x.mean())
    s["temp_min_mean"]       = safe("temperature_2m_min",  lambda x: x.mean())
    s["temp_mean_annual"]    = safe("temperature_2m_mean", lambda x: x.mean())
    s["temp_max_absolute"]   = safe("temperature_2m_max",  lambda x: x.max())
    s["temp_min_absolute"]   = safe("temperature_2m_min",  lambda x: x.min())

    s["total_rainfall_mm"]         = safe("precipitation_sum",  lambda x: x.sum())
    s["avg_daily_rainfall_mm"]     = safe("precipitation_sum",  lambda x: x.mean())
    s["max_daily_rainfall_mm"]     = safe("precipitation_sum",  lambda x: x.max())
    s["total_rain_mm"]             = safe("rain_sum",            lambda x: x.sum())
    s["total_precip_hours"]        = safe("precipitation_hours", lambda x: x.sum())
    s["rainy_days"]                = (
        int((df["precipitation_sum"].dropna() > 0.1).sum())
        if "precipitation_sum" in df.columns else None
    )

    s["humidity_max_mean"]   = safe("relative_humidity_2m_max", lambda x: x.mean())
    s["humidity_min_mean"]   = safe("relative_humidity_2m_min", lambda x: x.mean())
    s["dewpoint_max_mean"]   = safe("dewpoint_2m_max",          lambda x: x.mean())
    s["dewpoint_min_mean"]   = safe("dewpoint_2m_min",          lambda x: x.mean())

    s["wind_speed_max_mean"]      = safe("wind_speed_10m_max",           lambda x: x.mean())
    s["wind_gusts_max_mean"]      = safe("wind_gusts_10m_max",           lambda x: x.mean())
    s["wind_direction_dominant"]  = safe("wind_direction_10m_dominant",  lambda x: x.mode()[0] if len(x) else None)

    s["solar_radiation_mean"]     = safe("shortwave_radiation_sum",      lambda x: x.mean())
    s["et0_annual_mm"]            = safe("et0_fao_evapotranspiration",   lambda x: x.sum())
    s["et0_daily_mean_mm"]        = safe("et0_fao_evapotranspiration",   lambda x: x.mean())
    s["sunshine_hours_daily_mean"]= safe("sunshine_duration",            lambda x: (x / 3600).mean())
    s["daylight_hours_daily_mean"]= safe("daylight_duration",            lambda x: (x / 3600).mean())

    # Soil columns come from hourly resampling → col_mean / col_max / col_min
    s["soil_temp_0_7cm_mean"]     = safe("soil_temperature_0_to_7cm_mean", lambda x: x.mean())
    s["soil_temp_0_7cm_max_mean"] = safe("soil_temperature_0_to_7cm_max",  lambda x: x.mean())
    s["soil_temp_0_7cm_min_mean"] = safe("soil_temperature_0_to_7cm_min",  lambda x: x.mean())
    s["soil_moisture_0_7cm_mean"] = safe("soil_moisture_0_to_7cm_mean",    lambda x: x.mean())
    s["soil_moisture_0_7cm_max"]  = safe("soil_moisture_0_to_7cm_max",     lambda x: x.mean())
    s["soil_moisture_0_7cm_min"]  = safe("soil_moisture_0_to_7cm_min",     lambda x: x.mean())

    s["vapor_pressure_deficit_max_mean"] = safe("vapor_pressure_deficit_max", lambda x: x.mean())

    return s


# ══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 70)
    print("   Agriculture Weather Data Extractor  —  Open-Meteo API")
    print(f"   Period: {START_DATE}  →  {END_DATE}")
    print(f"   Sleep between API calls: {SLEEP_BETWEEN_CALLS}s")
    print("=" * 70)

    # 1. Load all blocks
    blocks_df = load_all_blocks()

    results = []
    total = len(blocks_df)

    for idx, row in blocks_df.iterrows():
        district = row["District"]
        block    = row["Block"]
        print(f"\n[{idx+1}/{total}]  {block}  ({district})")

        # ── Step 1: Geocode ────────────────────────────────────────────────
        print(f"  → Geocoding …")
        coords = geocode_block(block, district)
        time.sleep(1)   # be polite to Nominatim

        if coords is None:
            print(f"  ✘  Could not geocode '{block}' — skipping.")
            results.append({
                "district": district, "block": block,
                "latitude": None, "longitude": None,
                "status": "geocode_failed"
            })
            continue

        lat, lon = coords
        print(f"  ✔  Coordinates: {lat:.4f}, {lon:.4f}")

        # ── Step 2: Wait before Open-Meteo call ───────────────────────────
        print(f"  → Waiting {SLEEP_BETWEEN_CALLS}s before weather fetch …")
        time.sleep(SLEEP_BETWEEN_CALLS)

        # ── Step 3: Fetch daily weather ────────────────────────────────────
        print(f"  → Fetching daily weather data from Open-Meteo …")
        weather_df = fetch_weather(lat, lon)

        if weather_df is None:
            print(f"  ✘  Weather fetch failed for '{block}'.")
            results.append({
                "district": district, "block": block,
                "latitude": lat, "longitude": lon,
                "status": "weather_failed"
            })
            continue

        # ── Step 3b: Wait then fetch hourly soil data ──────────────────────
        print(f"  → Waiting {SLEEP_BETWEEN_CALLS}s before soil fetch …")
        time.sleep(SLEEP_BETWEEN_CALLS)

        print(f"  → Fetching hourly soil data from Open-Meteo …")
        soil_df = fetch_soil_hourly(lat, lon)
        if soil_df is not None:
            weather_df = weather_df.merge(soil_df, on="date", how="left")
            print(f"  ✔  Soil data merged.")
        else:
            print(f"  ⚠  Soil data unavailable — continuing without it.")

        # ── Step 4: Summarise ──────────────────────────────────────────────
        summary = summarise_weather(weather_df)

        # Save per-block raw daily CSV as well
        raw_dir = WEATHER_DIR / "Raw Daily"
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_csv = raw_dir / f"{district}_{block}_daily.csv"
        weather_df.insert(0, "block",    block)
        weather_df.insert(0, "district", district)
        weather_df.to_csv(raw_csv, index=False, encoding="utf-8")
        print(f"  ✔  Raw daily data saved → {raw_csv.name}")

        record = {
            "district":  district,
            "block":     block,
            "latitude":  lat,
            "longitude": lon,
            "data_start": START_DATE,
            "data_end":   END_DATE,
            "status":    "success",
            **summary,
        }
        results.append(record)
        print(f"  ✔  Summary computed.")

    # ── Save consolidated CSV ──────────────────────────────────────────────────
    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print("\n" + "=" * 70)
    print(f"✔  Consolidated weather summary saved to:")
    print(f"   {OUTPUT_CSV}")
    print(f"   Rows: {len(out_df)}   |   Columns: {len(out_df.columns)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
