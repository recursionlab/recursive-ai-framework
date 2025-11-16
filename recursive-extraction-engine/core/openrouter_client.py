"""
OpenRouter API client wrapper to match Anthropic SDK interface
"""

import requests
import json
from typing import Optional


class OpenRouterMessage:
    """Wrapper for OpenRouter message response"""
    def __init__(self, content_text: str):
        self.content = [type('Content', (), {'text': content_text})]


class OpenRouterClient:
    """
    OpenRouter API client that mimics Anthropic SDK interface.
    This allows drop-in replacement in extraction engine.
    """

    def __init__(self, api_key: str, model: str = "anthropic/claude-3.5-sonnet"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    class Messages:
        """Nested Messages class to match anthropic.messages.create()"""

        def __init__(self, client):
            self.client = client

        def create(
            self,
            model: str,
            max_tokens: int,
            messages: list,
            **kwargs
        ):
            """
            Create completion via OpenRouter API.
            Matches Anthropic SDK interface.
            """
            headers = {
                "Authorization": f"Bearer {self.client.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/recursionlab/recursive-ai-framework",
                "X-Title": "Recursive AI Framework - Extraction Engine"
            }

            payload = {
                "model": self.client.model,
                "messages": messages,
                "max_tokens": max_tokens
            }

            response = requests.post(
                self.client.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")

            result = response.json()

            # Extract content from OpenRouter response format
            content_text = result['choices'][0]['message']['content']

            # Return object that matches Anthropic SDK response format
            return OpenRouterMessage(content_text)

    def __init__(self, api_key: str, model: str = "anthropic/claude-3.5-sonnet"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.messages = self.Messages(self)
