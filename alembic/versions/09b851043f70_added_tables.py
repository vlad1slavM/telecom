"""Added tables

Revision ID: 09b851043f70
Revises: 
Create Date: 2023-05-23 22:49:09.876169

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '09b851043f70'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('equipment_type',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('type_name', sa.String(length=255), nullable=True),
    sa.Column('mask', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('equipment',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('code_equipment_type', mysql.INTEGER(display_width=11), nullable=True),
    sa.Column('serial_number', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['code_equipment_type'], ['equipment_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('serial_number')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('equipment')
    op.drop_table('equipment_type')
    # ### end Alembic commands ###