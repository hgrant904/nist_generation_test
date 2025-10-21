# Quick Start Guide

Get the NIST CSF Conversational Agent up and running in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- ~5GB free disk space
- 8GB+ RAM

## Step 1: Install Ollama (2 minutes)

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:** Download from https://ollama.ai/download

## Step 2: Start Ollama & Download Model (2 minutes)

```bash
# Start Ollama (keep this terminal open)
ollama serve

# In a new terminal, download the model
ollama pull llama3.1:8b
```

## Step 3: Set Up the Application (1 minute)

```bash
# Clone and navigate to project
cd nist_generation_test

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

## Step 4: Run the Application (30 seconds)

```bash
# Start the API server
python run.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 5: Test It! (30 seconds)

**Option A: Web Browser**

Open http://localhost:8000/docs in your browser and try the interactive API.

**Option B: Command Line**

```bash
# Check health
curl http://localhost:8000/api/v1/health

# Send a message
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "message": "Hello! I run a small business and need cybersecurity advice."
  }'
```

**Option C: Example Script**

```bash
python examples/chat_example.py
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [API.md](API.md) for complete API reference
- Review [SETUP.md](SETUP.md) for troubleshooting

## Common Issues

**"Cannot connect to Ollama"**
→ Make sure `ollama serve` is running in another terminal

**"Model not found"**
→ Run `ollama pull llama3.1:8b`

**"Port 8000 already in use"**
→ Edit `.env` and change `API_PORT=8001`

## What You've Built

✅ Local LLM-powered chat agent (no cloud API keys!)  
✅ NIST CSF security expertise built-in  
✅ Conversational memory across sessions  
✅ Real-time streaming responses  
✅ REST API with OpenAPI docs  

Enjoy! 🚀
