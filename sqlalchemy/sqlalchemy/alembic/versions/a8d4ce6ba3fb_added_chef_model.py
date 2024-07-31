"""added chef model

Revision ID: a8d4ce6ba3fb
Revises: f625f9f69d4d
Create Date: 2024-07-19 16:30:03.918896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8d4ce6ba3fb'
down_revision: Union[str, None] = 'f625f9f69d4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chefs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.add_column('recipes', sa.Column('chef_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'recipes', ['id'])
    op.create_foreign_key(None, 'recipes', 'chefs', ['chef_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'recipes', type_='foreignkey')
    op.drop_constraint(None, 'recipes', type_='unique')
    op.drop_column('recipes', 'chef_id')
    op.drop_table('chefs')
    # ### end Alembic commands ###