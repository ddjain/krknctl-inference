# krknctl-ai

Standalone Python CLI tool for chaos engineering command generation using the Qwen3-1.7B base model with a LoRA adapter.

## Features

- 🚀 Direct inference using Qwen3-1.7B + LoRA from HuggingFace Hub
- 🔧 Packaged as a CLI executable (`krknctl-ai`)
- 🎯 Generates deterministic chaos engineering commands
- 🔥 Supports Apple Silicon (MPS), NVIDIA GPUs (CUDA), and CPU
- 📦 Modern Python tooling with `uv` for dependency management

## Models

- **Base Model**: `Qwen/Qwen3-1.7B` (from HuggingFace Hub)
- **LoRA Adapter**: `ddjain/Qwen3-1.7B-krknctl-lora` (from HuggingFace Hub)

## Requirements

- Python 3.8+
- ~2GB disk space for model cache (first run)
- HuggingFace API token (optional, only for private/gated models or to bypass rate limits)

## Installation

### Using uv (Recommended)

```bash
# Clone or navigate to the project directory
cd /Users/darjain/sample-projects/krknctl-inference

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or for fish shell: source .venv/bin/activate.fish
# or for Windows: .venv\Scripts\activate

# Install the package
uv pip install -e .

krknctl-ai --prompt "crash the pod with name backend-service in default namespace"
```


## Configuration

### HuggingFace Token (Optional)

Both models (`Qwen/Qwen3-1.7B` and `ddjain/Qwen3-1.7B-krknctl-lora`) are **public** and work without authentication.

However, you may want to set a HuggingFace token to:
- Access private/gated models
- Bypass rate limits
- Increase download speeds

Get a token from: https://huggingface.co/settings/tokens

Set your token using one of these methods:

**Option 1: Environment variable**
```bash
export HF_TOKEN=hf_your_token_here
```

**Option 2: .env file (recommended)**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your token
echo "HF_TOKEN=hf_your_token_here" > .env
```

**Option 3: CLI argument**
```bash
krknctl-ai --hf-token hf_your_token_here --prompt "your prompt"
```

## Usage

### Basic Usage

```bash
krknctl-ai --prompt "crash the pod with name backend-service in default namespace"
```

### With Options

```bash
# Verbose output (shows loading progress)
krknctl-ai --prompt "simulate a pod crash" --verbose

# Specify max tokens
krknctl-ai --prompt "stress CPU on nodes" --max-tokens 256

# Force specific device
krknctl-ai --prompt "test" --device cpu

# Custom model selection
krknctl-ai --prompt "test" --model "Qwen/Qwen3-1.7B" --lora-adapter "custom/lora-model"

# With HF token for private models
krknctl-ai --prompt "test" --hf-token "hf_your_token"

# All options combined
krknctl-ai --prompt "your prompt" --max-tokens 200 --device mps --verbose
```

### Example Prompts

```bash
# Pod crash simulation
krknctl-ai --prompt "crash the pod with name backend-service in default namespace"

# CPU stress test
krknctl-ai --prompt "stress CPU on nodes labeled pool=gpu for 3 minutes using 8 cores at 80 percent"

# Network chaos
krknctl-ai --prompt "simulate network latency for pods with label app=checkout in payments namespace"

# Pod crash with label selector
krknctl-ai --prompt "simulate a pod crash in the payments namespace targeting pods with label app=checkout"
```

### Run Without Installation

You can run the tool directly with `uv` without installing it:

```bash
uv run krknctl-ai --prompt "your prompt"
```

## CLI Options

```
usage: krknctl-ai [-h] --prompt PROMPT [--hf-token HF_TOKEN] [--model MODEL]
                  [--lora-adapter LORA_ADAPTER] [--max-tokens MAX_TOKENS]
                  [--device {auto,mps,cuda,cpu}] [--verbose]

options:
  -h, --help            Show this help message and exit
  --prompt PROMPT, -p PROMPT
                        Instruction prompt for command generation
  --hf-token HF_TOKEN   HuggingFace token (optional, only needed for private/gated models)
  --model MODEL         Base model name (default: Qwen/Qwen3-1.7B)
  --lora-adapter LORA_ADAPTER
                        LoRA adapter model (default: ddjain/Qwen3-1.7B-krknctl-lora)
  --max-tokens MAX_TOKENS
                        Maximum tokens to generate (default: 128)
  --device {auto,mps,cuda,cpu}
                        Device to use for inference (default: auto)
  --verbose, -v         Enable verbose output
```

## How It Works

1. **Model Loading**: Downloads and caches the Qwen3-1.7B base model and LoRA adapter from HuggingFace Hub (first run only)
2. **Device Detection**: Automatically selects the best available device (MPS > CUDA > CPU)
3. **Inference**: Applies chat template to your prompt and generates deterministic output
4. **Output**: Returns the generated chaos engineering command

### First Run

On the first run, the tool will download models (~1.7GB) to `~/.cache/huggingface/hub/`. This may take a few minutes depending on your internet connection.

```bash
krknctl-ai --prompt "test" --verbose
# Loading models from HuggingFace Hub...
#   Base model: Qwen/Qwen3-1.7B
#   LoRA adapter: ddjain/Qwen3-1.7B-krknctl-lora
#   Device: mps
#
# Generating response...
# [output]
```

### Subsequent Runs

After the first run, models are cached locally and loading is much faster:

```bash
krknctl-ai --prompt "crash pod backend" --verbose
# Loading models from HuggingFace Hub...  # Uses cache
#   Device: mps
#
# Generating response...
# [output]
```

## Troubleshooting

### Command Not Found

**Error:**
```
krknctl-ai: command not found
```

**Solution:**
1. Make sure you've activated the virtual environment: `source .venv/bin/activate`
2. Verify installation: `which krknctl-ai`
3. If still not found, reinstall: `uv pip install -e .`

### Out of Memory

**Error:**
```
RuntimeError: MPS backend out of memory
```

**Solution:**
1. Try using CPU instead: `krknctl-ai --prompt "..." --device cpu`
2. Reduce max tokens: `krknctl-ai --prompt "..." --max-tokens 64`
3. Close other applications to free up memory

### Network/Download Issues

**Error:**
```
HTTPError: 401 Unauthorized
```

**Solution:**
1. Verify your HuggingFace token is valid
2. Check that you have access to the models (both are public)
3. Try regenerating your token at https://huggingface.co/settings/tokens

### Model Cache Location

Models are cached at: `~/.cache/huggingface/hub/`

To clear the cache:
```bash
rm -rf ~/.cache/huggingface/hub/models--Qwen--Qwen3-1.7B
rm -rf ~/.cache/huggingface/hub/models--ddjain--Qwen3-1.7B-krknctl-lora
```

## Development

### Project Structure

```
krknctl-inference/
├── pyproject.toml              # Project config & dependencies
├── README.md                   # This file
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore patterns
└── src/
    └── krknctl_ai/
        ├── __init__.py        # Package initialization
        ├── config.py          # Configuration management
        ├── inference.py       # Core inference engine
        └── cli.py             # CLI entry point
```

### Running Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests (when available)
pytest
```

### Code Quality

The tool generates deterministic output by default (`do_sample=False`). To verify:

```bash
# Run the same prompt twice
krknctl-ai --prompt "test prompt" > output1.txt
krknctl-ai --prompt "test prompt" > output2.txt

# Outputs should be identical
diff output1.txt output2.txt
```

## License

MIT

## Acknowledgments

- Base model: [Qwen/Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B)
- LoRA adapter: [ddjain/Qwen3-1.7B-krknctl-lora](https://huggingface.co/ddjain/Qwen3-1.7B-krknctl-lora)
- Built with: PyTorch, Transformers, PEFT
