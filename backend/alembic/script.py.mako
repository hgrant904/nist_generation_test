# -*- coding: utf-8 -*-
"""Generic Alembic revision script."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
