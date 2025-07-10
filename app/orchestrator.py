from agents.email_classifier import EmailClassifier
from agents.crewai_response_agent import OllamaResponderAgent
from agents.escalation_agent import EscalationAgent

class Orchestrator:
    def __init__(self):
        self.classifier = EmailClassifier()
        self.responder = OllamaResponderAgent()
        self.escalator = EscalationAgent()

    def handle_email(self, email_text: str) -> dict:
        result = self.classifier.predict(email_text)
        is_confident = self.classifier.is_confident(result["confidence"], result["predicted_category"])

        if is_confident:
            response = self.responder.generate_response(email_text, result["predicted_category"])
            return {
                **result,
                "action": "Responded",
                "response": response["response"]
            }
        else:
            escalation = self.escalator.escalate(email_text, result["predicted_category"], result["confidence"])
            return {
                **result,
                "action": "Escalated",
                "escalation_message": escalation["message"]
            }
