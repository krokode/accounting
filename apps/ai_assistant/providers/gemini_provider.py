"""
Google Gemini provider using official google-genai SDK.
Supports native multimodal PDF & image extraction.
"""
import json
import logging
import time
from typing import Tuple

from apps.ai_assistant.providers.base import BaseLLMProvider
from apps.ai_assistant.providers.exceptions import (
    AIConfigurationError,
    AIRateLimitError,
    AIOfflineError,
    AIAuthenticationError,
    AIError,
)

logger = logging.getLogger(__name__)


class GeminiProvider(BaseLLMProvider):
    name = "gemini"
    display_name = "Google Gemini"
    default_model = "gemini-2.5-flash"
    default_base_url = "https://generativelanguage.googleapis.com"
    is_vision_supported = True

    def _get_client(self):
        self.validate_configuration()
        try:
            from google import genai
            return genai.Client(api_key=self.api_key)
        except Exception as e:
            raise AIConfigurationError(provider=self.display_name, details=str(e))

    def _handle_exception(self, e: Exception):
        msg = str(e).lower()
        if "quota" in msg or "429" in msg or "resource_exhausted" in msg:
            raise AIRateLimitError(provider=self.display_name, details=str(e))
        elif "api_key_invalid" in msg or "permission" in msg or "401" in msg or "403" in msg or "unauthenticated" in msg:
            raise AIAuthenticationError(provider=self.display_name, details=str(e))
        elif "connection" in msg or "timeout" in msg or "offline" in msg or "dns" in msg or "network" in msg:
            raise AIOfflineError(provider=self.display_name, endpoint=self.default_base_url, details=str(e))
        else:
            raise AIError(message=f"Gemini error: {e}", provider=self.display_name, details=str(e))

    def generate_text(self, prompt: str, system_prompt: str = "") -> str:
        self.validate_configuration()
        client = self._get_client()
        contents = [system_prompt, prompt] if system_prompt else [prompt]
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=contents
            )
            return response.text or ""
        except Exception as e:
            self._handle_exception(e)

    def extract_document(self, file_path: str, mime_type: str, system_prompt: str) -> dict:
        self.validate_configuration()
        client = self._get_client()
        from google.genai import types

        with open(file_path, 'rb') as f:
            file_bytes = f.read()

        part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=[part, system_prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                )
            )
            clean_text = self.clean_json_text(response.text or "")
            return json.loads(clean_text)
        except json.JSONDecodeError as je:
            raise AIError(f"Failed to parse JSON response from Gemini: {je}", provider=self.display_name)
        except Exception as e:
            self._handle_exception(e)

    def test_connection(self) -> Tuple[bool, str]:
        if not self.api_key:
            return False, "API key is not configured."
        start = time.time()
        try:
            client = self._get_client()
            response = client.models.generate_content(
                model=self.model,
                contents="Ping. Respond with 'PONG'."
            )
            elapsed_ms = int((time.time() - start) * 1000)
            if response and response.text:
                return True, f"Connected successfully! (Latency: {elapsed_ms}ms)"
            return False, "Received empty response from Gemini."
        except Exception as e:
            try:
                self._handle_exception(e)
            except AIError as aie:
                return False, str(aie)
            return False, str(e)
