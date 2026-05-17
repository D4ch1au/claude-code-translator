#!/usr/bin/env python3
"""UserPromptSubmit hook for translating Chinese input to English."""

import sys
import json
import os
import re

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.translation_client_factory import get_translation_client
from lib.dialogs import show_edit_dialog


SYSTEM_TAG_PATTERN = re.compile(r'<([a-zA-Z][\w-]*)\b[^>]*>[\s\S]*?</\1\s*>')


def strip_system_tags(text: str) -> str:
    """Recursively remove paired XML-like tag blocks injected by the harness."""
    for _ in range(10):
        new_text = SYSTEM_TAG_PATTERN.sub('', text)
        if new_text == text:
            return text
        text = new_text
    return text


def emit_continue():
    """Continue without adding hook output."""
    return


def emit_additional_context(context):
    """Emit Codex-compatible UserPromptSubmit context."""
    print(json.dumps({
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        },
    }, ensure_ascii=False))


def emit_system_message(message):
    """Emit a Codex-compatible non-blocking hook message."""
    print(json.dumps({
        "continue": True,
        "systemMessage": message,
    }, ensure_ascii=False))


def load_config():
    """Load configuration from config.json."""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'config.json'
    )
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """Main hook handler."""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        prompt = input_data.get('prompt') or input_data.get('user_prompt', '')

        if not prompt:
            # No prompt, continue without modification
            emit_continue()
            return

        # Strip harness-injected XML-like blocks so detection only sees user content
        user_content = strip_system_tags(prompt).strip()

        if not user_content:
            emit_continue()
            return

        # Load config
        config = load_config()

        # Initialize client based on provider
        client = get_translation_client(config)

        # Check if prompt contains non-English text
        if not client.detect_non_english(user_content):
            # No non-English text detected, continue without modification
            emit_continue()
            return

        # Translate to English
        translated, _ = client.translate(user_content, 'English')

        # Check if interactive mode is enabled
        interactive_input = config.get('interactive_input', True)

        if interactive_input:
            # Show edit dialog for user to review/edit translation
            confirmed, edited_translation = show_edit_dialog(user_content, translated)

            if not confirmed:
                # User cancelled, continue with original prompt without translation context
                emit_continue()
                return

            translated = edited_translation

        # Build context showing translation
        # Note: UserPromptSubmit hooks cannot modify the prompt, only add context
        # Claude will see: original Chinese prompt + this context with translation
        context = f"""[Translation Context]
The user's message above is in Chinese. Here is the English translation:

{translated}

Please respond based on the translated meaning."""

        emit_additional_context(context)

    except Exception as e:
        emit_system_message(f"Translation hook error: {e}")


if __name__ == '__main__':
    main()
