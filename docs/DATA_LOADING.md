# Data Loading Workflow

This document describes the data loading workflow for the NIST Security Report Automation system.

## Overview

The system uses a structured approach to load NIST Cybersecurity Framework (CSF) taxonomy and questionnaire data into the database. The workflow consists of:

1. Database schema creation via Alembic migrations
2. Seed data loading for control families, controls, and implementation tiers
3. Sample questionnaire generation

## Database Schema

### Core Entities

The database schema supports the following core entities:

#### Control Families (Table: `control_families`)
- Represents high-level categories from NIST CSF 2.0: Govern (GV), Identify (ID), Protect (PR), Detect (DE), Respond (RS), Recover (RC)
- Fields: code, name, description, framework, version, is_active, sort_order
- Supports versioning and branching through version field

#### Controls (Table: `controls`)
- Individual security controls within families (e.g., GV.OC-01, ID.AM-01)
- Fields: family_id, code, name, description, guidance, version, parent_control_id, priority
- Hierarchical structure via self-referencing parent_control_id
- Links to control families via family_id foreign key

#### Implementation Tiers (Table: `implementation_tiers`)
- NIST CSF maturity levels (Tier 1-4: Partial, Risk Informed, Repeatable, Adaptive)
- Fields: tier_level, name, description, characteristics, framework, version

#### Questions (Table: `questions`)
- Assessment questions linked to specific controls
- Fields: control_id, question_text, question_type, help_text, is_required, version
- Question types: MULTIPLE_CHOICE, TEXT, RATING, YES_NO, FILE_UPLOAD

#### Options (Table: `options`)
- Response options for multiple choice and rating questions
- Fields: question_id, option_text, option_value, score, sort_order

#### Assessments (Table: `assessments`)
- Assessment instances with metadata
- Fields: name, description, framework, framework_version, status, organization_name, assessor_name, dates
- Status workflow: DRAFT → IN_PROGRESS → UNDER_REVIEW → COMPLETED → ARCHIVED

#### Assessment Sessions (Table: `assessment_sessions`)
- Tracks user sessions conducting assessments
- Fields: assessment_id, session_token, user_identifier, ip_address, user_agent, timestamps

#### Responses (Table: `responses`)
- User responses to assessment questions
- Fields: assessment_id, question_id, option_id, text_response, numeric_response, version
- Supports multiple response types (text, numeric, option-based)

#### Evidence (Table: `evidences`)
- Metadata for evidence files supporting responses
- Fields: response_id, file_name, file_path, file_size, file_type, mime_type, checksum, storage_location

### Indices and Constraints

The schema includes the following performance optimizations:

**Unique Constraints:**
- `control_families.code` - Ensures unique control family identifiers
- `controls.code` - Ensures unique control identifiers
- `implementation_tiers.tier_level` - Ensures unique tier levels
- `assessment_sessions.session_token` - Ensures unique session tokens

**Foreign Key Constraints with Cascade:**
- Controls cascade delete from families
- Questions cascade delete from controls
- Options cascade delete from questions
- Responses cascade delete from assessments and questions
- Evidence cascade delete from responses
- Assessment sessions cascade delete from assessments

**Indices:**
- Framework and version fields for filtering by framework
- Status fields for assessment workflow queries
- Foreign key columns for join performance
- Session tokens and user identifiers for session management

## Migration Management

### Initial Migration

The initial migration (`001_initial_schema.py`) creates all tables with proper indices and constraints.

```bash
# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check current version
alembic current

# View migration history
alembic history
```

### Creating New Migrations

When modifying models:

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Review generated migration file in alembic/versions/
# Edit if necessary to add custom logic

# Apply migration
alembic upgrade head
```

### Branching and Versioning

The schema supports multiple framework versions simultaneously:

- `version` field on control families, controls, questions tracks framework version
- `framework` field allows multiple frameworks (NIST_CSF, NIST_800_53, etc.)
- Queries can filter by framework and version for version-specific assessments
- Old versions remain in database for historical assessments

## Seed Data Loading

### Architecture

The seeding system uses:

1. **Data Files** (`nist_csf_data.py`): Static data definitions for NIST CSF 2.0
2. **Seed Runner** (`seed_runner.py`): Orchestrates loading process
3. **Service Layer** (`crud_service.py`): Business logic for CRUD operations
4. **Repository Layer** (`base.py`): Generic data access patterns

### Running Seeds

```bash
# Ensure database is created and migrations are run
alembic upgrade head

# Run seed data loading
python -m src.nist_automation.seeds.seed_runner

# Or use Python:
from src.nist_automation.seeds import run_seeds
run_seeds()
```

### Seed Data Content

**Control Families (6 families):**
- GV (Govern), ID (Identify), PR (Protect), DE (Detect), RS (Respond), RC (Recover)

**Controls (15 representative controls):**
- Sampling from each family covering key security domains
- Examples: Asset management, risk assessment, access control, monitoring, incident response

**Implementation Tiers (4 tiers):**
- Tier 1: Partial (ad hoc risk management)
- Tier 2: Risk Informed (management-approved practices)
- Tier 3: Repeatable (formalized policies)
- Tier 4: Adaptive (continuous improvement)

**Sample Questions (7 questions):**
- Various question types demonstrating all supported formats
- Linked to specific controls for realistic assessment workflow

### Seed Loading Process

The `SeedRunner` class orchestrates loading in dependency order:

```
1. Control Families (no dependencies)
   └─> Stores family_id mapping by code

2. Controls (depends on families)
   └─> Uses family_id from mapping
   └─> Stores control_id mapping by code

3. Implementation Tiers (no dependencies)
   └─> Loads tier definitions

4. Questions (depends on controls)
   └─> Uses control_id from mapping
   └─> Creates linked options for multiple choice questions
```

### Extending Seed Data

To add more controls or questions:

1. Edit `src/nist_automation/seeds/nist_csf_data.py`
2. Add entries to `NIST_CSF_CONTROLS` or `SAMPLE_QUESTIONS` lists
3. Ensure `family_code` or `control_code` references exist
4. Run seed script again (duplicate prevention via unique constraints)

For complete NIST 800-53 taxonomy:

1. Create new file `nist_800_53_data.py` with full control catalog
2. Update `seed_runner.py` to import and load 800-53 data
3. Set `framework="NIST_800_53"` and appropriate version

## CRUD Operations

### Service Layer Usage

```python
from src.nist_automation.database import SessionLocal
from src.nist_automation.services import CRUDService

# Create service with database session
db = SessionLocal()
service = CRUDService(db)

# Create entities
family = service.create_control_family(
    code="GV",
    name="Govern",
    framework="NIST_CSF",
    version="2.0",
    is_active=True,
    sort_order=1
)

control = service.create_control(
    family_id=family.id,
    code="GV.OC-01",
    name="Organizational Context",
    version="2.0",
    is_active=True,
    sort_order=1
)

# Read entities
families = service.get_control_families(framework="NIST_CSF")
control = service.get_control(control.id)
controls = service.get_controls(family_id=family.id)

# Update entities
updated_control = service.update_control(
    control.id,
    description="Updated description",
    is_active=False
)

# Delete entities
service.delete_control(control.id)

# Assessment workflow
assessment = service.create_assessment(
    name="Q4 2024 Security Assessment",
    framework="NIST_CSF",
    framework_version="2.0",
    status="DRAFT",
    organization_name="Acme Corp"
)

response = service.create_response(
    assessment_id=assessment.id,
    question_id=question.id,
    option_id=option.id,
    version="1.0"
)

evidence = service.create_evidence(
    response_id=response.id,
    file_name="incident_response_plan.pdf",
    file_size=1024000,
    mime_type="application/pdf"
)

db.close()
```

### Repository Layer

For advanced queries, use the repository layer directly:

```python
from src.nist_automation.repositories import BaseRepository
from src.nist_automation.models import Control

db = SessionLocal()
control_repo = BaseRepository(Control, db)

# Bulk operations
controls_data = [{"code": f"CTRL-{i}", ...} for i in range(100)]
controls = control_repo.bulk_create(controls_data)

# Filtering
high_priority = control_repo.get_by_filters(
    {"priority": "high", "is_active": True},
    skip=0,
    limit=50
)

# Count
total = control_repo.count({"framework": "NIST_CSF"})

db.close()
```

## Data Validation

### Model-Level Validation

SQLAlchemy models enforce:
- Required fields via `nullable=False`
- Data types via column type definitions
- Referential integrity via foreign key constraints
- Unique constraints on codes and identifiers

### Application-Level Validation

Additional validation should be implemented:
- Business rules (e.g., status transitions)
- Complex constraints (e.g., response must match question type)
- File upload validation (size, type, malware scanning)

## Performance Considerations

### Query Optimization

- Use appropriate indices (already defined in migration)
- Eager load relationships when needed: `joinedload()`, `selectinload()`
- Use pagination for large result sets (`skip` and `limit` parameters)
- Consider read replicas for reporting queries

### Bulk Operations

For loading large datasets:

```python
# Use bulk_create instead of individual creates
control_repo.bulk_create(large_control_list)

# Disable autoflush for better performance
with db.no_autoflush:
    for item in large_dataset:
        db.add(Model(**item))
    db.commit()
```

### Caching

Consider caching for:
- Control taxonomy (rarely changes)
- Implementation tiers (static data)
- Active framework versions

## Backup and Recovery

### Database Backup

```bash
# PostgreSQL backup
pg_dump -U postgres nist_automation > backup.sql

# Restore
psql -U postgres nist_automation < backup.sql
```

### Seed Data Re-seeding

Seeds are idempotent for initial load but may create duplicates on re-run due to timestamps. For clean re-seed:

```bash
# Drop and recreate database
alembic downgrade base
alembic upgrade head
python -m src.nist_automation.seeds.seed_runner
```

## Troubleshooting

### Common Issues

**Migration conflicts:**
```bash
# Resolve by checking current state
alembic current
alembic history

# Manually resolve conflicts in versions/
# Then upgrade
alembic upgrade head
```

**Foreign key violations:**
- Ensure parent entities exist before creating children
- Check cascade rules match intended behavior
- Use transactions to maintain consistency

**Duplicate entries:**
- Unique constraints prevent duplicates
- Handle `IntegrityError` exceptions in application code
- Use upsert patterns for idempotent operations

## Future Enhancements

1. **Full NIST 800-53 Import**: Load complete control catalog with relationships
2. **Control Mappings**: Map between frameworks (CSF ↔ 800-53 ↔ ISO 27001)
3. **Version Migration**: Tools to migrate assessments between framework versions
4. **Audit Trail**: Track all changes to control data and assessments
5. **Import/Export**: Load controls from OSCAL format, export to various formats
6. **Data Validation Rules**: Complex validation engine for response data
7. **Calculated Fields**: Auto-compute maturity scores, compliance percentages
8. **Archival Strategy**: Archive old assessments, maintain history

## References

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
