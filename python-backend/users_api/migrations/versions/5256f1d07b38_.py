"""empty message

Revision ID: 5256f1d07b38
Revises: 092220883c75, 12e9a26e335b, c30f65880a6b
Create Date: 2024-02-06 10:10:04.342855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5256f1d07b38'
down_revision: Union[str, None] = ('092220883c75', '12e9a26e335b', 'c30f65880a6b')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
