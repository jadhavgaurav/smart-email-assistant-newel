"""
📌 AGENT: Escalation Agent
This agent logs and handles emails where the classifier has low confidence,
allowing for manual follow-up.
"""

import datetime
import os

class EscalationAgent:
    def __init__(self, log_path="logs/escalations.log"):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.log_path = log_path

    def escalate(self, email_text: str, category: str, confidence: float) -> dict:
        timestamp = datetime.datetime.now().isoformat()
        message = f"[{timestamp}] ESCALATED\nCategory: {category}\nConfidence: {confidence}\nEmail: {email_text}\n\n"

        with open(self.log_path, "a") as f:
            f.write(message)

        return {
            "email_text": email_text,
            "category": category,
            "confidence": confidence,
            "status": "Escalated",
            "message": "Email has been escalated for manual review."
        }
