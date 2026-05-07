# Claude Code Translation Plugin

[简体中文](./README.md)

> Fork notice: This repository is forked from [iChenwin/claude-code-translator](https://github.com/iChenwin/claude-code-translator). The original author is [iChenwin](https://github.com/iChenwin). This fork preserves the original attribution and customizes translation providers on top of the original project.

**Save 30%~50% on token costs by automatically translating prompts to English.**

This plugin hooks into [Claude Code](https://docs.anthropic.com/en/docs/claude-code) to translate non-English input (Chinese, Japanese, etc.) into English through TTime Cloud or MiniMax Coding Plan before it reaches Claude.

## Features

- **Seamless**: Automatically detects and translates non-English input.
- **Smart**: Preserves code blocks, file paths, and URLs.
- **Flexible**: Supports **TTime Cloud** and **MiniMax Coding Plan** translation providers.
- **Native Experience**: Supports review/edit dialogs before sending translated prompts and popup display for translated output.

![Claude Code Translator Screenshot](./screenshot.png)

## Installation

### Prerequisites

- Python 3.8+
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- TTime login callback token OR
- MiniMax Coding Plan API key

1. **Clone & Install Dependencies**
   ```bash
   git clone https://github.com/D4ch1au/claude-code-translator.git
   cd claude-code-translator
   pip install -r requirements.txt
   ```

2. **Configure provider**
   Rename `config.example.json` to `config.json` and add the key for the provider you use.

   *Using TTime Cloud:*
   ```json
   {
     "provider": "ttime",
     "ttime": {
       "base_url": "https://ink.timerecord.cn/apis",
       "source": "TTime",
       "token": "your-ttime-callback-token"
     }
   }
   ```
   Built-in TTime sources have provider aliases. Keep `ttime.token` once, then switch by editing only `provider`, for example `ttime_deepl` or `ttime_google`.

   *Using MiniMax Coding Plan:*
   ```json
   {
     "provider": "minimax_coding_plan",
     "minimax_coding_plan": {
       "base_url": "https://api.minimax.io/anthropic",
       "model": "MiniMax-M2.7",
       "api_key": "your-minimax-coding-plan-api-key",
       "temperature": 0.3,
       "max_tokens": 4096,
       "timeout": 30
     }
   }
   ```

3. **Install Hooks**
   ```bash
   python install.py
   ```

Restart Claude Code, and you're good to go.

## Configuration (`config.json`)

| Option | Description | Default |
| :--- | :--- | :--- |
| `provider` | Translation provider. Supported values: `ttime`, `ttime_ai`, `ttime_google`, `ttime_deepl`, `ttime_bing`, `ttime_transmart`, `ttime_niutrans`, `minimax_coding_plan` | `ttime` |
| `ttime.source` | TTime cloud source used when `provider` is `ttime` | `TTime` |
| `ttime.token` | TTime login callback token | None |
| `minimax_coding_plan.base_url` | MiniMax Coding Plan API base URL | `https://api.minimax.io/anthropic` |
| `minimax_coding_plan.model` | MiniMax Coding Plan model name | `MiniMax-M2.7` |
| `minimax_coding_plan.api_key` | MiniMax Coding Plan API key | None |
| `minimax_coding_plan.max_tokens` | Maximum output tokens per translation | `4096` |
| `translate_output` | Show translated Chinese output for Claude responses | `true` |
| `interactive_input` | Show a review/edit dialog before sending the English prompt | `true` |
| `interactive_output` | Show translated output in a popup | `true` |

### Built-in TTime provider aliases

| `provider` | TTime `source` | Description |
| :--- | :--- | :--- |
| `ttime` | `TTime` | TTime translation |
| `ttime_ai` | `TTimeAI` | TTimeAI translation |
| `ttime_google` | `GoogleBuiltIn` | Google Translate built-in |
| `ttime_deepl` | `DeepLBuiltIn` | DeepL built-in / DeepLX |
| `ttime_bing` | `Bing` | Bing built-in |
| `ttime_transmart` | `TranSmart` | Tencent TranSmart built-in |
| `ttime_niutrans` | `NiuTransBuiltIn` | NiuTrans built-in |

## References

- MiniMax Coding Plan configuration is based on MiniMax official docs: `https://platform.minimax.io/docs/token-plan/other-tools`.
- The default MiniMax Coding Plan model is based on the `minimax-coding-plan` record in `https://models.dev/api.json`.

## Uninstallation

```bash
python install.py --uninstall
```
