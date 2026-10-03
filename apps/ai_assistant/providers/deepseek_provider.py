"""
DeepSeek provider implementation using OpenAI-compatible API format over httpx.
Supports deepseek-chat (DeepSeek-V3) and deepseek-reasoner (DeepSeek-R1).
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


class DeepSeekProvider(BaseLLMProvider):
    name = "deepseek"
    display_name = "DeepSeek"
    default_model = "deepseek-chat"
    default_base_url = "https://api.deepseek.com"
    is_vision_supported = False

    def _get_headers(self) -> dict:
        self.validate_configuration()
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

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
            raise AIError(f"DeepSeek error ({status}): {err_msg}", provider=self.display_name, details=err_msg)

    def _post_chat(self, payload: dict, timeout: float = 60.0) -> dict:
        headers = self._get_headers()
        base = self.base_url.rstrip('/')
        endpoint = f"{base}/chat/completions" if not base.endswith('/v1') else f"{base}/chat/completions"
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
            raise AIError(f"DeepSeek request failed: {e}", provider=self.display_name, details=str(e))

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
            if mime_type.startswith("image/"):
                raise AIError(
                    "DeepSeek is a text-based model and cannot process raw image scans directly. "
                    "Please use a multimodal vision provider (Google Gemini, OpenAI GPT-4o, or Claude 3.7) for image documents.",
                    provider=self.display_name
                )
            raise AIError("No readable text content found in document.", provider=self.display_name)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Document content:\n\n{doc_text}\n\nExtract and return the structured JSON record."}
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }

        data = self._post_chat(payload)
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        clean_text = self.clean_json_text(content)
        return json.loads(clean_text)

    def test_connection(self) -> Tuple[bool, str]:
        if not self.api_key:
            return False, "API key is not configured."
        start = time.time()
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": "Ping"}],
            "max_tokens": 5
        }
        try:
            data = self._post_chat(payload, timeout=15.0)
            elapsed_ms = int((time.time() - start) * 1000)
            if data.get("choices"):
                return True, f"Connected successfully! (Latency: {elapsed_ms}ms)"
            return False, "Unexpected response from DeepSeek."
        except AIError as aie:
            return False, str(aie)
        except Exception as e:
            return False, str(e)
