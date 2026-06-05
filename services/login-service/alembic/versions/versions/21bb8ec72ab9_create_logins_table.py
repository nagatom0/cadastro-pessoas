"""create logins table

Revision ID: 21bb8ec72ab9
Revises: 
Create Date: 2026-06-01 17:54:07.798700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '21bb8ec72ab9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('logins',
    sa.Column('login', sa.String(length=7), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('login')
    )
def downgrade() -> None:
    op.drop_table('logins')
