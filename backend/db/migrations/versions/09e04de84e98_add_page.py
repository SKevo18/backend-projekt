"""add_page

Revision ID: 09e04de84e98
Revises: 56fa62a328fa
"""

import sqlalchemy as sa
from alembic import op

revision = "09e04de84e98"
down_revision = "56fa62a328fa"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('pages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('html_content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('pages')
