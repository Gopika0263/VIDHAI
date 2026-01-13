# knowledge_engine.py
import json
from pathlib import Path
from datetime import datetime

# Set the path to your dataset folder
DATA_DIR = Path(__file__).resolve().parent.parent / "VIDHAI-web-app" / "data"

def load_json(fname):
    """Load JSON file from the data directory."""
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

        # --------------------------
        # Fertilizer recommendation
        # --------------------------
        fert_list = [
            f.copy() for f in self.fertilizers.get("data", [])
            if f.get("CropType", "").lower() == crop_lower and f.get("SoilType", "").lower() == soil_lower
        ]
        for f in fert_list:
            f_name = f.get("Fertilizer", "")
            f["Fertilizer Name"] = (
                self.fertilizers.get("labels", {})
                .get("fertilizers", {})
                .get(f_name, {})
                .get(lang, f_name)
            )
        rec["fertilizers"] = fert_list

        # --------------------------
        # Crop calendar
        # --------------------------
        month = datetime.now().strftime("%B")
        month_stage = self.crop_calendar.get(crop, {}).get(month, {})
        rec["crop_stage"] = month_stage.get(lang, "Unknown")

        # --------------------------
        # Pest alerts
        # --------------------------
        pests = [
            {
                "Crop": p.get("Crop"),
                "Pest": p.get("Pest") if lang == "en" else p.get("Pest_ml", p.get("Pest")),
                "Solution": p.get("Solution") if lang == "en" else p.get("Solution_ml", p.get("Solution"))
            }
            for p in self.pest_data.get("data", [])
            if p.get("Crop", "").lower() == crop_lower
        ]
        rec["pest_risk"] = pests

        # --------------------------
        # Best practices
        # --------------------------
        best = self.best_practices.get(crop, {})
        rec["best_practices"] = best.get(lang, "No data available")

        return rec
