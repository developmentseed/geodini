"""Centralized LLM model configuration.

Two tiers control all agent models:
- MODEL_LIGHT: fast/cheap tasks (rephrase, routing, complex parse, rerank)
- MODEL_HEAVY: SQL generation and error correction

LLM_API_KEY is a convenience env var that auto-maps to the correct
provider-specific env var based on the model prefix. For multi-provider
setups, set provider-specific env vars directly instead.

Supported provider prefixes: openai, anthropic, groq, mistral.
Bedrock uses AWS creds (AWS_ACCESS_KEY_ID, etc.).
Ollama uses OLLAMA_BASE_URL (no API key needed).
"""

import os

MODEL_LIGHT = os.getenv("MODEL_LIGHT", "anthropic:claude-haiku-4-5")
MODEL_HEAVY = os.getenv("MODEL_HEAVY", "anthropic:claude-sonnet-4-6")

_KEY_MAP = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "groq": "GROQ_API_KEY",
    "mistral": "MISTRAL_API_KEY",
}

_llm_key = os.getenv("LLM_API_KEY", "")
if _llm_key:
    _provider = MODEL_LIGHT.split(":")[0]
    if _provider in _KEY_MAP:
        os.environ.setdefault(_KEY_MAP[_provider], _llm_key)
    _heavy_provider = MODEL_HEAVY.split(":")[0]
    if _heavy_provider != _provider and _heavy_provider in _KEY_MAP:
        os.environ.setdefault(_KEY_MAP[_heavy_provider], _llm_key)
