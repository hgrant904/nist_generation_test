# Setup Guide: NIST CSF Conversational Agent

This guide walks you through setting up the Ollama-powered conversational agent from scratch.

## Prerequisites

Before starting, ensure you have:
- Python 3.9 or higher
- 8GB+ RAM available
- ~5GB free disk space for the model
- Internet connection for downloading dependencies

## Step 1: Install Ollama

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
Download the installer from [https://ollama.ai/download](https://ollama.ai/download)

## Step 2: Download the Model

After installing Ollama, download the llama3.1:8b model:

```bash
ollama pull llama3.1:8b
```

This will download approximately 4.7GB. Wait for it to complete.

Verify the model is installed:
```bash
ollama list
```

You should see `llama3.1:8b` in the list.

## Step 3: Start Ollama Service

Start the Ollama service in a terminal:
```bash
ollama serve
```

Keep this terminal running. The service will be available at `http://localhost:11434`.

To test if Ollama is working:
```bash
curl http://localhost:11434/api/tags
```

## Step 4: Set Up the Python Application

### Clone the repository
```bash
git clone <repository-url>
cd nist_generation_test
```

### Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure environment
```bash
cp .env.example .env
```

The default settings should work if Ollama is running on localhost:11434. If needed, edit `.env` to customize.

## Step 5: Run the Application

### Start the API server
```bash
python run.py
```

Or with make:
```bash
make run
```

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 6: Test the Application

### Option 1: Interactive API Docs
Open your browser to [http://localhost:8000/docs](http://localhost:8000/docs)

You'll see the Swagger UI where you can test all endpoints interactively.

### Option 2: Health Check
```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "ollama_available": true,
  "model_available": true,
  "configured_model": "llama3.1:8b",
  "available_models": ["llama3.1:8b"]
}
```

### Option 3: Send a Chat Message
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "message": "Hello! I run a small business and need help with cybersecurity.",
    "include_context": true
  }'
```

### Option 4: Run the Example Script
```bash
python examples/chat_example.py
```

## Step 7: Run Tests

### Run all tests
```bash
pytest
```

### Run only unit tests (no Ollama required)
```bash
pytest tests/unit/
```

### Run with coverage
```bash
pytest --cov=src --cov-report=html
```

Open `htmlcov/index.html` in your browser to view the coverage report.

## Troubleshooting

### "Cannot connect to Ollama"
- Ensure `ollama serve` is running in a terminal
- Check if port 11434 is available: `lsof -i :11434` (macOS/Linux)
- Verify Ollama is responding: `curl http://localhost:11434/api/tags`

### "Model not found"
- Run `ollama list` to see installed models
- Pull the model if missing: `ollama pull llama3.1:8b`
- Check the model name in `.env` matches exactly

### Slow responses
- First response may be slow as the model loads into memory
- Subsequent responses should be faster (2-5 seconds)
- Reduce `OLLAMA_NUM_PREDICT` in `.env` for shorter responses

### Port 8000 already in use
- Change `API_PORT` in `.env` to another port (e.g., 8001)
- Or find and stop the process using port 8000

### Import errors
- Ensure you activated the virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

## Docker Setup (Alternative)

If you prefer Docker:

```bash
# Build the image
docker-compose build

# Start the service
docker-compose up
```

Note: Ollama must still be running on your host machine.

## Next Steps

- Read the [README.md](README.md) for detailed API documentation
- Explore the example script in `examples/chat_example.py`
- Check out the system prompts in `src/prompts/system_prompts.py`
- Customize the agent for your specific use case

## Performance Tips

### Memory Management
- The model uses ~8GB RAM when loaded
- Close other memory-intensive applications
- On systems with limited RAM, consider using a smaller model

### CPU Optimization
- llama3.1:8b works well on modern CPUs
- Response time: ~2-5 seconds on typical hardware
- For faster responses, consider using a GPU-enabled setup

### Concurrent Users
- The application handles concurrent requests via request queuing
- Each user gets their own session with isolated conversation history
- For high traffic, consider load balancing multiple instances

## Support Resources

- **Ollama Documentation**: https://ollama.ai/docs
- **LangChain Documentation**: https://python.langchain.com
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **NIST CSF Reference**: https://www.nist.gov/cyberframework

## Common Commands Reference

```bash
# Start Ollama
ollama serve

# List models
ollama list

# Pull a model
ollama pull llama3.1:8b

# Test Ollama
curl http://localhost:11434/api/tags

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python run.py

# Run tests
pytest

# Clean up
make clean
```
