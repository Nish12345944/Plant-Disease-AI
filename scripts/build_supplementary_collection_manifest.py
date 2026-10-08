"""
Generate Model 2 Supplementary Dataset Collection Manifest
==========================================================
Constructs a fine-grained, crop-stratified supplementary collection manifest based on
Model 2 error analysis and test performance.

Outputs:
- reports/model2_classifier/supplementary_collection_manifest.csv
- reports/model2_classifier/supplementary_collection_manifest.md
- reports/model2_classifier/supplementary_collection_summary.json
"""

import os
import sys
import csv
import json
from pathlib import Path
from collections import Counter, defaultdict

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
ERROR_ANALYSIS_CSV = PROJECT_ROOT / "reports" / "model2_classifier" / "model2_error_analysis.csv"
REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_classifier"

TARGET_TRAIN_COUNT = 100

def generate_manifest():
    print("==================================================", flush=True)
    print("BUILDING SUPPLEMENTARY DATASET COLLECTION MANIFEST", flush=True)
    print("==================================================", flush=True)

    if not ERROR_ANALYSIS_CSV.exists():
        print(f"Error: {ERROR_ANALYSIS_CSV} not found!")
        sys.exit(1)

    all_rows = []
    with open(ERROR_ANALYSIS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            all_rows.append(r)

    # Process all disease classes
    manifest_entries = []
    for r in all_rows:
        if r["is_healthy"] == "True" or r["class_name"] == "healthy":
            continue

        c_name = r["class_name"]
        crop = r["crop"]
        tr_cnt = int(r["train_support"])
        va_cnt = int(r["val_support"])
        te_cnt = int(r["test_support"])
        prec = float(r["precision"])
        rec = float(r["recall"])
        f1 = float(r["f1_score"])

        # Priority categorization based on strict thresholds:
        # CRITICAL: F1 < 0.40 -> target 100
        # HIGH: 0.40 <= F1 < 0.60 -> target 100
        # MEDIUM: 0.60 <= F1 < 0.75 -> target 100
        # LOW: F1 >= 0.75 -> no mandatory collection
        if f1 < 0.40:
            priority = "CRITICAL"
            target_train = TARGET_TRAIN_COUNT
            additional = max(0, target_train - tr_cnt)
            # If tr_cnt is already >= 100 but F1 < 0.40, recommend 30 hard diagnostic examples
            if additional == 0:
                additional = 30
                target_train = tr_cnt + 30
        elif f1 < 0.60:
            priority = "HIGH"
            target_train = TARGET_TRAIN_COUNT
            additional = max(0, target_train - tr_cnt)
            if additional == 0:
                additional = 25
                target_train = tr_cnt + 25
        elif f1 < 0.75:
            priority = "MEDIUM"
            target_train = TARGET_TRAIN_COUNT
            additional = max(0, target_train - tr_cnt)
            if additional == 0:
                additional = 20
                target_train = tr_cnt + 20
        else:
            priority = "LOW"
            target_train = tr_cnt
            additional = 0

        manifest_entries.append({
            "class_name": c_name,
            "crop": crop,
            "current_train_count": tr_cnt,
            "current_val_count": va_cnt,
            "current_test_count": te_cnt,
            "test_precision": prec,
            "test_recall": rec,
            "test_f1": f1,
            "priority": priority,
            "recommended_target_train_count": target_train,
            "additional_images_needed": additional,
            "top_confusion_targets": r.get("top_confusion_targets", "")
        })

    # Sort entries by priority order and then worst F1 first
    priority_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    manifest_entries.sort(key=lambda x: (priority_rank[x["priority"]], x["test_f1"], x["test_recall"]))

    # Output CSV: supplementary_collection_manifest.csv
    csv_path = REPORTS_DIR / "supplementary_collection_manifest.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "class_name", "crop", "current_train_count", "current_val_count", "current_test_count",
            "test_precision", "test_recall", "test_f1", "priority",
            "recommended_target_train_count", "additional_images_needed", "top_confusion_targets"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in manifest_entries:
            writer.writerow({
                "class_name": entry["class_name"],
                "crop": entry["crop"],
                "current_train_count": entry["current_train_count"],
                "current_val_count": entry["current_val_count"],
                "current_test_count": entry["current_test_count"],
                "test_precision": f"{entry['test_precision']:.4f}",
                "test_recall": f"{entry['test_recall']:.4f}",
                "test_f1": f"{entry['test_f1']:.4f}",
                "priority": entry["priority"],
                "recommended_target_train_count": entry["recommended_target_train_count"],
                "additional_images_needed": entry["additional_images_needed"],
                "top_confusion_targets": entry["top_confusion_targets"]
            })
    print(f"Saved supplementary collection CSV: {csv_path}", flush=True)

    # Compile Summary Metrics
    critical_list = [e for e in manifest_entries if e["priority"] == "CRITICAL"]
    high_list = [e for e in manifest_entries if e["priority"] == "HIGH"]
    medium_list = [e for e in manifest_entries if e["priority"] == "MEDIUM"]
    low_list = [e for e in manifest_entries if e["priority"] == "LOW"]

    total_additional_needed = sum(e["additional_images_needed"] for e in manifest_entries)
    critical_additional = sum(e["additional_images_needed"] for e in critical_list)
    high_additional = sum(e["additional_images_needed"] for e in high_list)
    medium_additional = sum(e["additional_images_needed"] for e in medium_list)

    # Specific crop inspection
    ginger_list = [e for e in manifest_entries if e["crop"] == "Ginger"]
    banana_list = [e for e in manifest_entries if e["crop"] == "Banana"]
    garlic_list = [e for e in manifest_entries if e["crop"] == "Garlic"]

    # Onion future taxonomy expansion definition
    onion_future_classes = [
        {"class_name": "onion__purple_blotch", "disease": "Purple Blotch (Alternaria porri)", "target_images": 100, "priority": "HIGH_FUTURE"},
        {"class_name": "onion__downy_mildew", "disease": "Downy Mildew (Peronospora destructor)", "target_images": 100, "priority": "HIGH_FUTURE"},
        {"class_name": "onion__black_mold", "disease": "Black Mold (Aspergillus niger)", "target_images": 100, "priority": "MEDIUM_FUTURE"},
        {"class_name": "onion__stemphylium_leaf_blight", "disease": "Stemphylium Leaf Blight (Stemphylium vesicarium)", "target_images": 100, "priority": "HIGH_FUTURE"},
        {"class_name": "onion__bacterial_soft_rot", "disease": "Bacterial Soft Rot (Pectobacterium carotovorum)", "target_images": 80, "priority": "MEDIUM_FUTURE"},
        {"class_name": "healthy", "disease": "Onion Clean Foliage / Bulbs", "target_images": 150, "priority": "MANDATORY_FUTURE"}
    ]

    # Hard-example confusion pairs definition
    hard_confusion_pairs = [
        {
            "pair": "Tomato Bacterial Leaf Spot ↔ Tomato Septoria Leaf Spot",
            "class_a": "tomato__bacterial_leaf_spot",
            "class_b": "tomato__septoria_leaf_spot",
            "crop": "Tomato",
            "mutual_errors": 8,
            "diagnostic_challenge": "Both produce small, pinpoint circular dark necrotic lesions with yellow halos on tomato foliage.",
            "collection_strategy": "Collect high-resolution macro-photography capturing mature lesions with pycnidia (black dots in center for Septoria) vs water-soaked angular borders (Bacterial Spot)."
        },
        {
            "pair": "Bean Angular Leaf Spot ↔ Bean Rust",
            "class_a": "bean__angular_leaf_spot",
            "class_b": "bean__rust",
            "crop": "Bean",
            "mutual_errors": 8,
            "diagnostic_challenge": "Both present as angular or circular reddish-brown necrotic spots across Phaseolus foliage.",
            "collection_strategy": "Collect distinct underside foliar imagery emphasizing raised powdery rust urediniospores vs vein-delimited angular necrotic patches."
        },
        {
            "pair": "Wheat Leaf Rust ↔ Wheat Stripe Rust",
            "class_a": "wheat__leaf_rust",
            "class_b": "wheat__stripe_rust",
            "crop": "Wheat",
            "mutual_errors": 6,
            "diagnostic_challenge": "Early stage uredinial pustules exhibit overlapping orange-brown discoloration before distinct striping occurs.",
            "collection_strategy": "Collect field images showing elongated linear stripe patterns along leaf veins (Stripe Rust) vs randomly scattered oval pustules (Leaf Rust)."
        },
        {
            "pair": "Corn Gray Leaf Spot ↔ Corn Rust",
            "class_a": "corn__gray_leaf_spot",
            "class_b": "corn__rust",
            "crop": "Corn",
            "mutual_errors": 4,
            "diagnostic_challenge": "Lesions on maize foliage can appear similar in early stages under bright outdoor lighting.",
            "collection_strategy": "Collect mature rectangular vein-bounded gray-brown lesions (Gray Leaf Spot) vs raised cinnamon-brown pustules that rupture epidermal tissue (Rust)."
        },
        {
            "pair": "Soybean Bacterial Blight ↔ Soybean Rust",
            "class_a": "soybean__bacterial_blight",
            "class_b": "soybean__rust",
            "crop": "Soybean",
            "mutual_errors": 4,
            "diagnostic_challenge": "Small angular brown lesions on Glycine max leaves overlap visually in low contrast frames.",
            "collection_strategy": "Collect backlit leaves highlighting translucent yellow water-soaked halos (Bacterial Blight) vs abaxial surface raised pustules (Soybean Rust)."
        }
    ]

    summary_data = {
        "manifest_date": "2026-10-07",
        "baseline_metrics": {
            "test_accuracy": 0.8429,
            "test_top3_accuracy": 0.9457,
            "test_macro_f1": 0.6101,
            "disease_only_macro_f1": 0.6015,
            "healthy_f1": 0.9924
        },
        "collection_summary": {
            "total_disease_classes": len(manifest_entries),
            "critical_priority_classes": len(critical_list),
            "high_priority_classes": len(high_list),
            "medium_priority_classes": len(medium_list),
            "low_priority_classes": len(low_list),
            "total_additional_images_recommended": total_additional_needed,
            "critical_tier_images": critical_additional,
            "high_tier_images": high_additional,
            "medium_tier_images": medium_additional
        },
        "crop_specific_analyses": {
            "ginger": ginger_list,
            "banana": banana_list,
            "garlic": garlic_list
        },
        "hard_confusion_pairs": hard_confusion_pairs,
        "onion_future_taxonomy": onion_future_classes
    }

    # Output JSON: supplementary_collection_summary.json
    json_path = REPORTS_DIR / "supplementary_collection_summary.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)
    print(f"Saved supplementary collection JSON: {json_path}", flush=True)

    # Output Markdown: supplementary_collection_manifest.md
    md_path = REPORTS_DIR / "supplementary_collection_manifest.md"
    generate_markdown_manifest_report(
        md_path, critical_list, high_list, medium_list, low_list,
        ginger_list, banana_list, garlic_list, onion_future_classes,
        hard_confusion_pairs, total_additional_needed, critical_additional,
        high_additional, medium_additional
    )
    print(f"Saved supplementary collection Markdown: {md_path}", flush=True)

    # Print Summary to Terminal
    print("\n==================================================")
    print("SUPPLEMENTARY DATASET COLLECTION MANIFEST SUMMARY")
    print("==================================================")
    print(f"TOTAL DISEASE CLASSES AUDITED      : {len(manifest_entries)}")
    print(f"CRITICAL PRIORITY (F1 < 0.40)      : {len(critical_list):>2} classes -> Target: +{critical_additional:,} genuine images")
    print(f"HIGH PRIORITY     (0.40 <= F1 < 0.60): {len(high_list):>2} classes -> Target: +{high_additional:,} genuine images")
    print(f"MEDIUM PRIORITY   (0.60 <= F1 < 0.75): {len(medium_list):>2} classes -> Target: +{medium_additional:,} genuine images")
    print(f"LOW PRIORITY      (F1 >= 0.75)     : {len(low_list):>2} classes -> No mandatory collection needed")
    print(f"TOTAL ADDITIONAL IMAGES RECOMMENDED: +{total_additional_needed:,} genuine images")

def generate_markdown_manifest_report(
    report_path: Path, critical_list: list, high_list: list, medium_list: list, low_list: list,
    ginger_list: list, banana_list: list, garlic_list: list, onion_future: list,
    hard_pairs: list, total_needed: int, crit_needed: int, high_needed: int, med_needed: int
):
    lines = [
        "# Model 2 Disease Classifier: Targeted Supplementary Dataset Collection Manifest",
        "",
        "**Date:** 2026-10-07  ",
        "**Module:** Model 2 EfficientNet-B2 Supplementary Collection Strategy  ",
        "**Baseline Performance:** Top-1 Accuracy: **84.29%**, Top-3: **94.57%**, Macro F1: **61.01%**, Healthy F1: **99.24%**  ",
        "**Data Policy:** Strictly genuine, real-world, unblemished/diseased plant photography (No synthetic data, no artificial duplication).  ",
        "",
        "---",
        "",
        "## 1. Executive Summary & Collection Quotas",
        "",
        "```",
        f"TOTAL DISEASE CLASSES IN TAXONOMY   : 116 disease classes",
        f"CRITICAL PRIORITY CLASSES (F1 < 0.40): {len(critical_list)} classes (+{crit_needed:,} images)",
        f"HIGH PRIORITY CLASSES (0.40 <= F1 < 0.60): {len(high_list)} classes (+{high_needed:,} images)",
        f"MEDIUM PRIORITY CLASSES (0.60 <= F1 < 0.75): {len(medium_list)} classes (+{med_needed:,} images)",
        f"LOW PRIORITY CLASSES (F1 >= 0.75)   : {len(low_list)} classes (Fully sufficient; 0 images required)",
        f"TOTAL ADDITIONAL IMAGES RECOMMENDED : +{total_needed:,} genuine field/leaf images",
        "```",
        "",
        "---",
        "",
        "## 2. CRITICAL Priority Tier (Test F1 < 0.40) — Target: 100 Train Images",
        "",
        "These 20 classes suffer from severe data scarcity (<25 training images) or high confusion, leading to low test recall. Expanding these classes to 100 images will yield the largest gain in macro F1.",
        "",
        "| # | Class Name | Crop | Train | Val | Test | Precision | Recall | Test F1 | Target Train | Additional Needed |",
        "|---|---|---|---|---|---|---|---|---|---|---|"
    ]

    for idx, e in enumerate(critical_list, 1):
        lines.append(
            f"| {idx} | `{e['class_name']}` | **{e['crop']}** | {e['current_train_count']} | {e['current_val_count']} | {e['current_test_count']} | "
            f"{e['test_precision']*100:.1f}% | {e['test_recall']*100:.1f}% | **{e['test_f1']*100:.1f}%** | {e['recommended_target_train_count']} | **+{e['additional_images_needed']}** |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. HIGH Priority Tier (0.40 ≤ Test F1 < 0.60) — Target: 100 Train Images",
        "",
        "These 29 classes exhibit moderate baseline signal (40–59% F1). Expanding to 100 authentic images will stabilize intra-class variation and eliminate borderline misclassifications.",
        "",
        "| # | Class Name | Crop | Train | Val | Test | Precision | Recall | Test F1 | Target Train | Additional Needed |",
        "|---|---|---|---|---|---|---|---|---|---|---|"
    ])

    for idx, e in enumerate(high_list, 1):
        lines.append(
            f"| {idx} | `{e['class_name']}` | **{e['crop']}** | {e['current_train_count']} | {e['current_val_count']} | {e['current_test_count']} | "
            f"{e['test_precision']*100:.1f}% | {e['test_recall']*100:.1f}% | **{e['test_f1']*100:.1f}%** | {e['recommended_target_train_count']} | **+{e['additional_images_needed']}** |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 4. MEDIUM Priority Tier (0.60 ≤ Test F1 < 0.75) — Target: 100 Train Images",
        "",
        "These 21 classes perform solidly (60–74% F1). Supplementary collection brings them to the benchmark tier (≥75% F1).",
        "",
        "| # | Class Name | Crop | Train | Val | Test | Precision | Recall | Test F1 | Target Train | Additional Needed |",
        "|---|---|---|---|---|---|---|---|---|---|---|"
    ])

    for idx, e in enumerate(medium_list, 1):
        lines.append(
            f"| {idx} | `{e['class_name']}` | **{e['crop']}** | {e['current_train_count']} | {e['current_val_count']} | {e['current_test_count']} | "
            f"{e['test_precision']*100:.1f}% | {e['test_recall']*100:.1f}% | **{e['test_f1']*100:.1f}%** | {e['recommended_target_train_count']} | **+{e['additional_images_needed']}** |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 5. Crop-Specific Analysis & Targeted Directives",
        "",
        "### A. GINGER Diagnostic Requirements",
        "",
        "| Class Name | Train | Test | Precision | Recall | Test F1 | Priority | Actionable Directive |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ])

    for g in ginger_list:
        if "sheath" in g["class_name"]:
            directive = "**CRITICAL (23.5% F1):** Severe confusion with rice sheath blight. Collect +60 genuine ginger pseudostem/sheath lesion images."
        else:
            directive = "**HIGH (50.0% F1):** Moderate foliar spot identification. Collect +85 genuine ginger leaf spot images to reach 100."
        lines.append(
            f"| `{g['class_name']}` | {g['current_train_count']} | {g['current_test_count']} | {g['test_precision']*100:.1f}% | {g['test_recall']*100:.1f}% | **{g['test_f1']*100:.1f}%** | `{g['priority']}` | {directive} |"
        )

    lines.extend([
        "",
        "### B. BANANA Diagnostic Requirements",
        "",
        "| Class Name | Train | Test | Precision | Recall | Test F1 | Priority | Actionable Directive |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ])

    for b in banana_list:
        if "cordana" in b["class_name"]:
            directive = "**CRITICAL (28.6% F1):** Confused with Black Leaf Streak. Collect +80 oval zonate leaf spot images with bright yellow halos."
        elif "cigar" in b["class_name"]:
            directive = "**MEDIUM (66.7% F1):** Tip rot symptom. Collect +78 genuine banana fruit/tip rot images."
        elif "black" in b["class_name"]:
            directive = "**LOW (81.1% F1):** Black Sigatoka / Black Leaf Streak is well represented. No mandatory collection."
        elif "panama" in b["class_name"]:
            directive = "**LOW (87.5% F1):** Vascular wilt foliar yellowing is well distinguished. No mandatory collection."
        elif "anthracnose" in b["class_name"]:
            directive = "**LOW (93.3% F1):** Diamond-shaped necrotic lesions are well identified. No mandatory collection."
        elif "bunchy" in b["class_name"]:
            directive = "**LOW (95.2% F1):** Stunted rosette growth habit is well identified. No mandatory collection."
        else:
            directive = f"**{b['priority']}:** Collect +{b['additional_images_needed']} genuine images."
        lines.append(
            f"| `{b['class_name']}` | {b['current_train_count']} | {b['current_test_count']} | {b['test_precision']*100:.1f}% | {b['test_recall']*100:.1f}% | **{b['test_f1']*100:.1f}%** | `{b['priority']}` | {directive} |"
        )

    lines.extend([
        "",
        "### C. GARLIC Diagnostic Requirements",
        "",
        "| Class Name | Train | Test | Precision | Recall | Test F1 | Priority | Actionable Directive |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ])

    for gar in garlic_list:
        if "rust" in gar["class_name"]:
            directive = "**MEDIUM (66.7% F1):** Garlic rust pustules perform moderately. Collect +44 images to reach 100."
        else:
            directive = "**HIGH (50.0% F1):** Garlic leaf blight has moderate recall (58.3%). Collect +45 images to reach 100."
        lines.append(
            f"| `{gar['class_name']}` | {gar['current_train_count']} | {gar['current_test_count']} | {gar['test_precision']*100:.1f}% | {gar['test_recall']*100:.1f}% | **{gar['test_f1']*100:.1f}%** | `{gar['priority']}` | {directive} |"
        )

    lines.extend([
        "",
        "### D. ONION Future Taxonomy Expansion (DO NOT ADD TO CURRENT 117-CLASS DATASET)",
        "",
        "Onion is not part of the active 117-class Model 2 deployment. When ready to expand the model taxonomy, collect the following classes:",
        "",
        "| Proposed Class Name | Pathogen / Condition | Target Image Volume | Expansion Priority |",
        "| :--- | :--- | :--- | :--- |"
    ])

    for o in onion_future:
        lines.append(f"| `{o['class_name']}` | {o['disease']} | {o['target_images']} images | `{o['priority']}` |")

    lines.extend([
        "",
        "---",
        "",
        "## 6. Hard-Example Intra-Crop Confusion Collection Directives",
        "",
        "Rather than gathering random images, collection for these 5 high-confusion intra-crop pairs must prioritize **diagnostic discriminating features**:",
        ""
    ])

    for idx, p in enumerate(hard_pairs, 1):
        lines.extend([
            f"### {idx}. {p['pair']} ({p['crop']})",
            f"- **Observed Mutual Errors:** {p['mutual_errors']} test instances",
            f"- **Diagnostic Ambiguity:** {p['diagnostic_challenge']}",
            f"- **Targeted Collection Directive:** {p['collection_strategy']}",
            ""
        ])

    lines.extend([
        "---",
        "",
        "## 7. Artifact References",
        "",
        "- CSV Manifest: [`reports/model2_classifier/supplementary_collection_manifest.csv`](file:///reports/model2_classifier/supplementary_collection_manifest.csv)",
        "- Summary JSON: [`reports/model2_classifier/supplementary_collection_summary.json`](file:///reports/model2_classifier/supplementary_collection_summary.json)",
        "- Markdown Manifest Report: [`reports/model2_classifier/supplementary_collection_manifest.md`](file:///reports/model2_classifier/supplementary_collection_manifest.md)"
    ])

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    generate_manifest()
