"""Translation client factory."""

from lib.minimax_coding_plan_client import MiniMaxCodingPlanClient
from lib.ttime_client import TTimeClient


TTIME_PROVIDER_SOURCES = {
    "ttime": "TTime",
    "ttime_cloud": "TTime",
    "ttime_ai": "TTimeAI",
    "ttime_google": "GoogleBuiltIn",
    "ttime_deepl": "DeepLBuiltIn",
    "ttime_bing": "Bing",
    "ttime_transmart": "TranSmart",
    "ttime_niutrans": "NiuTransBuiltIn",
}


def get_translation_client(config):
    provider = config.get("provider", "ttime")

    if provider in TTIME_PROVIDER_SOURCES:
        ttime_config = config.get("ttime", {})
        provider_config = config.get(provider, {})
        source = provider_config.get("source", ttime_config.get("source", TTIME_PROVIDER_SOURCES[provider]))
        return TTimeClient(
            token=provider_config.get("token", ttime_config.get("token")),
            base_url=provider_config.get(
                "base_url",
                ttime_config.get("base_url", TTimeClient.DEFAULT_BASE_URL),
            ),
            source=source,
            language_type=provider_config.get(
                "language_type",
                ttime_config.get("language_type", "auto"),
            ),
            timeout=provider_config.get("timeout", ttime_config.get("timeout", 30)),
            user_agent=provider_config.get("user_agent", ttime_config.get("user_agent")),
        )

    if provider == "minimax_coding_plan":
        minimax_config = config.get("minimax_coding_plan", {})
        return MiniMaxCodingPlanClient(
            base_url=minimax_config.get("base_url", MiniMaxCodingPlanClient.DEFAULT_BASE_URL),
            api_key=minimax_config.get("api_key", ""),
            model=minimax_config.get("model", MiniMaxCodingPlanClient.DEFAULT_MODEL),
            timeout=minimax_config.get("timeout", 30),
            temperature=minimax_config.get("temperature", 0.3),
            max_tokens=minimax_config.get("max_tokens", 4096),
            anthropic_version=minimax_config.get(
                "anthropic_version",
                MiniMaxCodingPlanClient.DEFAULT_ANTHROPIC_VERSION,
            ),
        )

    raise ValueError(f"Unsupported translation provider: {provider}")
