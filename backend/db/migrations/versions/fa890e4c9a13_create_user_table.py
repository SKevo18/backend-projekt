"""create_user_table

Revision ID: fa890e4c9a13
Revises:
Create Date: 2025-03-10 18:40:17.415515

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "fa890e4c9a13"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Použije sa pri `alembic upgrade ...`."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=35), nullable=False),
        sa.Column("last_name", sa.String(length=35), nullable=False),
        sa.Column("user_email", sa.String(length=64), nullable=False),
        sa.Column("user_password", sa.String(length=60), nullable=False),
        sa.Column("registered_at", sa.DateTime(), nullable=False),
        sa.Column("role", sa.Integer(), nullable=False, default=0),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_user_email"), "users", ["user_email"], unique=False)


def downgrade():
    """Použije sa pri `alembic downgrade ...`."""

    op.drop_index(op.f("ix_users_user_email"), table_name="users")
    op.drop_table("users")
