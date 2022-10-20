"""empty message

Revision ID: acfb1d8fed59
Revises: 2f46b32d4ab6
Create Date: 2022-10-20 16:35:34.276371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acfb1d8fed59'
down_revision = '2f46b32d4ab6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tag', sa.Column('transaction_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tag', 'transaction', ['transaction_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tag', type_='foreignkey')
    op.drop_column('tag', 'transaction_id')
    # ### end Alembic commands ###
