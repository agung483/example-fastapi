"""add user table

Revision ID: 5620c7cc6db9
Revises: d87c01f187e1
Create Date: 2023-04-07 19:09:37.680969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5620c7cc6db9'
down_revision = '352d03a2d47b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer, nullable=False), 
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('email', sa.String, nullable=True), 
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username', 'email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
