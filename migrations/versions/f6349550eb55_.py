"""empty message

Revision ID: f6349550eb55
Revises: ab95e831b33f
Create Date: 2023-02-03 09:58:01.591309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6349550eb55'
down_revision = 'ab95e831b33f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    # ### end Alembic commands ###