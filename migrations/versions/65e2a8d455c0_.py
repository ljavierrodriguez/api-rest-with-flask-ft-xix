"""empty message

Revision ID: 65e2a8d455c0
Revises: d8d772eb526f
Create Date: 2023-03-31 18:19:38.626272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65e2a8d455c0'
down_revision = 'd8d772eb526f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.drop_constraint('profiles_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['users_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('profiles_ibfk_1', 'users', ['users_id'], ['id'])

    # ### end Alembic commands ###
