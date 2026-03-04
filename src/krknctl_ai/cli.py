"""CLI interface for krknctl-ai"""

import sys
import argparse
from .config import load_config_from_env
from .inference import load_model_and_tokenizer, generate_response


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI"""
    parser = argparse.ArgumentParser(
        prog="krknctl-ai",
        description="Chaos engineering command generation using Qwen3-1.7B + LoRA"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Instruction prompt for command generation"
    )
    parser.add_argument(
        "--hf-token",
        help="HuggingFace token (optional, only needed for private/gated models)"
    )
    parser.add_argument(
        "--model",
        help="Base model name (default: Qwen/Qwen3-1.7B)"
    )
    parser.add_argument(
        "--lora-adapter",
        help="LoRA adapter model (default: ddjain/Qwen3-1.7B-krknctl-lora)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=128,
        help="Maximum tokens to generate (default: 128)"
    )
    parser.add_argument(
        "--device",
        choices=["auto", "mps", "cuda", "cpu"],
        default="auto",
        help="Device to use for inference (default: auto)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    return parser


def main():
    """Main entry point for krknctl-ai command"""
    # 1. Parse arguments
    parser = create_parser()
    args = parser.parse_args()

    # Validate prompt is not empty
    if not args.prompt.strip():
        print("ERROR: Prompt cannot be empty", file=sys.stderr)
        sys.exit(1)

    # 2. Load config from environment
    config = load_config_from_env()

    # Apply CLI overrides
    if args.hf_token:
        config.hf_token = args.hf_token
    if args.model:
        config.base_model = args.model
    if args.lora_adapter:
        config.adapter_model = args.lora_adapter
    config.max_tokens = args.max_tokens
    if args.device != "auto":
        config.device = args.device

    # 3. Load model and generate
    try:
        if args.verbose:
            print("Loading models from HuggingFace Hub...", file=sys.stderr)
            print(f"  Base model: {config.base_model}", file=sys.stderr)
            print(f"  LoRA adapter: {config.adapter_model}", file=sys.stderr)
            if config.hf_token:
                print("  Using HF token: Yes", file=sys.stderr)

        model, tokenizer, device = load_model_and_tokenizer(config)

        if args.verbose:
            print(f"  Device: {device}", file=sys.stderr)
            print("", file=sys.stderr)
            print("Generating response...", file=sys.stderr)

        response = generate_response(model, tokenizer, device, args.prompt, config)
        print(response)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
