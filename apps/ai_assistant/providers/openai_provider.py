"""
OpenAI / ChatGPT provider implementation using lightweight httpx HTTP client.
Supports Vision (GPT-4o / GPT-4o-mini) and structured JSON outputs.
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


class OpenAIProvider(BaseLLMProvider):
    name = "openai"
    display_name = "OpenAI / ChatGPT"
    default_model = "gpt-4o"
    default_base_url = "https://api.openai.com/v1"
    is_vision_supported = True

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
            raise AIError(f"OpenAI error ({status}): {err_msg}", provider=self.display_name, details=err_msg)

    def _post_chat(self, payload: dict, timeout: float = 60.0) -> dict:
        headers = self._get_headers()
        url = f"{self.base_url}/chat/completions"
        try:
            with httpx.Client(timeout=timeout) as client:
                res = client.post(url, headers=headers, json=payload)
                if res.status_code != 200:
                    self._handle_response_error(res)
                return res.json()
        except httpx.ConnectError as ce:
            raise AIOfflineError(provider=self.display_name, endpoint=url, details=str(ce))
        except httpx.TimeoutException as te:
            raise AIOfflineError(provider=self.display_name, endpoint=url, details=f"Timeout: {te}")
        except AIError:
            raise
        except Exception as e:
            raise AIError(f"OpenAI request failed: {e}", provider=self.display_name, details=str(e))

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
        is_image = mime_type.startswith("image/")
        user_content = []

        if is_image:
            b64_img = self.get_file_base64(file_path)
            user_content = [
                {"type": "text", "text": "Analyze this document scan and extract the structured records according to instructions."},
                {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64_img}"}}
            ]
        else:
            # For PDF or other files, extract text
            doc_text = self.extract_text_from_file(file_path)
            if not doc_text:
                raise AIError("Document has no readable text content and image vision is not supported for this format.", provider=self.display_name)
            user_content = f"Document content:\n\n{doc_text}\n\nExtract the structured records according to instructions."

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
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
            return False, "Unexpected response structure from OpenAI."
        except AIError as aie:
            return False, str(aie)
        except Exception as e:
            return False, str(e)
