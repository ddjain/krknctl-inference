# krknctl-ai

CLI tool for chaos engineering command generation using Qwen3-1.7B with LoRA.

## Installation

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install
uv pip install -e .
```

## Usage

```bash
krknctl-ai --prompt "crash the pod with name backend-service in default namespace"
```

### Options

```bash
# Verbose output
krknctl-ai --prompt "simulate a pod crash" --verbose

# Specify device
krknctl-ai --prompt "test" --device cpu

# Custom max tokens
krknctl-ai --prompt "stress CPU" --max-tokens 256
```

## Models

- Base: `Qwen/Qwen3-1.7B`
- LoRA: `ddjain/Qwen3-1.7B-krknctl-lora`

Both models are public on HuggingFace. First run downloads ~1.7GB to cache.
