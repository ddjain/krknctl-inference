"""Configuration management for krknctl-ai"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration for krknctl-ai inference"""
    hf_token: Optional[str] = None
    base_model: str = "Qwen/Qwen3-1.7B"
    adapter_model: str = "ddjain/Qwen3-1.7B-krknctl-lora"
    adapter_subfolder: str = "lora_adapter"
    max_tokens: int = 128
    do_sample: bool = False  # Deterministic output
    device: Optional[str] = None  # Auto-detect if None


def load_config_from_env() -> Config:
    """Load configuration from environment variables"""
    # Load .env file if it exists
    load_dotenv()

    return Config(
        hf_token=os.getenv("HF_TOKEN"),
    )
