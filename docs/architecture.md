# System Architecture

## Overview

The NIST Reports platform follows a modern three-tier architecture with clear separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    (Next.js / React)                         │
│                  Port: 3000 (HTTP)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ REST API (HTTP/HTTPS)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                       Backend API                            │
│                      (FastAPI)                              │
│                  Port: 8000 (HTTP)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ SQLAlchemy ORM
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      PostgreSQL                              │
│                  Port: 5432 (TCP)                           │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Frontend Layer
- **Technology**: Next.js 14 with App Router
- **Language**: TypeScript
- **Responsibilities**:
  - User interface rendering
  - Client-side state management
  - API communication
  - Form validation
  - Report visualization

### Backend Layer
- **Technology**: FastAPI
- **Language**: Python 3.11+
- **Responsibilities**:
  - RESTful API endpoints
  - Business logic processing
  - Data validation (Pydantic)
  - NIST API integration
  - Report generation
  - Authentication & authorization
  - Database operations

### Data Layer
- **Technology**: PostgreSQL 16
- **ORM**: SQLAlchemy
- **Responsibilities**:
  - Data persistence
  - Relational data management
  - Transaction management
  - Query optimization

## Communication Flow

1. User interacts with the frontend (Next.js)
2. Frontend sends HTTP requests to the backend API
3. Backend validates requests and processes business logic
4. Backend queries/updates the database via SQLAlchemy ORM
5. Backend returns JSON responses to the frontend
6. Frontend renders the data to the user

## Design Decisions

### Why FastAPI?
- High performance (async/await support)
- Automatic API documentation (OpenAPI/Swagger)
- Built-in data validation with Pydantic
- Excellent developer experience

### Why Next.js?
- Server-side rendering capabilities
- Built-in routing and API routes
- Excellent TypeScript support
- Strong ecosystem and community

### Why PostgreSQL?
- Robust ACID compliance
- Excellent performance for relational data
- Strong community support
- Rich feature set (JSON support, full-text search, etc.)

## Scalability Considerations

- **Horizontal Scaling**: Both frontend and backend can be scaled horizontally
- **Database**: PostgreSQL supports read replicas and connection pooling
- **Caching**: Redis can be added for session management and caching
- **Load Balancing**: Nginx or similar can be used for load balancing

## Security Considerations

- HTTPS for all external communication
- JWT-based authentication
- CORS configuration
- Input validation and sanitization
- SQL injection prevention via ORM
- Environment-based configuration
