import numpy as np
import json
from sklearn.preprocessing import OneHotEncoder

# === Step 1: Normalize numerical features ===
def normalize_college_numerics(college):
    # Helper function to safely normalize a value
    def safe_normalize(value, max_value):
        if value is None:
            return 0.0  # Default to 0 for missing values
        return float(value) / max_value

    return np.array([
        safe_normalize(college.get("admission_rate"), 1.0),
        safe_normalize(college.get("sat_reading"), 800),
        safe_normalize(college.get("sat_math"), 800),
        safe_normalize(college.get("act_composite"), 36),
        safe_normalize(college.get("graduation_rate"), 1.0),
        safe_normalize(college.get("cost_of_attendance"), 80000),
        safe_normalize(college.get("net_price"), 80000),
        safe_normalize(college.get("tuition_in"), 80000),
        safe_normalize(college.get("tuition_out"), 80000),
        safe_normalize(college.get("size"), 100000),
        safe_normalize(college.get("latitude", 0) + 90, 180),
        safe_normalize(college.get("longitude", 0) + 180, 360)
    ])

# === Step 2: Encode categorical values ===
def encode_categoricals(college, encoder):
    inputs = [[
        college["carnegie_desc"],
        college["locale_desc"],
        college["state"]
    ]]
    return encoder.transform(inputs)

# === Step 3: Combine numeric + categorical vectors ===
def vectorize_college(college, encoder):
    numeric = normalize_college_numerics(college)
    categorical = encode_categoricals(college, encoder).flatten()
    return np.concatenate([numeric, categorical])


# === Vectorize a sample college for testing ===
sample_college = {
    "name": "Alabama A & M University",
    "city": "Normal",
    "state": "AL",
    "locate_type": 12.0,
    "latitude": 34.783368,
    "longitude": -86.568502,
    "carnegie": 10.0,
    "admission_rate": 0.6622,
    "sat_reading": 475.0,
    "sat_math": 460.0,
    "act_composite": 18.0,
    "size": 5726.0,
    "cost_of_attendance": 23751.0,
    "tuition_in": 10024.0,
    "tuition_out": 18634.0,
    "graduation_rate": 0.2874,
    "net_price": 14559.0,
    "carnegie_desc": "Full‑time four‑year, selective, lower transfer‑in",
    "locale_desc": "City: population between 100,000 and 249,999"
}

# === Load full dataset to fit encoder ===
with open('colleges.json', 'r') as f:
    colleges = json.load(f)

carnegie_list = [c['carnegie_desc'] for c in colleges]
locale_list = [c['locale_desc'] for c in colleges]
state_list = [c['state'] for c in colleges]
combined_categories = list(zip(carnegie_list, locale_list, state_list))

encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoder.fit(combined_categories)

# === Vectorize the sample college ===
college_vector = vectorize_college(sample_college, encoder)
print("Vector shape:", college_vector.shape)
print("Vector:", college_vector)

# === Vectorize all colleges and save ===
college_data = []  # List to store all college information

for college in colleges:
    try:
        vec = vectorize_college(college, encoder)
        college_data.append({
            "name": college['name'],
            "city": college.get('city', ''),
            "state": college.get('state', ''),
            "locate_type": college.get('locate_type', 0.0),
            "latitude": college.get('latitude', 0.0),
            "longitude": college.get('longitude', 0.0),
            "carnegie": college.get('carnegie', 0.0),
            "admission_rate": college.get('admission_rate', 0.0),
            "sat_reading": college.get('sat_reading', 0.0),
            "sat_math": college.get('sat_math', 0.0),
            "act_composite": college.get('act_composite', 0.0),
            "size": college.get('size', 0.0),
            "cost_of_attendance": college.get('cost_of_attendance', 0.0),
            "tuition_in": college.get('tuition_in', 0.0),
            "tuition_out": college.get('tuition_out', 0.0),
            "graduation_rate": college.get('graduation_rate', 0.0),
            "net_price": college.get('net_price', 0.0),
            "carnegie_desc": college.get('carnegie_desc', ''),
            "locale_desc": college.get('locale_desc', ''),
            "vector": vec.tolist()  # Convert numpy array to list for JSON serialization
        })
    except Exception as e:
        print(f"Skipping {college.get('name', 'Unknown')} due to error: {e}")

# Save numpy array of just the vectors for machine learning purposes
vectors = np.array([data["vector"] for data in college_data])
np.save("college_vectors.npy", vectors)

# Save detailed college information to JSON
with open("college_vectors.json", "w") as f:
    json.dump(college_data, f, indent=2)

# Create JavaScript export with college data - export array directly
with open("colleges.js", "w") as f:
    f.write("export const colleges = ")
    json.dump(college_data, f, indent=2)

print(f"\n✅ Saved {len(college_data)} colleges with vectors to 'college_vectors.json' and 'colleges.js'")
print(f"✅ Saved raw vectors to 'college_vectors.npy'")
