"""Adiciona campo menuOrdem

Revision ID: 78e7b7a4e55f
Revises: 4cc0c9859f7f
Create Date: 2024-11-28 10:04:29.997752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78e7b7a4e55f'
down_revision = '4cc0c9859f7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menus', schema=None) as batch_op:
        batch_op.add_column(sa.Column('menuOrdem', sa.Integer(), nullable=False, server_default="0"))

    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menus', schema=None) as batch_op:
        batch_op.drop_column('menuOrdem')

    # ### end Alembic commands ###