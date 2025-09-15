# knowledge_engine.py
import json
from pathlib import Path
from datetime import datetime

# Set the path to your dataset folder
DATA_DIR = Path(__file__).resolve().parent.parent / "AgriSens-web-app" / "data"

def load_json(fname):
    with open(DATA_DIR / fname, "r", encoding="utf-8") as f:
        return json.load(f)

class KnowledgeEngine:
    def __init__(self):
        self.fertilizers = load_json("fertilizer_data.json")
        self.crop_calendar = load_json("crop_calendar.json")
        self.pest_data = load_json("pest_data.json")
        self.best_practices = load_json("best_practices.json")

    def recommend(self, crop, soil, temp, humidity, lang="en"):
        rec = {}
        crop_lower = crop.lower()
        soil_lower = soil.lower()

        # Fertilizer recommendation
        fert_list = [
            f.copy() for f in self.fertilizers["data"]
            if f["CropType"].lower() == crop_lower and f["SoilType"].lower() == soil_lower
        ]
        for f in fert_list:
            f["Fertilizer Name"] = self.fertilizers["labels"]["fertilizers"].get(f["Fertilizer"], {}).get(lang, f["Fertilizer"])
        rec["fertilizers"] = fert_list

        # Crop calendar
        month = datetime.now().strftime("%B")
        month_stage = self.crop_calendar.get(crop, {}).get(month, {})
        rec["crop_stage"] = month_stage.get(lang, "Unknown")

        # Pest alerts
        pests = [p.copy() for p in self.pest_data["data"] if p["Crop"].lower() == crop_lower]
        for p in pests:
            pest_name = p["Pest"]
            if lang in self.pest_data["labels"]["pests"].get(pest_name, {}):
                p["Pest"] = self.pest_data["labels"]["pests"][pest_name][lang]
        rec["pest_risk"] = pests

        # Best practices
        best = self.best_practices.get(crop, {})
        rec["best_practices"] = best.get(lang, "No data available")

        return rec
