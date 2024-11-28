"""Adiciona campo menuTemplate à tabela menus

Revision ID: 77e8f28fcfab
Revises: 78e7b7a4e55f
Create Date: 2024-11-28 12:47:17.851679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77e8f28fcfab'
down_revision = '78e7b7a4e55f'
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona a nova coluna menuTemplate, inicialmente como nullable
    with op.batch_alter_table('menus', schema=None) as batch_op:
        batch_op.add_column(sa.Column('menuTemplate', sa.String(length=50), nullable=True))

    # Atualiza os registros existentes com valores únicos para menuTemplate
    connection = op.get_bind()
    result = connection.execute("SELECT menuId FROM menus")
    rows = result.fetchall()
    for index, row in enumerate(rows, start=1):
        connection.execute(
            f"UPDATE menus SET menuTemplate = 'home{index}' WHERE menuId = {row['menuId']}"
        )

    # Torna a coluna não nula e adiciona a restrição de unicidade
    with op.batch_alter_table('menus', schema=None) as batch_op:
        batch_op.alter_column('menuTemplate', nullable=False)
        batch_op.create_unique_constraint('uq_menuTemplate', ['menuTemplate'])


def downgrade():
    with op.batch_alter_table('menus', schema=None) as batch_op:
        batch_op.drop_constraint('uq_menuTemplate', type_='unique')
        batch_op.drop_column('menuTemplate')

