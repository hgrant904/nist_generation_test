# Scripts

Utility scripts for the NIST Reports project.

## Available Scripts

### `init-project.sh`
Initializes the project for first-time setup.

**Usage:**
```bash
./scripts/init-project.sh
```

**What it does:**
- Checks for Docker and Docker Compose installation
- Creates `.env` file from `.env.example` if it doesn't exist
- Builds Docker images
- Starts all services
- Verifies that services are running

### `health-check.sh`
Checks the health of all running services.

**Usage:**
```bash
./scripts/health-check.sh
```

**What it checks:**
- Docker Compose services status
- Backend API health endpoint
- Frontend availability
- PostgreSQL database connection
- Displays container status

### `db-init.sql`
Example SQL script for database initialization.

**Usage:**
```bash
# Execute manually in PostgreSQL
docker-compose exec postgres psql -U nist_user -d nist_reports -f /path/to/db-init.sql

# Or copy into container first
docker cp scripts/db-init.sql nist-reports-postgres:/tmp/
docker-compose exec postgres psql -U nist_user -d nist_reports -f /tmp/db-init.sql
```

**What it contains:**
- Example table schemas
- Index creation statements
- Initial data (if needed)

## Adding New Scripts

When adding new scripts:

1. Create the script file in this directory
2. Make it executable: `chmod +x scripts/your-script.sh`
3. Add a shebang line: `#!/bin/bash`
4. Add error handling: `set -e`
5. Add helpful output messages
6. Document it in this README
7. Update the main README if it's a commonly used script

## Script Guidelines

- Use `set -e` to exit on errors
- Use clear, descriptive echo messages
- Check for prerequisites before running
- Provide helpful error messages
- Use `$()` for command substitution instead of backticks
- Quote variables to handle spaces: `"$var"`
- Use absolute paths when referencing files
- Test scripts in a clean environment

## Examples

### Creating a backup script

```bash
#!/bin/bash
set -e

echo "📦 Creating database backup..."

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

mkdir -p "$BACKUP_DIR"

docker-compose exec -T postgres pg_dump -U nist_user nist_reports > "$BACKUP_FILE"

echo "✅ Backup created: $BACKUP_FILE"
```

### Creating a cleanup script

```bash
#!/bin/bash
set -e

echo "🧹 Cleaning up development environment..."

# Stop containers
docker-compose down

# Remove Python cache
find backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find backend -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# Remove Node modules and cache
rm -rf frontend/node_modules frontend/.next 2>/dev/null || true

echo "✅ Cleanup complete!"
```
