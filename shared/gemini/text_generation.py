# shared/gemini/text_generation.py
import sys
from pathlib import Path
from typing import Optional

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from google.genai import types as genai_types
from shared.gemini.client import initialize_gemini

DEFAULT_TEXT_MODEL = "gemini-2.5-flash"

def _build_text_config(
    system_instruction: Optional[str] = None,
    temperature: Optional[float] = None,
    disable_thinking: bool = False,
) -> Optional[genai_types.GenerateContentConfig]:
    """Builds the generation config for a text generation call."""
    config_params = {}
    if system_instruction:
        config_params["system_instruction"] = system_instruction
    if temperature is not None:
        config_params["temperature"] = temperature
    if disable_thinking:
        config_params["thinking_config"] = genai_types.ThinkingConfig(thinking_budget=0)

    if config_params:
        return genai_types.GenerateContentConfig(**config_params)
    return None

def generate_text(
    prompt: str,
    model: str = DEFAULT_TEXT_MODEL,
    system_instruction: Optional[str] = None,
    temperature: Optional[float] = None,
    disable_thinking: bool = False,
) -> str:
    """
    Generates text from a prompt using the Gemini API.
    """
    client = initialize_gemini()
    config = _build_text_config(system_instruction, temperature, disable_thinking)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    return response.text

async def generate_text_async(
    prompt: str,
    model: str = DEFAULT_TEXT_MODEL,
    system_instruction: Optional[str] = None,
    temperature: Optional[float] = None,
    disable_thinking: bool = False,
) -> str:
    """
    Asynchronously generates text from a prompt using the Gemini API.
    """
    client = initialize_gemini()
    config = _build_text_config(system_instruction, temperature, disable_thinking)
    response = await client.models.generate_content_async(
        model=model,
        contents=prompt,
        config=config,
    )
    return response.text
