"""start of courses

Revision ID: 3245e4b276f3
Revises: 22c5f76074f1
Create Date: 2013-09-10 14:11:54.382801

"""

# revision identifiers, used by Alembic.
revision = '3245e4b276f3'
down_revision = '22c5f76074f1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('terms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('current', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=16), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('term_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('archived', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['term_id'], ['terms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'users', sa.Column('is_admin', sa.Boolean(), nullable=True))


    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'users', 'is_admin')
    op.drop_table('courses')
    op.drop_table('terms')
    ### end Alembic commands ###
