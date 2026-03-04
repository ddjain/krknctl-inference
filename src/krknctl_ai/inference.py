"""Core inference engine for krknctl-ai"""

from typing import Optional

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from .config import Config


def get_device(device_str: Optional[str] = None) -> torch.device:
    """Auto-detect best device: MPS (Apple Silicon) > CUDA > CPU"""
    if device_str:
        return torch.device(device_str)

    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def load_model_and_tokenizer(config: Config):
    """Load base model + LoRA adapter from HuggingFace Hub

    Args:
        config: Configuration object with model paths and HF token

    Returns:
        tuple: (model, tokenizer, device)
    """
    # 1. Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        config.base_model,
        token=config.hf_token
    )
    tokenizer.pad_token = tokenizer.eos_token

    # 2. Determine device
    device = get_device(config.device)

    # 3. Load base model
    base_model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        token=config.hf_token,
        torch_dtype=torch.bfloat16
    ).to(device)

    # 4. Load LoRA adapter from HuggingFace Hub
    model = PeftModel.from_pretrained(
        base_model,
        config.adapter_model,
        subfolder=config.adapter_subfolder,
        token=config.hf_token
    )
    model.eval()

    return model, tokenizer, device


def generate_response(
    model,
    tokenizer,
    device: torch.device,
    prompt: str,
    config: Config
) -> str:
    """Generate response using chat template

    Args:
        model: The PEFT model with LoRA adapter
        tokenizer: The tokenizer
        device: The device to run inference on
        prompt: User instruction prompt
        config: Configuration object

    Returns:
        str: Generated response
    """
    # Apply chat template
    messages = [{"role": "user", "content": prompt}]
    formatted_prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Tokenize and move to device
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)

    # Generate with torch.no_grad() for memory efficiency
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=config.max_tokens,
            do_sample=config.do_sample,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Extract only new tokens (exclude input)
    new_tokens = outputs[0][inputs.input_ids.shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
