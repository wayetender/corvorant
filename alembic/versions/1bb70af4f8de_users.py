"""users

Revision ID: 1bb70af4f8de
Revises: None
Create Date: 2013-09-10 09:04:36.801363

"""

# revision identifiers, used by Alembic.
revision = '1bb70af4f8de'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=129), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    op.drop_table('users')
    ### end Alembic commands ###
