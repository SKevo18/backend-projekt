"""seed_admin

Revision ID: 56fa62a328fa
Revises: fa890e4c9a13
Create Date: 2025-03-10 18:43:15.087475

"""

import sqlalchemy as sa
from alembic import op

from db.orm import User
from utils.password import hash_password

# revision identifiers, used by Alembic.
revision = "56fa62a328fa"
down_revision = "fa890e4c9a13"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Použije sa pri `alembic upgrade ...`."""

    op.execute(
        sa.insert(User).values(
            first_name="admin",
            last_name="admin",
            user_email="admin@nieco.sk",
            user_password=hash_password("12345678"),
            role=2,
        )
    )


def downgrade() -> None:
    """Použije sa pri `alembic downgrade ...`."""

    op.execute(sa.delete(User).where(User.user_email == "admin@nieco.sk"))
