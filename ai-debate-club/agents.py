# agents.py
import ollama

class Agent:
    def __init__(self, name: str, persona: str):
        self.name = name
        self.persona = persona

    def speak(self, history: list[dict], context: str = "") -> str:
        """
        The agent generates a response.
        'history' is the recent conversation.
        'context' is relevant information retrieved from long-term memory.
        """
        print(f"--- {self.name} is thinking... ---")
        
        messages = [{'role': 'system', 'content': self.persona}]
        
        if context:
            messages.append({'role': 'system', 'content': context})

        messages.extend(history)

        response = ollama.chat(
            model='tinyllama',
            messages=messages
        )

        return response['message']['content'].strip()