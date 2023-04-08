"""add foreign-key to posts table

Revision ID: 53a0ab27b160
Revises: 5620c7cc6db9
Create Date: 2023-04-07 19:39:06.834719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53a0ab27b160'
down_revision = '5620c7cc6db9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean() , nullable=False, server_default="TRUE"))
    op.add_column('posts', sa.Column('owner_id',sa.Integer(), nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default = sa.text('now()'), nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts',referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'owner_id')
    op.drop_column('posts', 'created_at')
    pass
