"""create table

Revision ID: b525eaf3b71e
Revises:
Create Date: 2018-06-24 19:30:05.749338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b525eaf3b71e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('birthday', sa.Date),
        sa.Column('phone', sa.Text),
        sa.Column('email', sa.Text)
    )

    op.create_table(
        'schedule',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', onupdate='RESTRICT', ondelete='SET NULL')),
        sa.Column('time_start', sa.Time),
        sa.Column('time_end', sa.Time),
        sa.Column('str_type', sa.Enum('start', 'end', 'eat', 'rest', name='schedule_type_enum'))
    )

def downgrade():
    op.drop_table('users')
    op.drop_table('schedule')
