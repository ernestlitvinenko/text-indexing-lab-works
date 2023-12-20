"""empty message

Revision ID: 43f1e2772d07
Revises: 
Create Date: 2023-12-19 13:37:27.033174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43f1e2772d07'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('request',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('request', sa.Text(), nullable=False),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('synonym',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('core_word', sa.Text(), nullable=False),
    sa.Column('synonym', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('synonym')
    op.drop_table('request')
    # ### end Alembic commands ###
