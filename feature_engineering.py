import pandas as pd
import os

print("Current Working Directory:")
print(os.getcwd())

# Full path to CSV file
csv_file = r"D:\AI-Based Network Anomaly Detection using Machine Learning\network_traffic.csv"

# Load CSV
df = pd.read_csv(csv_file)

print("\nOriginal Data:")
print(df.head())

# Convert Timestamp to DateTime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Extract Time Features
df["Hour"] = df["Timestamp"].dt.hour
df["Minute"] = df["Timestamp"].dt.minute
df["Second"] = df["Timestamp"].dt.second

# Convert Protocol Numbers
protocol_map = {
    6: 0,      # TCP
    17: 1,     # UDP
    1: 2       # ICMP
}

df["Protocol"] = df["Protocol"].map(protocol_map)

# Add Label Column
# 0 = Normal Traffic
df["Label"] = 0

# Select Features for ML
features = df[
    [
        "Protocol",
        "Packet_Size",
        "Hour",
        "Minute",
        "Second",
        "Label"
    ]
]

# Create dataset folder if not exists
output_folder = r"D:\AI-Based Network Anomaly Detection using Machine Learning\dataset"

os.makedirs(output_folder, exist_ok=True)

# Save ML Dataset
output_file = os.path.join(output_folder, "ml_dataset.csv")

features.to_csv(output_file, index=False)

print("\nML Dataset Created Successfully!")
print("\nDataset Preview:")
print(features.head())

print("\nTotal Records:", len(features))

print("\nSaved To:")
print(output_file)