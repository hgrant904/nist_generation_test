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
# NIST Security Report Automation

Automate NIST security report generation for end users to easily generate comprehensive security reports.

## 🏗️ Project Structure

This is a monorepo containing the following components:

```
nist_generation_test/
├── backend/              # FastAPI backend service
│   ├── app/             # Application code
│   ├── tests/           # Backend tests
│   ├── Dockerfile       # Backend container configuration
│   └── requirements.txt # Python dependencies
├── frontend/            # Next.js frontend application
│   ├── src/            # Source code
│   ├── public/         # Static assets
│   ├── Dockerfile.dev  # Development container
│   └── package.json    # Node dependencies
├── docs/               # Project documentation
├── docker-compose.yml  # Docker orchestration
├── Makefile           # Development commands
└── .env.example       # Environment variable template
```

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:
- **Docker** (20.10+) and **Docker Compose** (2.0+)
- **Node.js** (20+) and **npm** (for local development without Docker)
- **Python** (3.11+) and **pip** (for local development without Docker)
- **Make** (optional, for convenience commands)

### Getting Started with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nist_generation_test
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration (optional for development)
   ```

3. **Start the services**
   ```bash
   make dev
   # Or without Make:
   docker-compose up
   ```

4. **Access the applications**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development without Docker

#### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example .env
# Edit .env with your configuration

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp ../.env.example .env.local
# Edit .env.local with your configuration

# Start the development server
npm run dev
```

#### Database Setup

For local development without Docker, you'll need to install and run PostgreSQL:

```bash
# On macOS with Homebrew
brew install postgresql@16
brew services start postgresql@16

# On Ubuntu/Debian
sudo apt-get install postgresql-16
sudo systemctl start postgresql

# Create database and user
psql postgres
CREATE DATABASE nist_reports;
CREATE USER nist_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE nist_reports TO nist_user;
\q
```

## 📦 Available Commands

If you have Make installed, you can use these convenience commands:

```bash
make help            # Show all available commands
make dev             # Start development environment
make up              # Start services in detached mode
make down            # Stop all services
make build           # Build Docker images
make rebuild         # Rebuild images from scratch
make restart         # Restart all services
make logs            # Show service logs
make clean           # Remove containers, volumes, and cache
make test            # Run all tests
make backend-test    # Run backend tests only
make frontend-test   # Run frontend tests only
make backend-shell   # Open shell in backend container
make frontend-shell  # Open shell in frontend container
make db-shell        # Open PostgreSQL shell
```

## 🔧 Configuration

### Environment Variables

The project uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

**Backend Configuration:**
- `BACKEND_PORT`: Backend server port (default: 8000)
- `DATABASE_URL`: PostgreSQL connection string
- `DEBUG`: Enable debug mode (default: true)
- `SECRET_KEY`: Application secret key
- `ALLOWED_ORIGINS`: CORS allowed origins

**Frontend Configuration:**
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
- `FRONTEND_PORT`: Frontend server port (default: 3000)

**Database Configuration:**
- `POSTGRES_HOST`: Database host (default: postgres)
- `POSTGRES_PORT`: Database port (default: 5432)
- `POSTGRES_DB`: Database name (default: nist_reports)
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Backend tests only
make backend-test
# Or: cd backend && pytest

# Frontend tests only
make frontend-test
# Or: cd frontend && npm test

# Backend tests with coverage
cd backend && pytest --cov=app tests/
```

## 📖 API Documentation

Once the backend is running, you can access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Technology Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Testing**: pytest

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Package Manager**: npm
- **HTTP Client**: Axios

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 16
- **Reverse Proxy**: (To be added)

## 🔄 Development Workflow

1. **Create a new branch** for your feature or bugfix
2. **Make your changes** following the coding standards
3. **Test your changes** locally
4. **Commit your changes** with descriptive commit messages
5. **Push your branch** and create a pull request

### Code Style

**Backend (Python):**
- Follow PEP 8 guidelines
- Use Black for formatting: `black .`
- Use Ruff for linting: `ruff check .`
- Type hints are encouraged

**Frontend (TypeScript):**
- Follow the project's ESLint configuration
- Use Prettier for formatting: `npm run format`
- Run type checking: `npm run type-check`

## 🐳 Docker Services

The `docker-compose.yml` defines three services:

1. **postgres**: PostgreSQL database with persistent volume
2. **backend**: FastAPI application with hot-reload
3. **frontend**: Next.js application with hot-reload

All services are connected via a custom bridge network `nist-network`.

### Volumes
- `postgres_data`: Persistent database storage
- `backend_cache`: Python cache directory

## 📝 Project Roadmap

- [x] Initial project setup
- [x] Docker containerization
- [x] Basic backend API structure
- [x] Basic frontend structure
- [ ] Database models and migrations
- [ ] Authentication system
- [ ] NIST API integration
- [ ] Report generation logic
- [ ] User dashboard
- [ ] Export functionality
- [ ] Deployment configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues, please:
- Open an issue on GitHub
- Contact the development team
- Refer to the documentation in the `docs/` directory

## 🙏 Acknowledgments

- NIST for providing security standards and guidelines
- FastAPI and Next.js communities for excellent frameworks
