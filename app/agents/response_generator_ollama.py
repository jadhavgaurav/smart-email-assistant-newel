# app/agents/response_generator_ollama.py

import requests

class ResponseGenerator:
    def __init__(self, model: str = "llama3:8b-instruct-q4_K_M", host: str = "http://localhost:11434"):
        self.model = model
        self.url = f"{host}/api/generate"

    def get_prompt(self, email_text: str, category: str) -> str:
        system_prompt = {
            "HR": "You are an HR assistant. Respond professionally to the following email:",
            "IT": "You are an IT support agent. Helpfully respond to the following message:",
            "Other": "You are a corporate assistant. Politely respond to the message:"
        }
        base = system_prompt.get(category, system_prompt["Other"])
        return f"{base}\n\n\"{email_text}\"\n\nReply:"

    def generate_response(self, email_text: str, category: str = "Other") -> dict:
        prompt = self.get_prompt(email_text, category)

        try:
            print(f"📥 Sending prompt to Ollama ({self.model})...")
            response = requests.post(self.url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })
            response.raise_for_status()

            result = response.json()
            response_text = result.get("response", "").strip() or "[Empty response from LLM]"

            return {
                "email_text": email_text,
                "category": category,
                "response": response_text
            }

        except Exception as e:
            return {
                "email_text": email_text,
                "category": category,
                "response": "[LLM failed]",
                "error": str(e)
            }
