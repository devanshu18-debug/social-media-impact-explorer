"""Reusable feature preparation and prediction helpers for the social-media model."""
from __future__ import annotations

import numpy as np
import pandas as pd

COMPARISON_ORDER = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Frequently": 3, "Always": 4}

NUMERIC_FEATURES = [
    "Age", "Daily_Usage_Hours", "Weekend_Extra_Hours", "Sleep_Duration_Hours",
    "Sleep_Quality_Score", "Late_Night_Usage", "Social_Comparison_Score",
    "Weekly_Avg_Usage", "Sleep_Deficit", "Usage_to_Sleep_Ratio",
]
CATEGORICAL_FEATURES = ["Gender", "Academic_Level", "Primary_Platform", "Device_Type"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
RAW_INPUT_COLUMNS = [
    "Age", "Gender", "Academic_Level", "Primary_Platform", "Daily_Usage_Hours",
    "Weekend_Extra_Hours", "Device_Type", "Sleep_Duration_Hours",
    "Sleep_Quality_Score", "Late_Night_Usage", "Social_Comparison_Frequency",
]

def engineer_features(raw: pd.DataFrame) -> pd.DataFrame:
    """Apply row-level feature transformations to raw student records."""
    out = raw.drop(columns=["Student_ID"], errors="ignore").copy()
    out["Late_Night_Usage"] = out["Late_Night_Usage"].astype(int)
    out["Social_Comparison_Score"] = out["Social_Comparison_Frequency"].map(COMPARISON_ORDER)
    out["Weekly_Avg_Usage"] = (5 * out["Daily_Usage_Hours"] +
                               2 * (out["Daily_Usage_Hours"] + out["Weekend_Extra_Hours"])) / 7
    out["Sleep_Deficit"] = (8 - out["Sleep_Duration_Hours"]).clip(lower=0)
    # Zero sleep is invalid for the ratio; leave it missing for pipeline imputation.
    out["Usage_to_Sleep_Ratio"] = (out["Daily_Usage_Hours"] /
                                   out["Sleep_Duration_Hours"].replace(0, np.nan))
    return out.drop(columns=["Social_Comparison_Frequency"], errors="ignore")

def predict_new_student(model_bundle: dict, raw_student) -> dict:
    """Predict both targets from a dict or DataFrame of raw input columns."""
    raw = raw_student if isinstance(raw_student, pd.DataFrame) else pd.DataFrame([raw_student])
    missing = sorted(set(RAW_INPUT_COLUMNS) - set(raw.columns))
    if missing:
        raise ValueError(f"Missing required input columns: {missing}")
    reg = model_bundle["mental_health_regressor"]
    clf = model_bundle["overall_impact_classifier"]
    result = {
        "mental_health_index": float(reg.predict(raw)[0]),
        "overall_impact": str(clf.predict(raw)[0]),
    }
    if hasattr(clf, "predict_proba"):
        result["overall_impact_probabilities"] = {
            str(label): float(prob)
            for label, prob in zip(clf.classes_, clf.predict_proba(raw)[0])
        }
    return result
