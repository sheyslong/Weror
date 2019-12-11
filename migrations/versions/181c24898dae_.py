"""empty message

Revision ID: 181c24898dae
Revises: 895d6f15db60
Create Date: 2019-12-09 16:06:21.423094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '181c24898dae'
down_revision = '895d6f15db60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Keys',
    sa.Column('id', sa.String(length=45), nullable=False),
    sa.Column('state', sa.String(length=2), nullable=False),
    sa.Column('year', sa.String(length=2), nullable=False),
    sa.Column('month', sa.String(length=2), nullable=False),
    sa.Column('model', sa.String(length=2), nullable=False),
    sa.Column('serie', sa.String(length=2), nullable=False),
    sa.Column('issue', sa.String(length=1), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.Column('numberDocument_id', sa.String(length=9), nullable=False),
    sa.ForeignKeyConstraint(['numberDocument_id'], ['NumberDocument.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Keys')
    # ### end Alembic commands ###