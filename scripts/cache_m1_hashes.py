import hashlib
import json
import time
from pathlib import Path
import pandas as pd

t0 = time.time()
root = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
m1_manifest = root / "data" / "processed" / "model1_balanced_manifest.csv"
cache_file = root / "data" / "processed" / "model1_hashes_cache.json"

if cache_file.exists():
    print("Loading cached M1 hashes...")
    with open(cache_file, "r") as f:
        data = json.load(f)
else:
    print("Computing M1 hashes...")
    df = pd.read_csv(m1_manifest)
    train_h, val_h, test_h = [], [], []
    for idx, row in df.iterrows():
        p = root / "data" / "processed" / row["image_path"]
        if p.exists():
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            sp = row.get("split", "train")
            if sp == "train":
                train_h.append(h)
            elif sp == "val":
                val_h.append(h)
            elif sp == "test":
                test_h.append(h)
    data = {"train": train_h, "val": val_h, "test": test_h}
    with open(cache_file, "w") as f:
        json.dump(data, f)

print(f"M1 Hashes computed: train={len(data['train'])}, val={len(data['val'])}, test={len(data['test'])} in {time.time()-t0:.2f}s")
