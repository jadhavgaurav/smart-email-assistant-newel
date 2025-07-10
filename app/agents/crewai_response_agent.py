"""
📌 AGENT: Response Agent (LLM - Ollama)
This agent uses a local LLM via LangChain and Ollama to generate dynamic,
contextual email responses based on category.
"""

from langchain_ollama import OllamaLLM

class OllamaResponderAgent:
    def __init__(self, model_name="llama3:8b-instruct-q4_K_M", base_url="http://host.docker.internal:11434"):
        # Setup LangChain LLM wrapper for Ollama
        self.llm = OllamaLLM(
            model=model_name,
            base_url=base_url,
            temperature=0.7,
            max_tokens=200
        )

    def _generate_prompt(self, email_text, category):
        prompts = {
            "HR": "You are an HR assistant. Reply professionally to this email:",
            "IT": "You are an IT assistant. Helpfully respond to this issue:",
            "Other": "You are a helpful assistant. Respond courteously to this email:"
        }
        return f"{prompts.get(category, prompts['Other'])}\n\n\"{email_text}\"\n\nReply:"

    def generate_response(self, email_text: str, category: str = "Other") -> dict:
        try:
            prompt = self._generate_prompt(email_text, category)
            print("\n📥 Sending to Ollama:")
            print(prompt)

            # Call LLM directly (NOT via CrewAI)
            result = self.llm.invoke(prompt)

            return {
                "email_text": email_text,
                "category": category,
                "response": result.strip() or "[LLM returned empty response]"
            }
        except Exception as e:
            return {
                "email_text": email_text,
                "category": category,
                "response": "[LLM call failed]",
                "error": str(e)
            }
