import pandas as pd

# Specify only the columns you need
cols = [
    "INSTNM", "CITY", "STABBR", "LATITUDE", "LONGITUDE", "INSTURL",
    "CCUGPROF", "LOCALE", "ADM_RATE", "SATVRMID", "SATMTMID",
    "ACTCMMID", "UGDS", "NPT4_PUB", "NPT4_PRIV", "COSTT4_A",
    "TUITIONFEE_IN", "TUITIONFEE_OUT", "C150_4",
]

# Read just those columns
df = pd.read_csv("college_data.csv", usecols=cols)

# Rename to convenient field names
df = df.rename(columns={
    "INSTNM": "name",
    "CITY": "city",
    "STABBR": "state",
    "LATITUDE": "latitude",
    "LONGITUDE": "longitude",
    "INSTURL": "url",
    "CCUGPROF": "carnegie",
    "LOCALE": "locate_type",
    "ADM_RATE": "admission_rate",
    "SATVRMID": "sat_reading",
    "SATMTMID": "sat_math",
    "ACTCMMID": "act_composite",
    "UGDS": "size",
    "NPT4_PUB": "net_price_public",
    "NPT4_PRIV": "net_price_private",
    "COSTT4_A": "cost_of_attendance",
    "TUITIONFEE_IN": "tuition_in",
    "TUITIONFEE_OUT": "tuition_out",
    "C150_4": "graduation_rate",
})

# Create a unified 'net_price' field
df["net_price"] = df["net_price_public"].fillna(df["net_price_private"])

# Drop the two original columns
df = df.drop(columns=["net_price_public", "net_price_private"])

# Define Carnegie size classification descriptions
carnegie_map = {
    1:  "Higher part‑time two‑year (associate’s degrees with 60 percent or more part‑time students)",
    2:  "Mixed part/full‑time two‑year (associate’s degrees with 40 to 59 percent part‑time students)",
    3:  "Medium full‑time two‑year (associate’s degrees with 10 to 39 percent part‑time students)",
    4:  "Higher full‑time two‑year (associate’s degrees with fewer than 10 percent part‑time students)",
    5:  "Higher part‑time four‑year (bachelor’s degrees with 40 percent or more part‑time students)",
    6:  "Medium full‑time four‑year inclusive (bachelor’s degrees with 60 to 79 percent full‑time students)",
    7:  "Medium full‑time four‑year, selective, lower transfer‑in",
    8:  "Medium full‑time four‑year, selective, higher transfer‑in",
    9:  "Full‑time four‑year inclusive (bachelor’s degrees with 80 percent or more full‑time students)",
    10: "Full‑time four‑year, selective, lower transfer‑in",
    11: "Full‑time four‑year, selective, higher transfer‑in",
    12: "Full‑time four‑year more selective, lower transfer‑in",
    13: "Full‑time four‑year more selective, higher transfer‑in",
    14: "Not classified or not applicable"
}

# Define Locale codes descriptions
locale_map = {
    11: "City: population of 250,000 or more",
    12: "City: population between 100,000 and 249,999",
    13: "City: population under 100,000",
    21: "Suburb in urbanized area with population of 250,000 or more",
    22: "Suburb in urbanized area with population between 100,000 and 249,999",
    23: "Suburb in urbanized area with population under 100,000",
    31: "Town on the fringe (within 10 miles of an urbanized area)",
    32: "Town at a distance (10 to 35 miles from an urbanized area)",
    33: "Remote town (more than 35 miles from an urbanized area)",
    41: "Rural fringe (within 5 miles of an urbanized area)",
    42: "Rural distant (5 to 25 miles from an urbanized area)",
    43: "Rural remote (more than 25 miles from an urbanized area)"
}

# Map codes to human-readable descriptions
df["carnegie_desc"] = df["carnegie"].map(carnegie_map)
df["locale_desc"]  = df["locate_type"].map(locale_map)

# Export to JSON with one record per line, pretty‑printed
df.to_json("colleges.json", orient="records", indent=2)

print(f"Exported {len(df)} records to colleges.json")
