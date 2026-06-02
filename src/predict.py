"""
predict.py — Wrapper for the Orange3 Machine Learning models.

Exposes functions to predict the field of study, satisfaction, and
engineering specialty based on user responses.
"""

import os
import pickle
from pathlib import Path

# Try importing Orange; handle case if it's not installed yet during dev
try:
    import Orange
    _ORANGE_AVAILABLE = True
except ImportError:
    _ORANGE_AVAILABLE = False

_MODELS_DIR = Path(__file__).resolve().parent / "models"

# Memoize loaded models to avoid loading them repeatedly
_rf_q1_model = None
_lr_q1_model = None
_rf_q2_model = None

def _load_q1_models():
    global _rf_q1_model, _lr_q1_model
    if _rf_q1_model is None:
        path = _MODELS_DIR / "questionaire_1" / "random_forest.pkcls"
        with open(path, "rb") as f:
            _rf_q1_model = pickle.load(f)
    if _lr_q1_model is None:
        path = _MODELS_DIR / "questionaire_1" / "linear_regression.pkcls"
        with open(path, "rb") as f:
            _lr_q1_model = pickle.load(f)

def _load_q2_model():
    global _rf_q2_model
    if _rf_q2_model is None:
        path = _MODELS_DIR / "questionaire_2" / "rand_forest_questionnaire2.pkcls"
        with open(path, "rb") as f:
            _rf_q2_model = pickle.load(f)

def predict_q1(vector_26: list) -> tuple[str, float]:
    """
    Predict the field of study and satisfaction.
    
    Args:
        vector_26: The 26-element model vector from Q1 payload (gender + 25 questions).
        
    Returns:
        A tuple of (predicted_field, predicted_satisfaction).
    """
    if not _ORANGE_AVAILABLE:
        return "technology", 80.0  # Fallback for dev without Orange

    _load_q1_models()

    # 1. Predict Field (RF)
    data_rf = Orange.data.Table.from_list(_rf_q1_model.domain, [vector_26])
    rf_idx = _rf_q1_model(data_rf)[0]
    predicted_field = str(_rf_q1_model.domain.class_var.values[int(rf_idx)])
    
    # FORCE PREDICTION FOR TESTING
    #predicted_field = "technology"
    
    # 2. Build Vector for LR (One-Hot Encoding)
    base_features = vector_26
    field_values = []
    for attr in _lr_q1_model.domain.attributes[26:]: 
        if "=" in attr.name:
            val_name = attr.name.split("=")[1]
            field_values.append(1.0 if predicted_field == val_name else 0.0)
        else:
            field_values.append(0.0)
    
    vector_32 = base_features + field_values
    
    # 3. Predict Satisfaction (LR)
    data_lr = Orange.data.Table.from_list(_lr_q1_model.domain, [vector_32])
    predicted_satis = round(float(_lr_q1_model(data_lr)[0]), 2)
    
    return predicted_field, predicted_satis

def predict_q2(vector_25: list) -> str:
    """
    Predict the engineering specialty based on Q2 responses.
    
    Args:
        vector_25: The 25-element vector of Q2 answers.
        
    Returns:
        The predicted engineering specialty (string).
    """
    if not _ORANGE_AVAILABLE:
        return "Software Engineering"  # Fallback for dev without Orange

    _load_q2_model()

    data_table = Orange.data.Table.from_list(_rf_q2_model.domain, [vector_25])
    prediction_idx = _rf_q2_model(data_table)[0]
    career_name = str(_rf_q2_model.domain.class_var.values[int(prediction_idx)])
    
    return career_name
