import os
from dotenv import load_dotenv

from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI, OpenAI
from langchain_anthropic import ChatAnthropic, Anthropic

print("current directory", os.getcwd())
load_dotenv('.env', override=True)
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "claude-3-5-sonnet-latest")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "gpt-4o-2024-08-06")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.7))
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if "claude" in DEFAULT_MODEL:
    if not ANTHROPIC_API_KEY:
        raise ValueError("Anthropic API key is not set")
    
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
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set")
    
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
