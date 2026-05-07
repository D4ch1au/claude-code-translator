# Claude Code 翻译插件

[English](./README_en.md) | [加入讨论](https://github.com/D4ch1au/claude-code-translator/issues)

> Fork 说明：本仓库 fork 自 [iChenwin/claude-code-translator](https://github.com/iChenwin/claude-code-translator)。

**通过将提示词自动翻译为英文，节省 30%~50% 的 Token 消耗。**

这是一个非侵入式的 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 插件。它会在后台通过 TTime 云端翻译或 MiniMax Coding Plan 将你的中文/日文等输入自动翻译成英文。

## 主要特性

- **无感介入**：自动检测非英文输入并翻译，保留代码块、URL 和文件路径原样。
- **高兼容性**：支持 VS Code 集成模式、REPL 和文件读写操作。
- **多引擎支持**：内置 **TTime 云端翻译** 和 **MiniMax Coding Plan** 支持。
- **交互可控**：支持在发送前预览并修改翻译后的英文 Prompt，以及在接收回复后弹窗显示中文翻译结果（支持一键复制）。

## 快速开始

### Prerequisites

- Python 3.8+
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- TTime 登录回调 token OR
- MiniMax Coding Plan API key

1. **下载与安装依赖**
   ```bash
   git clone https://github.com/D4ch1au/claude-code-translator.git
   cd claude-code-translator
   pip install -r requirements.txt
   ```

2. **配置 provider**
   将 `config.example.json` 重命名为 `config.json` 并填入对应密钥。

   *使用 TTime 云端翻译:*
   ```json
   {
     "provider": "ttime",
     "ttime": {
       "base_url": "https://ink.timerecord.cn/apis",
       "source": "TTime",
       "token": "你的TTime登录回调token"
     }
   }
   ```
   TTime 内置源已提供独立 provider 别名。`ttime.token` 只需保留一份，切换时只改 `provider`，例如 `ttime_deepl` 或 `ttime_google`。

   *使用 MiniMax Coding Plan:*
   ```json
   {
     "provider": "minimax_coding_plan",
     "minimax_coding_plan": {
       "base_url": "https://api.minimax.io/anthropic",
       "model": "MiniMax-M2.7",
       "api_key": "你的MiniMax Coding Plan API-Key",
       "temperature": 0.3,
       "max_tokens": 4096,
       "timeout": 30
     }
   }
   ```

3. **安装 Hook**
   ```bash
   python install.py
   ```

重启 Claude Code 即可生效。

## 配置选项 (`config.json`)

| 选项Key | 说明 | 默认值 |
| :--- | :--- | :--- |
| `provider` | 翻译服务商。可填 `ttime`、`ttime_ai`、`ttime_google`、`ttime_deepl`、`ttime_bing`、`ttime_transmart`、`ttime_niutrans`、`minimax_coding_plan` | `ttime` |
| `ttime.source` | `provider` 为 `ttime` 时使用的 TTime 云端翻译源 | `TTime` |
| `ttime.token` | TTime 登录回调 token | 无 |
| `minimax_coding_plan.base_url` | MiniMax Coding Plan API 基础地址 | `https://api.minimax.io/anthropic` |
| `minimax_coding_plan.model` | MiniMax Coding Plan 模型名 | `MiniMax-M2.7` |
| `minimax_coding_plan.api_key` | MiniMax Coding Plan API key | 无 |
| `minimax_coding_plan.max_tokens` | 单次翻译最大输出 token | `4096` |
| `translate_output` | 是否将 Claude 的英文回复翻译回中文显示 | `true` |
| `interactive_input` | 发送前是否弹窗确认/修改英文 Prompt | `true` |
| `interactive_output` | 输出翻译后是否弹窗显示 | `true` |

### TTime 内置源 provider 别名

| `provider` | TTime `source` | 说明 |
| :--- | :--- | :--- |
| `ttime` | `TTime` | TTime 翻译 |
| `ttime_ai` | `TTimeAI` | TTimeAI 翻译 |
| `ttime_google` | `GoogleBuiltIn` | Google 翻译（内置） |
| `ttime_deepl` | `DeepLBuiltIn` | DeepL 翻译（内置 / DeepLX） |
| `ttime_bing` | `Bing` | Bing 翻译（内置） |
| `ttime_transmart` | `TranSmart` | 腾讯交互翻译（内置） |
| `ttime_niutrans` | `NiuTransBuiltIn` | 小牛翻译（内置） |

## 依据

- MiniMax Coding Plan 配置参考 MiniMax 官方文档：`https://platform.minimax.io/docs/token-plan/other-tools`。
- MiniMax Coding Plan 默认模型参考 `https://models.dev/api.json` 中的 `minimax-coding-plan` 记录。

## 卸载

```bash
python install.py --uninstall
```
