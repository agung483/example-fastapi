"""create vote table

Revision ID: eb015e529e9a
Revises: 53a0ab27b160
Create Date: 2023-04-07 20:37:00.741503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb015e529e9a'
down_revision = '53a0ab27b160'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('votes', 
                    sa.Column('post_id', sa.Integer, nullable=False), 
                    sa.Column('user_id', sa.Integer, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('post_id', 'user_id')
                    )
    pass


def downgrade() -> None:
    op.drop_table('votes')
    pass
