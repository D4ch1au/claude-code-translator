"""TTime cloud translation client."""

import re
from typing import Optional, Tuple

import requests


class TTimeClient:
    """Client for TTime cloud translation."""

    DEFAULT_BASE_URL = "https://ink.timerecord.cn/apis"
    DEFAULT_SOURCE = "TTime"
    SUPPORTED_SOURCES = {
        "TTime",
        "TTimeAI",
        "TencentCloud",
        "Baidu",
        "Aliyun",
        "Google",
        "GoogleBuiltIn",
        "OpenAI",
        "AzureOpenAI",
        "YouDao",
        "DeepL",
        "DeepLBuiltIn",
        "Volcano",
        "Bing",
        "NiuTrans",
        "NiuTransBuiltIn",
        "CaiYun",
        "TranSmart",
        "Papago",
    }
    SOURCE_ALIASES = {source.lower(): source for source in SUPPORTED_SOURCES}
    LANGUAGE_ALIASES = {
        "english": "en",
        "en": "en",
        "chinese": "zh",
        "zh": "zh",
        "zh-cn": "zh",
        "中文": "zh",
        "中文(简体)": "zh",
    }

    def __init__(
        self,
        token: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        source: str = DEFAULT_SOURCE,
        language_type: str = "auto",
        timeout: int = 30,
        user_agent: Optional[str] = None,
        http_client=None,
    ):
        self.token = (token or "").strip()
        if not self.token:
            raise ValueError("TTime token is required. Set ttime.token in config.json.")

        self.source = self._normalize_source(source)
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.language_type = language_type or "auto"
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "time-translate/0.9.2 Chrome/104.0.5112.124 "
            "Electron/20.3.12 Safari/537.36"
        )
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
        url = f"{self.base_url}/translate/translate/"
        payload = {
            "channel": 0,
            "translateContent": text,
            "languageType": self.language_type,
            "languageResultType": self._language_code(target_lang),
            "type": self.source,
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
            "token": self.token,
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
            raise Exception(f"TTime Translation API error: {e}")
        except ValueError as e:
            raise Exception(f"Invalid TTime API response JSON: {e}")

        status = result.get("status")
        if status != 200:
            raise Exception(f"TTime API error: {status} - {result.get('msg')}")

        data = result.get("data")
        if not isinstance(data, dict):
            raise Exception("Invalid TTime API response: missing data object")

        translate_list = data.get("translateList")
        if not isinstance(translate_list, list):
            raise Exception("Invalid TTime API response: missing translateList")

        usage = {
            "provider": "ttime",
            "source": self.source,
        }
        return "\n".join(str(item) for item in translate_list), usage

    def _normalize_source(self, source: str) -> str:
        normalized = self.SOURCE_ALIASES.get((source or "").lower(), source)
        if normalized not in self.SUPPORTED_SOURCES:
            raise ValueError(
                "Unsupported TTime source: "
                f"{source}. Supported sources: {', '.join(sorted(self.SUPPORTED_SOURCES))}"
            )
        return normalized

    def _language_code(self, target_lang: str) -> str:
        key = (target_lang or "").strip().lower()
        return self.LANGUAGE_ALIASES.get(key, target_lang)
