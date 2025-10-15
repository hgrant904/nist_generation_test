# Database Schema Documentation

## Entity Relationship Overview

```
┌──────────────────┐
│ ControlFamily    │
│                  │
│ PK: id           │
│ UK: code         │
│ framework        │
│ version          │
└────────┬─────────┘
         │
         │ 1:N
         │
┌────────▼─────────┐      ┌─────────────────┐
│ Control          │      │ Implementation  │
│                  │      │ Tier            │
│ PK: id           │      │                 │
│ UK: code         │      │ PK: id          │
│ FK: family_id    │      │ UK: tier_level  │
│ FK: parent_id    │      │ framework       │
└────────┬─────────┘      └─────────────────┘
         │
         │ 1:N
         │
┌────────▼─────────┐
│ Question         │
│                  │
│ PK: id           │
│ FK: control_id   │
│ question_type    │
│ question_text    │
└────────┬─────────┘
         │
         │ 1:N
         │
┌────────▼─────────┐
│ Option           │
│                  │
│ PK: id           │
│ FK: question_id  │
│ option_text      │
│ score            │
└──────────────────┘


┌──────────────────┐
│ Assessment       │
│                  │
│ PK: id           │
│ name             │
│ framework        │
│ status           │
└────────┬─────────┘
         │
         ├──────────┐
         │          │
         │ 1:N      │ 1:N
         │          │
┌────────▼────────┐ │
│ Assessment      │ │
│ Session         │ │
│                 │ │
│ PK: id          │ │
│ FK: assess_id   │ │
│ session_token   │ │
└─────────────────┘ │
                    │
            ┌───────▼─────────┐
            │ Response        │
            │                 │
            │ PK: id          │
            │ FK: assess_id   │
            │ FK: question_id │
            │ FK: option_id   │
            │ text_response   │
            └────────┬────────┘
                     │
                     │ 1:N
                     │
            ┌────────▼────────┐
            │ Evidence        │
            │                 │
            │ PK: id          │
            │ FK: response_id │
            │ file_name       │
            │ file_path       │
            └─────────────────┘
```

## Tables

### control_families

Represents NIST framework categories (e.g., Govern, Identify, Protect).

| Column      | Type         | Constraints           | Description                    |
|-------------|--------------|----------------------|--------------------------------|
| id          | INTEGER      | PK, AUTO_INCREMENT   | Primary key                    |
| code        | VARCHAR(50)  | UNIQUE, NOT NULL     | Family code (e.g., "GV", "ID") |
| name        | VARCHAR(255) | NOT NULL             | Family name                    |
| description | TEXT         | NULL                 | Detailed description           |
| framework   | VARCHAR(50)  | NOT NULL, INDEXED    | Framework identifier           |
| version     | VARCHAR(50)  | NOT NULL             | Framework version              |
| is_active   | BOOLEAN      | NOT NULL, DEFAULT TRUE | Active status                |
| sort_order  | INTEGER      | NOT NULL, DEFAULT 0  | Display order                  |
| created_at  | DATETIME     | NOT NULL             | Creation timestamp             |
| updated_at  | DATETIME     | NOT NULL             | Last update timestamp          |

**Indices:**
- `ix_code` on `code`
- `ix_framework` on `framework`

**Relationships:**
- One-to-Many with `controls`

---

### controls

Individual security controls within control families.

| Column            | Type         | Constraints                | Description                     |
|-------------------|--------------|---------------------------|---------------------------------|
| id                | INTEGER      | PK, AUTO_INCREMENT        | Primary key                     |
| family_id         | INTEGER      | FK → control_families.id  | Parent family                   |
| code              | VARCHAR(50)  | UNIQUE, NOT NULL          | Control code (e.g., "GV.OC-01") |
| name              | VARCHAR(255) | NOT NULL                  | Control name                    |
| description       | TEXT         | NULL                      | Detailed description            |
| guidance          | TEXT         | NULL                      | Implementation guidance         |
| version           | VARCHAR(50)  | NOT NULL                  | Control version                 |
| parent_control_id | INTEGER      | FK → controls.id, NULL    | Parent control (hierarchical)   |
| is_active         | BOOLEAN      | NOT NULL, DEFAULT TRUE    | Active status                   |
| priority          | VARCHAR(20)  | NULL                      | Priority level                  |
| sort_order        | INTEGER      | NOT NULL, DEFAULT 0       | Display order                   |
| created_at        | DATETIME     | NOT NULL                  | Creation timestamp              |
| updated_at        | DATETIME     | NOT NULL                  | Last update timestamp           |

**Indices:**
- `ix_family_id` on `family_id`
- `ix_code` on `code`
- `ix_parent_control_id` on `parent_control_id`

**Relationships:**
- Many-to-One with `control_families`
- Self-referencing: Parent-Child relationship
- One-to-Many with `questions`

**Cascade Rules:**
- DELETE CASCADE from control_families
- DELETE SET NULL from parent_control

---

### implementation_tiers

NIST Cybersecurity Framework implementation maturity levels.

| Column          | Type         | Constraints           | Description                    |
|-----------------|--------------|----------------------|--------------------------------|
| id              | INTEGER      | PK, AUTO_INCREMENT   | Primary key                    |
| tier_level      | INTEGER      | UNIQUE, NOT NULL     | Tier number (1-4)              |
| name            | VARCHAR(100) | NOT NULL             | Tier name                      |
| description     | TEXT         | NULL                 | Tier description               |
| characteristics | TEXT         | NULL                 | Tier characteristics           |
| framework       | VARCHAR(50)  | NOT NULL, INDEXED    | Framework identifier           |
| version         | VARCHAR(50)  | NOT NULL             | Framework version              |
| is_active       | BOOLEAN      | NOT NULL, DEFAULT TRUE | Active status                |
| created_at      | DATETIME     | NOT NULL             | Creation timestamp             |
| updated_at      | DATETIME     | NOT NULL             | Last update timestamp          |

**Indices:**
- `ix_tier_level` on `tier_level`
- `ix_framework` on `framework`

---

### questions

Assessment questions linked to specific controls.

| Column        | Type             | Constraints           | Description                         |
|---------------|------------------|----------------------|-------------------------------------|
| id            | INTEGER          | PK, AUTO_INCREMENT   | Primary key                         |
| control_id    | INTEGER          | FK → controls.id     | Associated control                  |
| question_text | TEXT             | NOT NULL             | Question text                       |
| question_type | ENUM             | NOT NULL             | Question type (see below)           |
| help_text     | TEXT             | NULL                 | Helper text                         |
| is_required   | BOOLEAN          | NOT NULL, DEFAULT TRUE | Required flag                     |
| version       | VARCHAR(50)      | NOT NULL             | Question version                    |
| is_active     | BOOLEAN          | NOT NULL, DEFAULT TRUE | Active status                     |
| sort_order    | INTEGER          | NOT NULL, DEFAULT 0  | Display order                       |
| created_at    | DATETIME         | NOT NULL             | Creation timestamp                  |
| updated_at    | DATETIME         | NOT NULL             | Last update timestamp               |

**Question Types (ENUM):**
- `MULTIPLE_CHOICE`
- `TEXT`
- `RATING`
- `YES_NO`
- `FILE_UPLOAD`

**Indices:**
- `ix_control_id` on `control_id`

**Relationships:**
- Many-to-One with `controls`
- One-to-Many with `options`
- One-to-Many with `responses`

**Cascade Rules:**
- DELETE CASCADE from controls

---

### options

Response options for multiple choice and rating questions.

| Column       | Type          | Constraints           | Description               |
|--------------|---------------|-----------------------|---------------------------|
| id           | INTEGER       | PK, AUTO_INCREMENT    | Primary key               |
| question_id  | INTEGER       | FK → questions.id     | Associated question       |
| option_text  | TEXT          | NOT NULL              | Option text               |
| option_value | VARCHAR(255)  | NULL                  | Option value              |
| score        | NUMERIC(5,2)  | NULL                  | Score for this option     |
| is_active    | BOOLEAN       | NOT NULL, DEFAULT TRUE | Active status            |
| sort_order   | INTEGER       | NOT NULL, DEFAULT 0   | Display order             |
| created_at   | DATETIME      | NOT NULL              | Creation timestamp        |
| updated_at   | DATETIME      | NOT NULL              | Last update timestamp     |

**Indices:**
- `ix_question_id` on `question_id`

**Relationships:**
- Many-to-One with `questions`

**Cascade Rules:**
- DELETE CASCADE from questions

---

### assessments

Assessment instances with metadata.

| Column             | Type         | Constraints                | Description                |
|--------------------|--------------|---------------------------|----------------------------|
| id                 | INTEGER      | PK, AUTO_INCREMENT        | Primary key                |
| name               | VARCHAR(255) | NOT NULL                  | Assessment name            |
| description        | TEXT         | NULL                      | Assessment description     |
| framework          | VARCHAR(50)  | NOT NULL, INDEXED         | Framework identifier       |
| framework_version  | VARCHAR(50)  | NOT NULL                  | Framework version          |
| status             | ENUM         | NOT NULL, INDEXED         | Assessment status          |
| organization_name  | VARCHAR(255) | NULL                      | Organization name          |
| assessor_name      | VARCHAR(255) | NULL                      | Assessor name              |
| start_date         | DATETIME     | NULL                      | Assessment start date      |
| end_date           | DATETIME     | NULL                      | Assessment end date        |
| created_at         | DATETIME     | NOT NULL                  | Creation timestamp         |
| updated_at         | DATETIME     | NOT NULL                  | Last update timestamp      |

**Assessment Status (ENUM):**
- `DRAFT`
- `IN_PROGRESS`
- `UNDER_REVIEW`
- `COMPLETED`
- `ARCHIVED`

**Indices:**
- `ix_framework` on `framework`
- `ix_status` on `status`

**Relationships:**
- One-to-Many with `assessment_sessions`
- One-to-Many with `responses`

---

### assessment_sessions

Tracks user sessions conducting assessments.

| Column          | Type         | Constraints               | Description                |
|-----------------|--------------|--------------------------|----------------------------|
| id              | INTEGER      | PK, AUTO_INCREMENT       | Primary key                |
| assessment_id   | INTEGER      | FK → assessments.id      | Associated assessment      |
| session_token   | VARCHAR(255) | UNIQUE, NOT NULL         | Session token              |
| user_identifier | VARCHAR(255) | NULL, INDEXED            | User identifier            |
| ip_address      | VARCHAR(50)  | NULL                     | User IP address            |
| user_agent      | VARCHAR(500) | NULL                     | User agent string          |
| last_activity   | DATETIME     | NOT NULL                 | Last activity timestamp    |
| created_at      | DATETIME     | NOT NULL                 | Creation timestamp         |
| expires_at      | DATETIME     | NULL                     | Session expiration         |

**Indices:**
- `ix_assessment_id` on `assessment_id`
- `ix_session_token` on `session_token`
- `ix_user_identifier` on `user_identifier`

**Relationships:**
- Many-to-One with `assessments`

**Cascade Rules:**
- DELETE CASCADE from assessments

---

### responses

User responses to assessment questions.

| Column           | Type         | Constraints               | Description                |
|------------------|--------------|--------------------------|----------------------------|
| id               | INTEGER      | PK, AUTO_INCREMENT       | Primary key                |
| assessment_id    | INTEGER      | FK → assessments.id      | Associated assessment      |
| question_id      | INTEGER      | FK → questions.id        | Associated question        |
| option_id        | INTEGER      | FK → options.id, NULL    | Selected option            |
| text_response    | TEXT         | NULL                     | Text response              |
| numeric_response | INTEGER      | NULL                     | Numeric response           |
| version          | VARCHAR(50)  | NOT NULL                 | Response version           |
| response_metadata| TEXT         | NULL                     | Additional metadata (JSON) |
| created_at       | DATETIME     | NOT NULL                 | Creation timestamp         |
| updated_at       | DATETIME     | NOT NULL                 | Last update timestamp      |

**Indices:**
- `ix_assessment_id` on `assessment_id`
- `ix_question_id` on `question_id`
- `ix_option_id` on `option_id`

**Relationships:**
- Many-to-One with `assessments`
- Many-to-One with `questions`
- Many-to-One with `options`
- One-to-Many with `evidences`

**Cascade Rules:**
- DELETE CASCADE from assessments
- DELETE CASCADE from questions
- DELETE SET NULL from options

---

### evidences

Metadata for evidence files supporting responses.

| Column           | Type          | Constraints              | Description                |
|------------------|---------------|--------------------------|----------------------------|
| id               | INTEGER       | PK, AUTO_INCREMENT       | Primary key                |
| response_id      | INTEGER       | FK → responses.id        | Associated response        |
| file_name        | VARCHAR(255)  | NOT NULL                 | Original file name         |
| file_path        | VARCHAR(1000) | NULL                     | Storage file path          |
| file_size        | BIGINT        | NULL                     | File size in bytes         |
| file_type        | VARCHAR(100)  | NULL                     | File type/extension        |
| mime_type        | VARCHAR(100)  | NULL                     | MIME type                  |
| checksum         | VARCHAR(255)  | NULL                     | File checksum (SHA-256)    |
| storage_location | VARCHAR(500)  | NULL                     | Storage location (S3, etc) |
| description      | TEXT          | NULL                     | Evidence description       |
| uploaded_by      | VARCHAR(255)  | NULL                     | Uploader identifier        |
| created_at       | DATETIME      | NOT NULL                 | Creation timestamp         |
| updated_at       | DATETIME      | NOT NULL                 | Last update timestamp      |

**Indices:**
- `ix_response_id` on `response_id`

**Relationships:**
- Many-to-One with `responses`

**Cascade Rules:**
- DELETE CASCADE from responses

---

## Design Patterns

### Versioning

The schema supports multiple framework versions simultaneously:

- `version` field on control families, controls, questions tracks framework version
- `framework` field allows multiple frameworks (NIST_CSF, NIST_800_53, etc.)
- Responses track `version` to maintain historical consistency

### Soft Deletes

Most entities have `is_active` boolean for soft deletion:

- Controls, questions, options, tiers, families can be deactivated
- Historical data remains intact for reporting
- Queries should filter by `is_active=True` for current data

### Hierarchical Data

Controls support parent-child relationships via `parent_control_id`:

- Enables modeling of control enhancements (e.g., AC-1(1), AC-1(2))
- Self-referencing foreign key with SET NULL on delete
- Can represent unlimited depth hierarchy

### Audit Trail

All entities include timestamps:

- `created_at`: When entity was created (immutable)
- `updated_at`: When entity was last modified (auto-updated)
- Enables change tracking and audit logs

### Flexible Responses

Responses support multiple answer types:

- `option_id`: For multiple choice and rating questions
- `text_response`: For text answers
- `numeric_response`: For numeric ratings
- `response_metadata`: JSON field for complex data

## Query Patterns

### Get all controls for a framework version

```sql
SELECT c.* FROM controls c
JOIN control_families cf ON c.family_id = cf.id
WHERE cf.framework = 'NIST_CSF' AND cf.version = '2.0'
AND c.is_active = TRUE
ORDER BY cf.sort_order, c.sort_order;
```

### Get assessment progress

```sql
SELECT 
    a.id,
    a.name,
    COUNT(DISTINCT q.id) as total_questions,
    COUNT(DISTINCT r.id) as answered_questions,
    ROUND(COUNT(DISTINCT r.id) * 100.0 / COUNT(DISTINCT q.id), 2) as completion_pct
FROM assessments a
JOIN responses r ON a.id = r.assessment_id
JOIN questions q ON q.control_id IN (
    SELECT id FROM controls WHERE family_id IN (
        SELECT id FROM control_families WHERE framework = a.framework
    )
)
WHERE a.id = 1
GROUP BY a.id, a.name;
```

### Get control with questions and options

```sql
SELECT 
    c.code,
    c.name,
    q.id as question_id,
    q.question_text,
    q.question_type,
    o.id as option_id,
    o.option_text,
    o.score
FROM controls c
LEFT JOIN questions q ON c.id = q.control_id
LEFT JOIN options o ON q.id = o.question_id
WHERE c.code = 'GV.OC-01'
AND c.is_active = TRUE
AND q.is_active = TRUE
ORDER BY q.sort_order, o.sort_order;
```

## Performance Considerations

### Indexed Columns

All foreign keys have indices for join performance:
- `family_id`, `control_id`, `question_id`, `assessment_id`, `response_id`

Frequently filtered columns are indexed:
- Framework identifiers (`framework`)
- Status fields (`status`, `is_active`)
- Unique identifiers (`code`, `session_token`)

### Query Optimization Tips

1. **Use appropriate indices**: Already defined for common queries
2. **Limit result sets**: Use pagination (OFFSET/LIMIT)
3. **Eager loading**: Use JOINs to avoid N+1 queries
4. **Materialized views**: Consider for complex analytics
5. **Partitioning**: Consider for large assessment tables

## Migration Strategy

### Adding New Fields

```python
# In Alembic migration
op.add_column('controls', 
    sa.Column('maturity_level', sa.Integer(), nullable=True)
)
```

### Modifying Enums

```python
# Create new enum type
op.execute("ALTER TYPE question_type_enum ADD VALUE 'CHECKLIST'")
```

### Data Migrations

```python
# Update existing data
op.execute("""
    UPDATE controls 
    SET priority = 'high' 
    WHERE code LIKE 'GV%'
""")
```

## Future Enhancements

1. **Audit Tables**: Track all changes with before/after values
2. **Control Mappings**: Many-to-many relationships between frameworks
3. **Scoring Engine**: Calculated maturity scores
4. **Workflow States**: More granular assessment workflow
5. **User Management**: User accounts and permissions
6. **Organizations**: Multi-tenant support
7. **Tags/Categories**: Flexible categorization
8. **Attachments**: Binary file storage
9. **Comments**: Discussion threads on responses
10. **Notifications**: Event-driven notifications
