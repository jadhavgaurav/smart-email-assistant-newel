"""
📌 AGENT: Response Agent (Template-Based)
This agent generates a professional response based on the classified category
using static templates. Used in EC2-safe and non-LLM environments.
"""

# app/agents/response_generator.py

class ResponseGenerator:
    def __init__(self):
        pass  # No model to load

    def generate_response(self, email_text: str, category: str = "Other") -> dict:
        templates = {
            "HR": f"Hi, thank you for your message. Our HR team has received your request:\n\n\"{email_text}\"\n\nWe’ll get back to you shortly.",
            "IT": f"Hello, your IT support request has been received:\n\n\"{email_text}\"\n\nOur team will review and assist you soon.",
            "Other": f"Thanks for reaching out. We’ve received your message:\n\n\"{email_text}\"\n\nWe’ll forward it to the relevant department."
        }

        response = templates.get(category, templates["Other"])
        return {
            "email_text": email_text,
            "category": category,
            "response": response
        }
