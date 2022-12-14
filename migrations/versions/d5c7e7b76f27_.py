"""empty message

Revision ID: d5c7e7b76f27
Revises: 90591ca198e9
Create Date: 2022-08-04 18:37:30.907461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5c7e7b76f27'
down_revision = '90591ca198e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pokemon', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'pokemon', 'user', ['user_id'], ['id'])
    op.drop_constraint('user_pokemon_id_fkey', 'user', type_='foreignkey')
    op.drop_column('user', 'pokemon_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('pokemon_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_pokemon_id_fkey', 'user', 'pokemon', ['pokemon_id'], ['id'])
    op.drop_constraint(None, 'pokemon', type_='foreignkey')
    op.drop_column('pokemon', 'user_id')
    # ### end Alembic commands ###
