# Project Structure

This document provides a detailed overview of the NIST Reports monorepo structure.

## Directory Tree

```
nist_generation_test/
├── backend/                    # FastAPI backend service
│   ├── app/                   # Application source code
│   │   ├── __init__.py
│   │   └── main.py           # FastAPI application entry point
│   ├── tests/                # Backend test suite
│   │   ├── __init__.py
│   │   └── test_main.py     # Main application tests
│   ├── .dockerignore         # Docker ignore patterns
│   ├── Dockerfile            # Backend container configuration
│   ├── pyproject.toml        # Poetry configuration (optional)
│   ├── requirements.txt      # Python dependencies
│   └── README.md            # Backend documentation
│
├── frontend/                  # Next.js frontend application
│   ├── src/                  # Source code directory
│   │   └── app/             # Next.js App Router directory
│   │       ├── layout.tsx   # Root layout component
│   │       └── page.tsx     # Home page component
│   ├── public/              # Static assets
│   │   └── .gitkeep
│   ├── .dockerignore        # Docker ignore patterns
│   ├── .eslintrc.json       # ESLint configuration
│   ├── .prettierrc          # Prettier configuration
│   ├── Dockerfile           # Production container
│   ├── Dockerfile.dev       # Development container
│   ├── next.config.js       # Next.js configuration
│   ├── package.json         # Node.js dependencies
│   ├── tsconfig.json        # TypeScript configuration
│   └── README.md           # Frontend documentation
│
├── docs/                     # Project documentation
│   ├── README.md            # Documentation index
│   ├── architecture.md      # System architecture
│   └── development.md       # Development guide
│
├── scripts/                  # Utility scripts
│   ├── init-project.sh      # Project initialization script
│   ├── health-check.sh      # Service health check script
│   └── db-init.sql          # Database initialization SQL
│
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore patterns
├── CONTRIBUTING.md          # Contribution guidelines
├── docker-compose.yml       # Docker orchestration configuration
├── LICENSE                  # Project license (MIT)
├── Makefile                 # Development commands
├── PROJECT_STRUCTURE.md     # This file
├── README.md                # Main project documentation
└── SETUP.md                 # Setup instructions
```

## Backend Structure (`backend/`)

### Current Structure
```
backend/
├── app/
│   ├── __init__.py          # Package initialization
│   └── main.py              # FastAPI app, CORS, basic endpoints
├── tests/
│   ├── __init__.py
│   └── test_main.py         # Basic API tests
├── .dockerignore
├── Dockerfile
├── pyproject.toml           # Poetry/build configuration
├── requirements.txt         # pip dependencies
└── README.md
```

### Recommended Future Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI initialization
│   ├── config.py            # Configuration management
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   └── v1/             # API version 1
│   │       ├── __init__.py
│   │       ├── router.py   # Version router
│   │       └── endpoints/  # Individual endpoints
│   │           ├── __init__.py
│   │           ├── auth.py
│   │           ├── reports.py
│   │           └── users.py
│   ├── db/                  # Database
│   │   ├── __init__.py
│   │   ├── base.py         # Base class
│   │   ├── session.py      # Session management
│   │   └── init_db.py      # Database initialization
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── report.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── report.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── report.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── security.py
│       └── nist_api.py
└── tests/
    ├── __init__.py
    ├── conftest.py          # Pytest fixtures
    ├── api/                 # API tests
    ├── services/            # Service tests
    └── utils/               # Utility tests
```

## Frontend Structure (`frontend/`)

### Current Structure
```
frontend/
├── src/
│   └── app/
│       ├── layout.tsx       # Root layout
│       └── page.tsx         # Home page
├── public/
│   └── .gitkeep
├── .eslintrc.json
├── .prettierrc
├── Dockerfile
├── Dockerfile.dev
├── next.config.js
├── package.json
├── tsconfig.json
└── README.md
```

### Recommended Future Structure
```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Home page
│   │   ├── api/            # API routes (if needed)
│   │   ├── reports/        # Reports pages
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   ├── auth/           # Authentication pages
│   │   │   ├── login/
│   │   │   └── register/
│   │   └── dashboard/      # Dashboard pages
│   ├── components/          # React components
│   │   ├── ui/             # UI components
│   │   ├── forms/          # Form components
│   │   └── layout/         # Layout components
│   ├── lib/                 # Utility functions
│   │   ├── api.ts          # API client
│   │   ├── auth.ts         # Auth utilities
│   │   └── utils.ts        # General utilities
│   ├── hooks/               # Custom React hooks
│   │   ├── useAuth.ts
│   │   └── useReports.ts
│   ├── types/               # TypeScript types
│   │   ├── report.ts
│   │   └── user.ts
│   └── styles/              # Global styles
│       └── globals.css
└── public/                  # Static assets
    ├── images/
    └── icons/
```

## Configuration Files

### Root Level

- **`.env.example`** - Template for environment variables
- **`.gitignore`** - Specifies files Git should ignore
- **`docker-compose.yml`** - Orchestrates all services
- **`Makefile`** - Convenience commands for development
- **`LICENSE`** - MIT License
- **`README.md`** - Main project documentation
- **`SETUP.md`** - Detailed setup instructions
- **`CONTRIBUTING.md`** - Guidelines for contributors

### Backend Configuration

- **`pyproject.toml`** - Poetry/project metadata, tool configurations
- **`requirements.txt`** - Python dependencies
- **`Dockerfile`** - Container image for backend
- **`.dockerignore`** - Files to exclude from Docker build

### Frontend Configuration

- **`package.json`** - Node.js dependencies and scripts
- **`tsconfig.json`** - TypeScript compiler configuration
- **`next.config.js`** - Next.js configuration
- **`.eslintrc.json`** - ESLint rules
- **`.prettierrc`** - Prettier formatting rules
- **`Dockerfile`** - Production container image
- **`Dockerfile.dev`** - Development container image
- **`.dockerignore`** - Files to exclude from Docker build

## Docker Services

### PostgreSQL (Database)
- **Image**: `postgres:16-alpine`
- **Port**: 5432
- **Volume**: `postgres_data` (persistent storage)
- **Network**: `nist-network`
- **Health Check**: Enabled

### Backend (FastAPI)
- **Build Context**: `./backend`
- **Port**: 8000
- **Volumes**: 
  - `./backend:/app` (code hot-reload)
  - `backend_cache:/app/__pycache__`
- **Network**: `nist-network`
- **Depends On**: postgres (with health check)

### Frontend (Next.js)
- **Build Context**: `./frontend`
- **Port**: 3000
- **Volumes**: 
  - `./frontend:/app` (code hot-reload)
  - `/app/node_modules` (anonymous volume)
  - `/app/.next` (anonymous volume)
- **Network**: `nist-network`
- **Depends On**: backend

## Key Features

### Development Features
- Hot-reload for both backend and frontend
- Shared Docker network for service communication
- Persistent database storage
- Health checks for service dependencies
- Development and production Dockerfiles

### Configuration Management
- Environment-based configuration
- Sensible defaults for development
- Secure defaults (change in production)
- Centralized environment variables

### Developer Experience
- Makefile for common commands
- Initialization scripts
- Health check scripts
- Comprehensive documentation
- Code quality tools configured

## File Naming Conventions

### Backend (Python)
- Modules: `lowercase_with_underscores.py`
- Classes: `PascalCase`
- Functions: `lowercase_with_underscores`
- Constants: `UPPERCASE_WITH_UNDERSCORES`

### Frontend (TypeScript)
- Components: `PascalCase.tsx`
- Utilities: `camelCase.ts`
- Types: `PascalCase` (in `lowercase.ts` files)
- Hooks: `useCamelCase.ts`
- Pages: `page.tsx` (Next.js convention)

## Import Conventions

### Backend
```python
# Standard library imports
import os
import sys

# Third-party imports
from fastapi import FastAPI, Depends
from sqlalchemy import Column, String

# Local imports
from app.config import settings
from app.models.user import User
```

### Frontend
```typescript
// React imports
import { useState, useEffect } from 'react';

// Next.js imports
import Link from 'next/link';
import Image from 'next/image';

// Third-party imports
import axios from 'axios';

// Local imports
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';
```

## Documentation

- **Root README.md** - Project overview, quick start, tech stack
- **SETUP.md** - Detailed setup instructions and troubleshooting
- **CONTRIBUTING.md** - Contribution guidelines and standards
- **docs/architecture.md** - System architecture and design decisions
- **docs/development.md** - Development workflow and best practices
- **backend/README.md** - Backend-specific documentation
- **frontend/README.md** - Frontend-specific documentation

## Testing Structure

### Backend Tests
```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_main.py            # Basic app tests
├── api/
│   ├── test_auth.py
│   ├── test_reports.py
│   └── test_users.py
├── services/
│   └── test_report_service.py
└── utils/
    └── test_security.py
```

### Frontend Tests (Future)
```
__tests__/
├── components/
│   ├── Button.test.tsx
│   └── ReportCard.test.tsx
├── hooks/
│   └── useAuth.test.ts
└── lib/
    └── api.test.ts
```

## Git Workflow

Branches:
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - Feature branches
- `fix/*` - Bug fix branches
- `hotfix/*` - Urgent production fixes

## Environment Variables

See `.env.example` for all available environment variables and their descriptions.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `NEXT_PUBLIC_API_URL` - Backend API URL (accessible in browser)
- `SECRET_KEY` - Application secret key
- `ALLOWED_ORIGINS` - CORS allowed origins
