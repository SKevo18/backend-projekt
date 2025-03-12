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
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("registered_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=False)


def downgrade():
    """Použije sa pri `alembic downgrade ...`."""

    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
