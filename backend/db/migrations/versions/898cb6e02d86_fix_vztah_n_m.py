"""fix_vztah_N:M

Revision ID: 898cb6e02d86
Revises: 09efd8fa57fa
Create Date: 2025-04-02 20:55:50.671980

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '898cb6e02d86'
down_revision = '09efd8fa57fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Použije sa pri `alembic upgrade ...`."""
    pass


def downgrade() -> None:
    """Použije sa pri `alembic downgrade ...`."""
    pass
