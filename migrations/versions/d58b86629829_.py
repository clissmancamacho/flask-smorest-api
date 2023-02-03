"""empty message

Revision ID: d58b86629829
Revises: 36d470473237
Create Date: 2023-02-03 11:46:45.907275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd58b86629829'
down_revision = '36d470473237'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_parents')
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    op.create_table('roles_parents',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('parent_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['role.id'], name='roles_parents_parent_id_fkey'),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name='roles_parents_role_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='roles_parents_pkey')
    )
    # ### end Alembic commands ###
