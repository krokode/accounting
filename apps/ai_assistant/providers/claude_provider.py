"""
Anthropic Claude provider implementation using lightweight httpx client.
Supports native PDF documents and image vision.
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


class ClaudeProvider(BaseLLMProvider):
    name = "claude"
    display_name = "Anthropic Claude"
    default_model = "claude-3-7-sonnet-20250219"
    default_base_url = "https://api.anthropic.com"
    is_vision_supported = True

    def _get_headers(self) -> dict:
        self.validate_configuration()
        return {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
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
            raise AIError(f"Claude error ({status}): {err_msg}", provider=self.display_name, details=err_msg)

    def _post_messages(self, payload: dict, timeout: float = 60.0) -> dict:
        headers = self._get_headers()
        url = f"{self.base_url}/v1/messages"
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
            raise AIError(f"Claude request failed: {e}", provider=self.display_name, details=str(e))

    def generate_text(self, prompt: str, system_prompt: str = "") -> str:
        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
        if system_prompt:
            payload["system"] = system_prompt

        data = self._post_messages(payload)
        content_blocks = data.get("content", [])
        text_parts = [b.get("text", "") for b in content_blocks if b.get("type") == "text"]
        return "".join(text_parts)

    def extract_document(self, file_path: str, mime_type: str, system_prompt: str) -> dict:
        content_blocks = []
        b64_data = self.get_file_base64(file_path)

        if mime_type == "application/pdf":
            content_blocks.append({
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": b64_data
                }
            })
        elif mime_type.startswith("image/"):
            content_blocks.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": mime_type,
                    "data": b64_data
                }
            })
        else:
            text = self.extract_text_from_file(file_path)
            content_blocks.append({"type": "text", "text": f"Document content:\n\n{text}"})

        content_blocks.append({
            "type": "text",
            "text": "Analyze the document and output the extracted records strictly as a JSON object matching the required schema."
        })

        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "system": system_prompt + "\nIMPORTANT: Return ONLY raw JSON without markdown formatting or preamble.",
            "messages": [{"role": "user", "content": content_blocks}],
            "temperature": 0.1
        }

        data = self._post_messages(payload)
        text_parts = [b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"]
        raw_output = "".join(text_parts)
        clean_text = self.clean_json_text(raw_output)
        return json.loads(clean_text)

    def test_connection(self) -> Tuple[bool, str]:
        if not self.api_key:
            return False, "API key is not configured."
        start = time.time()
        payload = {
            "model": self.model,
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "Ping"}]
        }
        try:
            data = self._post_messages(payload, timeout=15.0)
            elapsed_ms = int((time.time() - start) * 1000)
            if data.get("content"):
                return True, f"Connected successfully! (Latency: {elapsed_ms}ms)"
            return False, "Unexpected response from Anthropic Claude."
        except AIError as aie:
            return False, str(aie)
        except Exception as e:
            return False, str(e)
