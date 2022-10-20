"""empty message

Revision ID: f763b820ec85
Revises: 4e9f33f6846f
Create Date: 2022-10-20 16:20:26.968327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f763b820ec85'
down_revision = '4e9f33f6846f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction', 'name')
    # ### end Alembic commands ###
