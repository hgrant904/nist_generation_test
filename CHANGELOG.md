# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-10-15

### Added

#### Core Features
- **Ollama Integration**: Full integration with Ollama for local LLM inference using llama3.1:8b
- **Conversational Agent**: Context-aware AI assistant specialized in NIST Cybersecurity Framework
- **Conversation Memory**: Database-backed persistent chat history across sessions
- **Context Retrieval**: Integration with prior questionnaire responses for intelligent follow-ups
- **Streaming Support**: Real-time chat responses using Server-Sent Events
- **Health Monitoring**: Built-in health check endpoint for Ollama connectivity and model availability

#### API Endpoints
- `GET /api/v1/health` - Check Ollama service status and model availability
- `POST /api/v1/chat` - Send message and receive complete response
- `POST /api/v1/chat/stream` - Send message and receive streaming response
- `GET /api/v1/chat/history/{session_id}` - Retrieve conversation history

#### System Prompts
- NIST CSF-specialized system prompt for professional services and small businesses
- Focus areas: cloud services, data handling, access controls, backups, incident response, vendor security, training
- Non-technical language optimized for business owners without IT staff

#### Database Schema
- `conversations` table: Session management and conversation tracking
- `messages` table: Chat history with role, content, and timestamps
- `questionnaire_responses` table: Prior assessment context for intelligent follow-ups

#### Testing
- Unit tests for prompt generation and Ollama service (13 tests)
- Integration tests with mocked API endpoints (7 tests)
- Live integration tests for Ollama connectivity (3 tests, skip if unavailable)
- 100% pass rate on unit and integration tests

#### Documentation
- Comprehensive README with setup instructions and usage examples
- Detailed SETUP guide with troubleshooting
- Complete API documentation with examples in multiple languages
- Quick start guide for 5-minute setup
- Example script demonstrating all API features

#### Configuration
- Environment-based configuration with sensible defaults
- Configurable Ollama connection settings
- Adjustable temperature and token limits
- Database connection string configuration

#### Developer Tools
- Makefile with common development commands
- Docker and docker-compose configuration
- Pre-configured pytest with async support
- Virtual environment setup scripts

#### Dependencies
- **LangChain**: 0.2.16 with langchain-ollama integration
- **FastAPI**: 0.115.0 for REST API
- **SQLAlchemy**: 2.0.35 with async support
- **Pydantic**: 2.9.2 for data validation
- **pytest**: 8.3.3 with async support

### Technical Details

#### Architecture
- Async/await throughout for optimal I/O performance
- Service layer pattern for business logic separation
- Repository pattern for database access
- Clean separation of concerns across modules

#### Performance
- Optimized for CPU-only inference
- Expected response times: 2-5 seconds per message
- Streaming for improved perceived performance
- Request queuing ready for concurrent users

#### Security
- No API keys required (local inference)
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy ORM
- CORS support for web clients

#### Code Quality
- Type hints on all functions
- Consistent coding style following Python best practices
- Comprehensive error handling
- Logging throughout the application

### Configuration Files
- `.env.example` - Environment variable template
- `.gitignore` - Git ignore rules
- `pytest.ini` - Test configuration
- `requirements.txt` - Python dependencies
- `setup.py` - Package configuration
- `Dockerfile` - Container build configuration
- `docker-compose.yml` - Container orchestration
- `Makefile` - Development commands

### Examples
- `examples/chat_example.py` - Complete usage demonstration including:
  - Health checks
  - Non-streaming chat
  - Streaming chat
  - History retrieval

### Known Limitations
- CPU-only inference (no GPU acceleration)
- Single-model support (llama3.1:8b)
- No authentication/authorization
- No rate limiting
- SQLite only (no PostgreSQL/MySQL support yet)

### Future Enhancements
- GPU acceleration support
- Multi-model switching
- Authentication with JWT
- Rate limiting per IP/session
- PostgreSQL support
- Questionnaire response API endpoints
- Web UI frontend
- Export conversation transcripts

## Version History

- **1.0.0** (2024-10-15): Initial release with full Ollama integration and conversational agent
