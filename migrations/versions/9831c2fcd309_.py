"""empty message

Revision ID: 9831c2fcd309
Revises: d1221668f339
Create Date: 2018-04-11 15:47:56.811607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9831c2fcd309'
down_revision = 'd1221668f339'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('checkout',
    sa.Column('checkout_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('subtotal', sa.Float(), nullable=True),
    sa.Column('product_id', sa.String(length=80), nullable=True),
    sa.Column('date', sa.String(length=80), nullable=True),
    sa.Column('total', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('checkout_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('checkout')
    # ### end Alembic commands ###
