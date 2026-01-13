import pandas as pd
import json

# CSV files-க்கு absolute path
crop_csv_path = 'F:/AgriSens/Datasets/Crop_recommendation.csv'
fert_csv_path = 'F:/AgriSens/Datasets/Fertilizer_recommendation.csv'

# Crop Recommendation Dataset
crop_df = pd.read_csv(crop_csv_path)
crop_json = crop_df.to_json(orient='records')

with open('F:/AgriSens/AgriSens-web-app/data/crop_data.json', 'w') as f:
    f.write(crop_json)
print("Crop data JSON file created successfully.")

# Fertilizer Recommendation Dataset
fert_df = pd.read_csv(fert_csv_path)
fert_json = fert_df.to_json(orient='records')

with open('F:/AgriSens/AgriSens-web-app/data/fertilizer_data.json', 'w') as f:
    f.write(fert_json)
print("Fertilizer data JSON file created successfully.")
