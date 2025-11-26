import requests
from typing import Dict, Optional
from crewai.tools import BaseTool


class OllamaTestTool(BaseTool):
    name: str = "Ollama Model Tester"
    description: str = (
        "Test AI models via Ollama API. "
        "Input should be a JSON string with 'model' (e.g., 'llama3.1:8b'), "
        "'system_prompt', and 'user_prompt' keys. "
        "Returns the model's response or an error message."
    )
    
    def _run(self, model: str, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
        """
        Test a model via Ollama API.
        
        Args:
            model: Model name (e.g., 'llama3.1:8b')
            system_prompt: System prompt to set model behavior
            user_prompt: User prompt to test the model with
            temperature: Temperature for response generation (default: 0.7)
            
        Returns:
            The model's response or error message
        """
        OLLAMA_API_URL = "http://localhost:11434/api/generate"
        
        payload = {
            "model": model,
            "prompt": f"[SYSTEM] {system_prompt} [/SYSTEM]\n[USER] {user_prompt} [/USER]",
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        try:
            response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            model_response = result.get("response", "").strip()
            
            if model_response:
                return f"Model '{model}' responded:\n\n{model_response}"
            else:
                return f"Error: Model '{model}' returned empty response"
                
        except requests.Timeout:
            return f"Error: Request to model '{model}' timed out after 120 seconds"
        except requests.RequestException as e:
            return f"Error calling Ollama API for model '{model}': {str(e)}"
        except Exception as e:
            return f"Unexpected error testing model '{model}': {str(e)}"
