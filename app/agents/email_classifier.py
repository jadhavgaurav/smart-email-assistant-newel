"""
📌 AGENT: Classification Agent
This agent is responsible for classifying the email into HR, IT, or Other,
and calculating the model confidence based on prediction probabilities.
"""

import joblib
import os
import numpy as np

class EmailClassifier:
    def __init__(self, model_path=None, vectorizer_path=None):
        # Allow env override or default path
        model_path = model_path or os.path.join("models", "model.pkl")
        vectorizer_path = vectorizer_path or os.path.join("models", "vectorizer.pkl")

        # Load model and vectorizer
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.confidence_threshold = 0.6

    def predict(self, email_text: str) -> dict:
        if not email_text or not isinstance(email_text, str):
            return {
                "error": "Invalid input. Must be a non-empty string."
            }

        # Vectorize input
        X = self.vectorizer.transform([email_text])
        
        # Predict probabilities
        probas = self.model.predict_proba(X)[0]
        pred_index = np.argmax(probas)
        predicted_class = self.model.classes_[pred_index]
        confidence = float(probas[pred_index])  # ensure JSON serializable

        return {
            "email_text": email_text,
            "predicted_category": predicted_class,
            "confidence": round(confidence, 4)
        }

    def is_confident(self, confidence: float, predicted_category: str) -> bool:
        """Whether the result meets the confidence threshold."""
        return confidence >= self.confidence_threshold and predicted_category != "Other"

