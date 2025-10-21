from setuptools import setup, find_packages

setup(
    name="nist-questionnaire-engine",
    version="1.0.0",
    description="NIST Security Report Automation Questionnaire Engine",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "sqlalchemy>=2.0.23",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "alembic>=1.12.1",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "httpx>=0.25.2",
        ]
    },
    python_requires=">=3.8",
)
