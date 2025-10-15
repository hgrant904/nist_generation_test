# Quick Start Guide

This guide will help you get the NIST Automation system up and running quickly.

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip (Python package installer)

## Installation Steps

### 1. Set up Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -e .
```

### 3. Configure Database

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` to match your PostgreSQL configuration:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/nist_automation
ECHO_SQL=false
ENVIRONMENT=development
```

### 4. Create Database

```bash
# Using psql
createdb nist_automation

# Or using PostgreSQL client
psql -U postgres
CREATE DATABASE nist_automation;
\q
```

### 5. Run Database Migrations

```bash
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial schema with control families...
```

### 6. Load Seed Data

```bash
python -m src.nist_automation.seeds.seed_runner
```

Expected output:
```
======================================================================
NIST CSF Data Seeding Process
======================================================================

Seeding control families...
  Created family: GV - Govern
  Created family: ID - Identify
  ...
✓ Seeded 6 control families

Seeding controls...
  Created control: GV.OC-01 - Organizational Context
  ...
✓ Seeded 15 controls

Seeding implementation tiers...
  Created tier 1: Partial
  ...
✓ Seeded 4 implementation tiers

Seeding sample questions...
  Created question for GV.OC-01: Has your organization documented...
  ...
✓ Seeded 7 sample questions

======================================================================
✓ All seed data loaded successfully!
======================================================================
```

### 7. Run Example Script

```bash
python example_usage.py
```

This demonstrates basic usage of the system.

## Verify Installation

Check that tables were created:

```bash
psql -U postgres -d nist_automation -c "\dt"
```

Expected tables:
- assessments
- assessment_sessions
- control_families
- controls
- evidences
- implementation_tiers
- options
- questions
- responses

Check seed data was loaded:

```bash
psql -U postgres -d nist_automation -c "SELECT code, name FROM control_families;"
```

Expected output should show 6 control families (GV, ID, PR, DE, RS, RC).

## Basic Usage

### Python Script Example

```python
from src.nist_automation.database import SessionLocal
from src.nist_automation.services import CRUDService

# Create database session
db = SessionLocal()
service = CRUDService(db)

# Get all control families
families = service.get_control_families(framework="NIST_CSF")
for family in families:
    print(f"{family.code}: {family.name}")

# Get controls for a specific family
controls = service.get_controls(family_id=families[0].id)
for control in controls:
    print(f"{control.code}: {control.name}")

# Create an assessment
assessment = service.create_assessment(
    name="My First Assessment",
    framework="NIST_CSF",
    framework_version="2.0",
    organization_name="My Company",
    status="DRAFT"
)

# Close session
db.close()
```

## Common Commands

### Database Migrations

```bash
# Check current migration version
alembic current

# View migration history
alembic history

# Upgrade to latest
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Create new migration after model changes
alembic revision --autogenerate -m "Description"
```

### Seed Data

```bash
# Load initial seed data
python -m src.nist_automation.seeds.seed_runner

# To reload seeds (requires clean database)
alembic downgrade base
alembic upgrade head
python -m src.nist_automation.seeds.seed_runner
```

### Python Environment

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Deactivate
deactivate

# Update dependencies
pip install -e . --upgrade
```

## Troubleshooting

### PostgreSQL Connection Issues

**Error**: `connection to server at "localhost" (127.0.0.1), port 5432 failed`

**Solutions**:
1. Ensure PostgreSQL is running: `sudo service postgresql start`
2. Check connection parameters in `.env` file
3. Verify database exists: `psql -U postgres -l`

### Migration Issues

**Error**: `Target database is not up to date`

**Solution**:
```bash
alembic upgrade head
```

**Error**: `Can't locate revision identified by 'xxx'`

**Solution**:
```bash
alembic stamp head
alembic upgrade head
```

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
pip install -e .
```

### Seed Data Errors

**Error**: `IntegrityError: duplicate key value violates unique constraint`

**Solution**: Seeds have already been loaded. To reload:
```bash
psql -U postgres -d nist_automation -c "TRUNCATE TABLE control_families CASCADE;"
python -m src.nist_automation.seeds.seed_runner
```

## Next Steps

1. **Explore the Models**: Review `src/nist_automation/models/` to understand the data structure
2. **Read Full Documentation**: See [docs/DATA_LOADING.md](docs/DATA_LOADING.md) for comprehensive guide
3. **Extend Seed Data**: Add more controls in `src/nist_automation/seeds/nist_csf_data.py`
4. **Build API**: Create REST API endpoints using FastAPI or Flask
5. **Create UI**: Build frontend for assessment completion

## Resources

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Getting Help

1. Check [docs/DATA_LOADING.md](docs/DATA_LOADING.md) for detailed documentation
2. Review example code in `example_usage.py`
3. Inspect models in `src/nist_automation/models/`
4. Check Alembic migrations in `alembic/versions/`

---

**Note**: This system is designed for development. For production deployment, consider:
- Using environment-specific configuration
- Implementing proper authentication
- Setting up database backups
- Adding monitoring and logging
- Using connection pooling
- Implementing caching strategies
