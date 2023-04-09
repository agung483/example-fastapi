"""create posts table

Revision ID: 352d03a2d47b
Revises: 
Create Date: 2023-04-07 15:05:03.058624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '352d03a2d47b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True), 
                    sa.Column('title', sa.String, nullable=False),sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
