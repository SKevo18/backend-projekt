"""update_users_table

Revision ID: b77a60239c60
Revises: 09e04de84e98
Create Date: 2025-03-17 00:45:48.346059

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'b77a60239c60'
down_revision = '09e04de84e98'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Použije sa pri `alembic upgrade ...`."""
    pass


def downgrade() -> None:
    """Použije sa pri `alembic downgrade ...`."""
    pass
