# NIST CSF Conversational Agent

An Ollama-powered conversational agent using llama3.1:8b for intelligent NIST Cybersecurity Framework (CSF) questionnaire follow-ups, designed for professional services firms and small businesses.

## Features

- 🤖 **Ollama Integration**: Powered by llama3.1:8b running locally (no API keys required)
- 💬 **Conversational AI**: Context-aware follow-up questions about security practices
- 🗄️ **Persistent Memory**: Database-backed chat history and conversation memory
- 📋 **Context Retrieval**: Integrates prior questionnaire responses to inform questions
- 🌊 **Streaming Support**: Real-time chat experience with Server-Sent Events
- 🏥 **Health Monitoring**: Built-in health checks for Ollama connectivity
- 🧪 **Comprehensive Testing**: Unit and integration tests with mock support for CI/CD
- 📚 **API Documentation**: Auto-generated OpenAPI/Swagger docs

## Tech Stack

- **LLM Framework**: LangChain with Ollama
- **Model**: llama3.1:8b (local inference)
- **API Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy (async)
- **Testing**: pytest with async support

## Prerequisites

### 1. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai):

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Download llama3.1:8b Model

```bash
ollama pull llama3.1:8b
```

This will download approximately 4.7GB. The model requires:
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: ~5GB free space
- **CPU**: Works on CPU-only systems (no GPU required)

### 3. Start Ollama Service

```bash
ollama serve
```

The service will start on `http://localhost:11434` by default.

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd nist_generation_test
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env if you need to change default settings
```

## Usage

### Starting the API Server

```bash
python -m src.main
```

Or with uvicorn directly:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### API Endpoints

#### 1. Health Check

Check Ollama connectivity and model availability:

```bash
curl http://localhost:8000/api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "ollama_available": true,
  "model_available": true,
  "configured_model": "llama3.1:8b",
  "available_models": ["llama3.1:8b", "mistral:7b"]
}
```

#### 2. Chat (Non-Streaming)

Send a message and receive a complete response:

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user-123",
    "message": "I run a small accounting firm. What cloud services should I secure?",
    "include_context": true
  }'
```

Response:
```json
{
  "session_id": "user-123",
  "message": "Great question! For an accounting firm...",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### 3. Chat (Streaming)

Receive real-time streaming responses:

```bash
curl -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user-123",
    "message": "Tell me about backup best practices"
  }'
```

#### 4. Get Chat History

Retrieve conversation history for a session:

```bash
curl http://localhost:8000/api/v1/chat/history/user-123
```

Response:
```json
{
  "session_id": "user-123",
  "messages": [
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2024-01-15T10:00:00"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you?",
      "timestamp": "2024-01-15T10:00:01"
    }
  ]
}
```

## Configuration

Environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_MODEL` | `llama3.1:8b` | Model to use |
| `OLLAMA_TEMPERATURE` | `0.7` | Response randomness (0.0-1.0) |
| `OLLAMA_NUM_PREDICT` | `512` | Max tokens to generate |
| `DATABASE_URL` | `sqlite+aiosqlite:///./nist_csf.db` | Database connection string |
| `API_HOST` | `0.0.0.0` | API server host |
| `API_PORT` | `8000` | API server port |
| `LOG_LEVEL` | `INFO` | Logging level |

## Testing

### Run All Tests

```bash
pytest
```

### Run Unit Tests Only

```bash
pytest tests/unit/
```

### Run Integration Tests (requires Ollama)

```bash
pytest tests/integration/
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

### Skip Live Ollama Tests

By default, tests marked with `@pytest.mark.integration` will skip if Ollama is not available. To run them:

```bash
pytest -m integration
```

## Architecture

```
src/
├── api/
│   └── routes.py          # FastAPI endpoints
├── database/
│   ├── models.py          # SQLAlchemy models
│   └── connection.py      # Database setup
├── services/
│   ├── ollama_service.py  # Ollama client wrapper
│   └── conversation_service.py  # Business logic
├── prompts/
│   └── system_prompts.py  # LLM system prompts
├── models/
│   └── schemas.py         # Pydantic models
├── config.py              # Configuration management
└── main.py                # Application entry point

tests/
├── unit/                  # Unit tests (mocked)
└── integration/           # Integration tests
```

## System Prompt

The agent is configured with a specialized system prompt focusing on:

- **Professional services and small business context**
- **NIST CSF framework understanding**
- **Security questionnaire clarifications**
- **Non-technical language** for business owners

Key areas of inquiry:
- ☁️ Cloud service usage (Microsoft 365, Google Workspace, etc.)
- 🔒 Client data handling and storage
- 👥 Employee access controls
- 💾 Backup and disaster recovery
- 🚨 Incident response
- 🤝 Third-party vendor security
- 📚 Security awareness training

## Performance

Optimized for CPU-only inference:
- **Response Time**: ~2-5 seconds per message
- **Memory Usage**: ~8GB RAM for model + application
- **Concurrency**: Request queuing for multiple users
- **Streaming**: Immediate chunk delivery for better UX

## Troubleshooting

### Ollama Connection Failed

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama service
ollama serve
```

### Model Not Found

```bash
# List available models
ollama list

# Pull the model
ollama pull llama3.1:8b
```

### Slow Responses

- Reduce `OLLAMA_NUM_PREDICT` to generate shorter responses
- Ensure no other resource-intensive processes are running
- Consider using a smaller model like `llama3.1:7b` if available

### Database Issues

```bash
# Remove existing database to reset
rm nist_csf.db

# Restart the application to recreate tables
python -m src.main
```

## Development

### Adding New Features

1. Create feature branch
2. Implement changes with tests
3. Run test suite: `pytest`
4. Update documentation
5. Submit pull request

### Code Style

The project follows Python best practices:
- Type hints for function signatures
- Async/await for I/O operations
- Pydantic for data validation
- SQLAlchemy for database operations

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Support

For issues or questions:
- Open a GitHub issue
- Check Ollama documentation: https://ollama.ai/docs
- Review LangChain docs: https://python.langchain.com
