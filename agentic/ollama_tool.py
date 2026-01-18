import requests
from typing import Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class OllamaTestInput(BaseModel):
    """Input schema for Ollama Model Tester tool"""

    model: str = Field(..., description="Model name (e.g., 'llama3.1:8b')")
    system_prompt: str = Field(..., description="System prompt to set model behavior")
    user_prompt: str = Field(..., description="User prompt to test the model with")
    temperature: Optional[float] = Field(
        0.7, description="Temperature for response generation (default: 0.7)"
    )


class OllamaTestTool(BaseTool):
    name: str = "Ollama Model Tester"
    description: str = (
        "Test AI models via Ollama API. "
        "Requires: model (e.g., 'llama3.1:8b'), system_prompt, and user_prompt. "
        "Optional: temperature (default: 0.7). "
        "Returns the model's response or an error message."
    )
    args_schema: type[BaseModel] = OllamaTestInput

    def _run(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = 0.7,
    ) -> str:
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
        OLLAMA_API_URL = "http://localhost:11434/api/chat"

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": temperature if temperature is not None else 0.7},
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
                response.raise_for_status()
                result = response.json()
                model_response = result.get("message", {}).get("content", "").strip()

                if model_response:
                    return f"Model '{model}' responded:\n\n{model_response}"
                else:
                    return f"Error: Model '{model}' returned empty response"

            except requests.Timeout:
                if attempt < max_retries - 1:
                    continue  # Retry
                return f"Error: Request to model '{model}' timed out after 120 seconds (retried {max_retries} times)"
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    continue  # Retry
                return f"Error calling Ollama API for model '{model}': {str(e)} (retried {max_retries} times)"
            except Exception as e:
                return f"Unexpected error testing model '{model}': {str(e)}"
        return f"Failed after {max_retries} retries for model '{model}'"
