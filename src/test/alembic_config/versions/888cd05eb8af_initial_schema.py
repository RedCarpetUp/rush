"""initial schema

Revision ID: 888cd05eb8af
Revises:
Create Date: 2019-01-19 14:07:18.828333

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '888cd05eb8af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('parent_task_id', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(op.f('ux_user_email'), 'users', ['email'])
    ### end Alembic commands ###


def downgrade():
    op.drop_constraint('ux_user_email', 'user')
