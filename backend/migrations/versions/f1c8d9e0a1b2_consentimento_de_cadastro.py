"""Consentimento de cadastro

Revision ID: f1c8d9e0a1b2
Revises: e4843bb0189c
Create Date: 2026-06-21

"""
from alembic import op
import sqlalchemy as sa


revision = "f1c8d9e0a1b2"
down_revision = "e4843bb0189c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("login", sa.Column("consent_accepted_at", sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column("login", "consent_accepted_at")
