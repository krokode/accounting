"""
Abstract base class for all AI/LLM providers.
"""
import base64
import json
import logging
import os
import re
from abc import ABC, abstractmethod
from typing import Optional, Tuple
from pypdf import PdfReader

from apps.ai_assistant.providers.exceptions import (
    AIConfigurationError,
    AIRateLimitError,
    AIOfflineError,
    AIAuthenticationError,
    AIError,
)

logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    name: str = "base"
    display_name: str = "Base Provider"
    default_model: str = ""
    default_base_url: str = ""
    is_vision_supported: bool = False

    def __init__(self, api_key: str = "", model: str = "", base_url: str = ""):
        self.api_key = api_key.strip()
        self.model = model.strip() or self.default_model
        self.base_url = (base_url.strip() or self.default_base_url).rstrip('/')

    def validate_configuration(self):
        """Validates that required credentials exist, raising AIConfigurationError if missing."""
        if not self.api_key and self.name != "custom":
            raise AIConfigurationError(provider=self.display_name)

    @abstractmethod
    def generate_text(self, prompt: str, system_prompt: str = "") -> str:
        """Generates conversational text response given prompt and system instructions."""
        pass

    @abstractmethod
    def extract_document(self, file_path: str, mime_type: str, system_prompt: str) -> dict:
        """Extracts structured operational and financial JSON from document file."""
        pass

    @abstractmethod
    def test_connection(self) -> Tuple[bool, str]:
        """
        Sends a lightweight test ping to verify credentials and endpoint availability.
        Returns: (success: bool, status_message_or_latency: str)
        """
        pass

    @staticmethod
    def clean_json_text(text: str) -> str:
        """Strips markdown code fences and returns cleaned JSON substring."""
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = cleaned.strip()

        # Extract first JSON object or array if surrounded by chatter
        match = re.search(r'(\{[\s\S]*\}|\[[\s\S]*\])', cleaned)
        if match:
            return match.group(0).strip()
        return cleaned

    @staticmethod
    def extract_text_from_file(file_path: str) -> str:
        """Extracts textual content from PDF or text file."""
        if file_path.lower().endswith('.pdf'):
            try:
                reader = PdfReader(file_path)
                text_pages = []
                for idx, page in enumerate(reader.pages):
                    t = page.extract_text() or ""
                    if t.strip():
                        text_pages.append(f"--- Page {idx+1} ---\n{t.strip()}")
                return "\n\n".join(text_pages)
            except Exception as e:
                logger.warning(f"Failed to extract text from PDF: {e}")
                return ""
        elif file_path.lower().endswith(('.txt', '.csv', '.json', '.xml', '.html')):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            except Exception as e:
                logger.warning(f"Failed to read text file: {e}")
                return ""
        return ""

    @staticmethod
    def get_file_base64(file_path: str) -> str:
        """Reads file and returns base64-encoded string."""
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
