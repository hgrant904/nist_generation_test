"""Initial schema with control families, controls, questions, assessments, and responses

Revision ID: 001
Revises: 
Create Date: 2024-10-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'control_families',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('framework', sa.String(length=50), nullable=False),
        sa.Column('version', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_control_families')),
        sa.UniqueConstraint('code', name=op.f('uq_control_families_code'))
    )
    op.create_index(op.f('ix_code'), 'control_families', ['code'], unique=False)
    op.create_index(op.f('ix_framework'), 'control_families', ['framework'], unique=False)

    op.create_table(
        'implementation_tiers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tier_level', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('characteristics', sa.Text(), nullable=True),
        sa.Column('framework', sa.String(length=50), nullable=False),
        sa.Column('version', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_implementation_tiers')),
        sa.UniqueConstraint('tier_level', name=op.f('uq_implementation_tiers_tier_level'))
    )
    op.create_index(op.f('ix_tier_level'), 'implementation_tiers', ['tier_level'], unique=False)
    op.create_index(op.f('ix_framework'), 'implementation_tiers', ['framework'], unique=False)

    op.create_table(
        'assessments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('framework', sa.String(length=50), nullable=False),
        sa.Column('framework_version', sa.String(length=50), nullable=False),
        sa.Column('status', sa.Enum('DRAFT', 'IN_PROGRESS', 'UNDER_REVIEW', 'COMPLETED', 'ARCHIVED', name='assessment_status_enum'), nullable=False),
        sa.Column('organization_name', sa.String(length=255), nullable=True),
        sa.Column('assessor_name', sa.String(length=255), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_assessments'))
    )
    op.create_index(op.f('ix_framework'), 'assessments', ['framework'], unique=False)
    op.create_index(op.f('ix_status'), 'assessments', ['status'], unique=False)

    op.create_table(
        'controls',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('family_id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('guidance', sa.Text(), nullable=True),
        sa.Column('version', sa.String(length=50), nullable=False),
        sa.Column('parent_control_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('priority', sa.String(length=20), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['family_id'], ['control_families.id'], name=op.f('fk_controls_family_id_control_families'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_control_id'], ['controls.id'], name=op.f('fk_controls_parent_control_id_controls'), ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_controls')),
        sa.UniqueConstraint('code', name=op.f('uq_controls_code'))
    )
    op.create_index(op.f('ix_family_id'), 'controls', ['family_id'], unique=False)
    op.create_index(op.f('ix_code'), 'controls', ['code'], unique=False)
    op.create_index(op.f('ix_parent_control_id'), 'controls', ['parent_control_id'], unique=False)

    op.create_table(
        'assessment_sessions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('assessment_id', sa.Integer(), nullable=False),
        sa.Column('session_token', sa.String(length=255), nullable=False),
        sa.Column('user_identifier', sa.String(length=255), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('last_activity', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['assessment_id'], ['assessments.id'], name=op.f('fk_assessment_sessions_assessment_id_assessments'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_assessment_sessions')),
        sa.UniqueConstraint('session_token', name=op.f('uq_assessment_sessions_session_token'))
    )
    op.create_index(op.f('ix_assessment_id'), 'assessment_sessions', ['assessment_id'], unique=False)
    op.create_index(op.f('ix_session_token'), 'assessment_sessions', ['session_token'], unique=False)
    op.create_index(op.f('ix_user_identifier'), 'assessment_sessions', ['user_identifier'], unique=False)

    op.create_table(
        'questions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('control_id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('question_type', sa.Enum('MULTIPLE_CHOICE', 'TEXT', 'RATING', 'YES_NO', 'FILE_UPLOAD', name='question_type_enum'), nullable=False),
        sa.Column('help_text', sa.Text(), nullable=True),
        sa.Column('is_required', sa.Boolean(), nullable=False),
        sa.Column('version', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['control_id'], ['controls.id'], name=op.f('fk_questions_control_id_controls'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_questions'))
    )
    op.create_index(op.f('ix_control_id'), 'questions', ['control_id'], unique=False)

    op.create_table(
        'options',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('option_text', sa.Text(), nullable=False),
        sa.Column('option_value', sa.String(length=255), nullable=True),
        sa.Column('score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], name=op.f('fk_options_question_id_questions'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_options'))
    )
    op.create_index(op.f('ix_question_id'), 'options', ['question_id'], unique=False)

    op.create_table(
        'responses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('assessment_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('option_id', sa.Integer(), nullable=True),
        sa.Column('text_response', sa.Text(), nullable=True),
        sa.Column('numeric_response', sa.Integer(), nullable=True),
        sa.Column('version', sa.String(length=50), nullable=False),
        sa.Column('response_metadata', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['assessment_id'], ['assessments.id'], name=op.f('fk_responses_assessment_id_assessments'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], name=op.f('fk_responses_question_id_questions'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['option_id'], ['options.id'], name=op.f('fk_responses_option_id_options'), ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_responses'))
    )
    op.create_index(op.f('ix_assessment_id'), 'responses', ['assessment_id'], unique=False)
    op.create_index(op.f('ix_question_id'), 'responses', ['question_id'], unique=False)
    op.create_index(op.f('ix_option_id'), 'responses', ['option_id'], unique=False)

    op.create_table(
        'evidences',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('response_id', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=1000), nullable=True),
        sa.Column('file_size', sa.BigInteger(), nullable=True),
        sa.Column('file_type', sa.String(length=100), nullable=True),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('checksum', sa.String(length=255), nullable=True),
        sa.Column('storage_location', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('uploaded_by', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['response_id'], ['responses.id'], name=op.f('fk_evidences_response_id_responses'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_evidences'))
    )
    op.create_index(op.f('ix_response_id'), 'evidences', ['response_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_response_id'), table_name='evidences')
    op.drop_table('evidences')
    op.drop_index(op.f('ix_option_id'), table_name='responses')
    op.drop_index(op.f('ix_question_id'), table_name='responses')
    op.drop_index(op.f('ix_assessment_id'), table_name='responses')
    op.drop_table('responses')
    op.drop_index(op.f('ix_question_id'), table_name='options')
    op.drop_table('options')
    op.drop_index(op.f('ix_control_id'), table_name='questions')
    op.drop_table('questions')
    op.drop_index(op.f('ix_user_identifier'), table_name='assessment_sessions')
    op.drop_index(op.f('ix_session_token'), table_name='assessment_sessions')
    op.drop_index(op.f('ix_assessment_id'), table_name='assessment_sessions')
    op.drop_table('assessment_sessions')
    op.drop_index(op.f('ix_parent_control_id'), table_name='controls')
    op.drop_index(op.f('ix_code'), table_name='controls')
    op.drop_index(op.f('ix_family_id'), table_name='controls')
    op.drop_table('controls')
    op.drop_index(op.f('ix_status'), table_name='assessments')
    op.drop_index(op.f('ix_framework'), table_name='assessments')
    op.drop_table('assessments')
    op.drop_index(op.f('ix_framework'), table_name='implementation_tiers')
    op.drop_index(op.f('ix_tier_level'), table_name='implementation_tiers')
    op.drop_table('implementation_tiers')
    op.drop_index(op.f('ix_framework'), table_name='control_families')
    op.drop_index(op.f('ix_code'), table_name='control_families')
    op.drop_table('control_families')
    op.execute('DROP TYPE IF EXISTS question_type_enum')
    op.execute('DROP TYPE IF EXISTS assessment_status_enum')
