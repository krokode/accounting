"""
Custom / Local OpenAI-Compatible provider implementation.
Ideal for privacy-first, on-premise local deployments (Ollama, vLLM, LM Studio, LocalAI)
or aggregators like OpenRouter.
"""
import json
import logging
import time
from typing import Tuple
import httpx

from apps.ai_assistant.providers.base import BaseLLMProvider
from apps.ai_assistant.providers.exceptions import (
    AIConfigurationError,
    AIRateLimitError,
    AIOfflineError,
    AIAuthenticationError,
    AIError,
)

logger = logging.getLogger(__name__)


class CustomProvider(BaseLLMProvider):
    name = "custom"
    display_name = "Custom / Local (Ollama, vLLM, OpenRouter)"
    default_model = "llama3.3"
    default_base_url = "http://localhost:11434/v1"
    is_vision_supported = False

    def validate_configuration(self):
        # Local endpoints like Ollama do not require an API key
        if not self.base_url:
            raise AIConfigurationError(provider=self.display_name, details="Base URL must be configured.")

    def _get_headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _handle_response_error(self, response: httpx.Response):
        status = response.status_code
        try:
            err_data = response.json().get('error', {})
            err_msg = err_data.get('message', response.text)
        except Exception:
            err_msg = response.text

        if status == 429:
            raise AIRateLimitError(provider=self.display_name, details=err_msg)
        elif status in (401, 403):
            raise AIAuthenticationError(provider=self.display_name, details=err_msg)
        else:
            raise AIError(f"Custom endpoint error ({status}): {err_msg}", provider=self.display_name, details=err_msg)

    def _post_chat(self, payload: dict, timeout: float = 60.0) -> dict:
        self.validate_configuration()
        headers = self._get_headers()
        base = self.base_url.rstrip('/')
        endpoint = f"{base}/chat/completions"
        try:
            with httpx.Client(timeout=timeout) as client:
                res = client.post(endpoint, headers=headers, json=payload)
                if res.status_code != 200:
                    self._handle_response_error(res)
                return res.json()
        except httpx.ConnectError as ce:
            raise AIOfflineError(provider=self.display_name, endpoint=endpoint, details=str(ce))
        except httpx.TimeoutException as te:
            raise AIOfflineError(provider=self.display_name, endpoint=endpoint, details=f"Timeout: {te}")
        except AIError:
            raise
        except Exception as e:
            raise AIError(f"Custom endpoint request failed: {e}", provider=self.display_name, details=str(e))

    def generate_text(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2
        }
        data = self._post_chat(payload)
        choices = data.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")
        return ""

    def extract_document(self, file_path: str, mime_type: str, system_prompt: str) -> dict:
        doc_text = self.extract_text_from_file(file_path)
        if not doc_text:
            raise AIError("No readable text content found in document for local model.", provider=self.display_name)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Document content:\n\n{doc_text}\n\nExtract and return structured JSON records."}
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1
        }

        data = self._post_chat(payload)
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        clean_text = self.clean_json_text(content)
        return json.loads(clean_text)

    def test_connection(self) -> Tuple[bool, str]:
        start = time.time()
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": "Ping"}],
            "max_tokens": 5
        }
        try:
            data = self._post_chat(payload, timeout=10.0)
            elapsed_ms = int((time.time() - start) * 1000)
            if data.get("choices"):
                return True, f"Connected successfully to {self.base_url}! (Latency: {elapsed_ms}ms)"
            return False, f"Connected, but model '{self.model}' returned unexpected structure."
        except AIError as aie:
            return False, str(aie)
        except Exception as e:
            return False, str(e)
