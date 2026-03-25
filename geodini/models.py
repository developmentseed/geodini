"""Centralized LLM model configuration.

Two tiers control all agent models:
- MODEL_LIGHT: fast/cheap tasks (rephrase, routing, complex parse, rerank)
- MODEL_HEAVY: SQL generation and error correction

Each model's provider is extracted from its prefix (e.g. "anthropic"
from "anthropic:claude-sonnet-4-6"). The provider-specific API key env
var (e.g. ANTHROPIC_API_KEY) takes priority; LLM_API_KEY is used as a
shared fallback for any provider that doesn't have its own key set.

Supported provider prefixes: openai, anthropic, groq, mistral.
Bedrock uses AWS creds (AWS_ACCESS_KEY_ID, etc.).
Ollama uses OLLAMA_BASE_URL (no API key needed).
"""

import os

MODEL_LIGHT = os.getenv("MODEL_LIGHT", "anthropic:claude-haiku-4-5")
MODEL_HEAVY = os.getenv("MODEL_HEAVY", "anthropic:claude-sonnet-4-6")

KEY_MAP = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "groq": "GROQ_API_KEY",
    "mistral": "MISTRAL_API_KEY",
}

llm_fallback_key = os.getenv("LLM_API_KEY", "")
for model in (MODEL_LIGHT, MODEL_HEAVY):
    provider = model.split(":")[0]
    if provider in KEY_MAP and llm_fallback_key:
        os.environ.setdefault(KEY_MAP[provider], llm_fallback_key)
