import os
from dotenv import load_dotenv

from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI, OpenAI
from langchain_anthropic import ChatAnthropic, Anthropic

load_dotenv('.env', override=True)
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL")
LLM_TEMPERATURE = os.getenv("LLM_TEMPERATURE")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if "claude" in DEFAULT_MODEL:
    chat_model = ChatAnthropic(
        model=DEFAULT_MODEL,
        api_key=ANTHROPIC_API_KEY,
        temperature=LLM_TEMPERATURE,
    ).with_fallbacks(
        [
            ChatOpenAI(
                model=FALLBACK_MODEL,
                api_key=OPENAI_API_KEY,
                temperature=LLM_TEMPERATURE,
            )
        ]
    )
    chat_model_small = ChatAnthropic(
        model="claude-3-haiku-20240307",
        api_key=ANTHROPIC_API_KEY,
        temperature=LLM_TEMPERATURE,
    ).with_fallbacks(
        [
            ChatOpenAI(
                model=FALLBACK_MODEL,
                api_key=OPENAI_API_KEY,
                temperature=LLM_TEMPERATURE,
            )
        ]
    )
elif "gpt" in DEFAULT_MODEL:
    chat_model = ChatOpenAI(
        model=DEFAULT_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=LLM_TEMPERATURE,
    ).with_fallbacks(
        [
            ChatAnthropic(
                model=FALLBACK_MODEL,
                api_key=ANTHROPIC_API_KEY,
                temperature=LLM_TEMPERATURE,
            )
        ]
    )
    chat_model_small = ChatOpenAI(
        model="gpt-4o-mini-2024-07-18",
        api_key=OPENAI_API_KEY,
        temperature=LLM_TEMPERATURE,
    ).with_fallbacks(
        [
            ChatAnthropic(
                model=FALLBACK_MODEL,
                api_key=ANTHROPIC_API_KEY,
                temperature=LLM_TEMPERATURE,
            )
        ]
    )
else:
    raise ValueError("Invalid model name")
