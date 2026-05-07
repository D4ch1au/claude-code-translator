"""MiniMax Coding Plan translation client."""

import re
from typing import Tuple

import requests


class MiniMaxCodingPlanClient:
    """Client for MiniMax Coding Plan translation."""

    DEFAULT_BASE_URL = "https://api.minimax.io/anthropic"
    DEFAULT_MODEL = "MiniMax-M2.7"
    DEFAULT_ANTHROPIC_VERSION = "2023-06-01"

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        api_key: str = "",
        model: str = DEFAULT_MODEL,
        timeout: int = 30,
        temperature: float = 0.3,
        max_tokens: int = 4096,
        anthropic_version: str = DEFAULT_ANTHROPIC_VERSION,
        http_client=None,
    ):
        self.api_key = (api_key or "").strip()
        if not self.api_key:
            raise ValueError("minimax_coding_plan.api_key is required in config.json.")

        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.model = (model or "").strip()
        if not self.model:
            raise ValueError("minimax_coding_plan.model is required in config.json.")

        self.timeout = timeout
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.anthropic_version = anthropic_version or self.DEFAULT_ANTHROPIC_VERSION
        self.http_client = http_client or requests

    def detect_chinese(self, text: str) -> bool:
        pattern = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\u20000-\u2a6df]")
        return bool(pattern.search(text))

    def detect_non_english(self, text: str) -> bool:
        clean_text = re.sub(r"```[\s\S]*?```", "", text)
        clean_text = re.sub(r"`[^`]+`", "", clean_text)
        clean_text = re.sub(r"https?://\S+", "", clean_text)
        clean_text = re.sub(r"[A-Za-z]:\\[\w\\/.]+", "", clean_text)
        clean_text = re.sub(r"/[\w/.-]+", "", clean_text)

        patterns = [
            r"[\u4e00-\u9fff]",
            r"[\u3400-\u4dbf]",
            r"[\u3040-\u309f]",
            r"[\u30a0-\u30ff]",
            r"[\uac00-\ud7af]",
            r"[\u0400-\u04ff]",
            r"[\u0600-\u06ff]",
            r"[\u0e00-\u0e7f]",
            r"[\u1e00-\u1eff]",
            r"[\u0370-\u03ff]",
            r"[\u0590-\u05ff]",
            r"[\u0900-\u097f]",
            r"[\u0980-\u09ff]",
            r"[\u0c00-\u0c7f]",
            r"[\u0b80-\u0bff]",
        ]
        return bool(re.search("|".join(patterns), clean_text))

    def translate(self, text: str, target_lang: str) -> Tuple[str, dict]:
        url = self._messages_url()
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "system": self._system_prompt(target_lang),
            "messages": [{"role": "user", "content": text}],
        }
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.anthropic_version,
            "Content-Type": "application/json",
        }

        try:
            response = self.http_client.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"MiniMax Coding Plan Translation API error: {e}")
        except ValueError as e:
            raise Exception(f"Invalid MiniMax Coding Plan API response JSON: {e}")

        usage = {
            "provider": "minimax_coding_plan",
            "model": self.model,
            "api_usage": result.get("usage", {}),
        }
        return self._extract_text(result), usage

    def _messages_url(self) -> str:
        if self.base_url.endswith("/messages"):
            return self.base_url
        if self.base_url.endswith("/v1"):
            return f"{self.base_url}/messages"
        return f"{self.base_url}/v1/messages"

    def _extract_text(self, result: dict) -> str:
        content = result.get("content")
        if not isinstance(content, list):
            raise Exception("Invalid MiniMax Coding Plan API response: missing content list")

        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))

        if not parts:
            raise Exception("Invalid MiniMax Coding Plan API response: missing text content")

        return "".join(parts).strip()

    def _system_prompt(self, target_lang: str) -> str:
        return f"""You are a professional translator, All your translations must be professional and colloquial. Translate the following text to {target_lang}.
Rules:
1. Only output the translated text, no explanations
2. Preserve code blocks, file paths, and technical terms as-is
3. Maintain the original formatting and structure
4. If the text is already in {target_lang}, return it unchanged"""
