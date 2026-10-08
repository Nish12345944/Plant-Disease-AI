"""
Analyze Full PlantSeg Taxonomy vs Model 2 117-Class Taxonomy
============================================================
"""

import json
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
MODEL2_CLASS_MAPPING = PROJECT_ROOT / "data" / "processed" / "model2_classifier_class_mapping.json"
PLANTSEG_METADATA = PROJECT_ROOT / "data" / "external" / "model2_supplementary" / "plantsegv3" / "plantsegv3" / "Metadatav2.csv"
PLANTSEG_SELECTED_DIR = PROJECT_ROOT / "data" / "external" / "model2_supplementary" / "plantseg_selected"

def main():
    with open(MODEL2_CLASS_MAPPING, "r", encoding="utf-8") as f:
        m2_mapping = json.load(f)

    class_to_id = m2_mapping.get("class_to_id", m2_mapping)
    m2_classes = set(class_to_id.keys())
    print(f"Model 2 total classes: {len(m2_classes)}")

    df = pd.read_csv(PLANTSEG_METADATA)
    plantseg_diseases = sorted(df["Disease"].unique())
    print(f"PlantSeg total unique diseases: {len(plantseg_diseases)}")

    existing_folders = set([d.name for d in PLANTSEG_SELECTED_DIR.iterdir() if d.is_dir()])
    print(f"Existing folders in plantseg_selected: {len(existing_folders)}")

    matches = []
    rejected = []

    for pd_name in plantseg_diseases:
        rows = df[df["Disease"] == pd_name]
        plant = rows["Plant"].iloc[0]
        plant_clean = plant.lower().replace(" ", "_")

        # Normalize disease string
        if pd_name.lower().startswith(plant.lower()):
            dis_clean = pd_name[len(plant):].strip().replace(" ", "_").replace("-", "_")
            m2_cand = f"{plant_clean}__{dis_clean}"
        else:
            words = pd_name.split(" ")
            m2_cand = f"{words[0]}__{'_'.join(words[1:]).replace('-', '_')}"

        # Manual adjustments for specific crops or exact syntax
        # Check if direct match
        matched_m2 = None
        if m2_cand in m2_classes and m2_cand != "healthy":
            matched_m2 = m2_cand
        else:
            # Check if any m2 class matches exactly when converting underscores to spaces
            for m2c in m2_classes:
                if m2c == "healthy":
                    continue
                # E.g. 'bell_pepper__bacterial_spot' -> 'bell pepper bacterial spot'
                m2c_space = m2c.replace("__", " ").replace("_", " ")
                pd_space = pd_name.replace("_", " ").replace("-", " ")
                if m2c_space == pd_space:
                    matched_m2 = m2c
                    break

        if matched_m2:
            matches.append({
                "plantseg_disease": pd_name,
                "plant": plant,
                "model2_class": matched_m2,
                "folder_name": matched_m2.replace("__", "_"),
                "metadata_count": len(rows),
                "already_extracted": (matched_m2.replace("__", "_") in existing_folders)
            })
        else:
            if "healthy" in pd_name.lower():
                reason = "Healthy plant class (excluded from disease supplementary extraction)"
            elif plant_clean not in [c.split("__")[0] for c in m2_classes]:
                reason = f"Crop '{plant}' is not in Model 2 39-crop taxonomy"
            else:
                reason = f"Disease '{pd_name}' is not in Model 2 taxonomy for crop '{plant}'"
            rejected.append({
                "plantseg_disease": pd_name,
                "plant": plant,
                "metadata_count": len(rows),
                "reason": reason
            })

    print(f"\nExact Semantic Matches to Model 2: {len(matches)}")
    print(f"Rejected PlantSeg Diseases: {len(rejected)}")

    print("\n--- ALL EXACT MATCHES ---")
    for m in matches:
        print(f"  {m['plantseg_disease']:<35} -> {m['model2_class']:<35} | Count: {m['metadata_count']:>4} | Already: {m['already_extracted']}")

    print("\n--- ALL REJECTED DISEASES ---")
    for r in rejected:
        print(f"  {r['plantseg_disease']:<35} | Plant: {r['plant']:<15} | Count: {r['metadata_count']:>4} | Reason: {r['reason']}")

if __name__ == "__main__":
    main()
