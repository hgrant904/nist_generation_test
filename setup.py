from setuptools import setup, find_packages

setup(
    name="nist-csf-agent",
    version="1.0.0",
    description="Ollama-powered conversational agent for NIST CSF questionnaire follow-ups",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.2.16",
        "langchain-ollama>=0.1.3",
        "langchain-community>=0.2.16",
        "fastapi>=0.115.0",
        "uvicorn[standard]>=0.30.6",
        "sqlalchemy>=2.0.35",
        "aiosqlite>=0.20.0",
        "pydantic>=2.9.2",
        "pydantic-settings>=2.5.2",
        "python-dotenv>=1.0.1",
        "httpx>=0.27.2",
        "sse-starlette>=2.1.3",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.3",
            "pytest-asyncio>=0.24.0",
            "pytest-mock>=3.14.0",
            "pytest-cov>=4.1.0",
        ],
    },
    python_requires=">=3.9",
)
