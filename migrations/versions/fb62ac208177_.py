"""empty message

Revision ID: fb62ac208177
Revises: 
Create Date: 2019-11-07 15:34:01.994384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb62ac208177'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Chaves',
    sa.Column('id', sa.String(length=44), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Company',
    sa.Column('id', sa.String(length=14), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('NumberDocument',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('month', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.Column('cnpj', sa.String(length=14), nullable=False),
    sa.ForeignKeyConstraint(['cnpj'], ['Company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('NumberDocument')
    op.drop_table('Company')
    op.drop_table('Chaves')
    # ### end Alembic commands ###
