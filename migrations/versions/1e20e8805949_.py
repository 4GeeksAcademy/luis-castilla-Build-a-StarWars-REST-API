"""empty message

Revision ID: 1e20e8805949
Revises: 
Create Date: 2024-09-18 19:08:30.266300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e20e8805949'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('personajes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('especie', sa.String(length=50), nullable=True),
    sa.Column('altura', sa.Float(), nullable=True),
    sa.Column('peso', sa.Float(), nullable=True),
    sa.Column('pelicula_origen', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planetas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('climate', sa.String(length=50), nullable=True),
    sa.Column('population', sa.String(length=50), nullable=True),
    sa.Column('diametro', sa.Float(), nullable=True),
    sa.Column('gravedad', sa.String(length=50), nullable=True),
    sa.Column('terreno', sa.String(length=50), nullable=True),
    sa.Column('pelicula_origen', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('firstname', sa.String(length=20), nullable=False),
    sa.Column('lastname', sa.String(length=250), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('vehiculos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('modelo', sa.String(length=50), nullable=True),
    sa.Column('fabricante', sa.String(length=50), nullable=True),
    sa.Column('longitud', sa.Float(), nullable=True),
    sa.Column('velocidad_maxima', sa.Float(), nullable=True),
    sa.Column('capacidad_pasajeros', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favoritos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('personaje_id', sa.Integer(), nullable=True),
    sa.Column('planeta_id', sa.Integer(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('vehiculo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['personaje_id'], ['personajes.id'], ),
    sa.ForeignKeyConstraint(['planeta_id'], ['planetas.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.ForeignKeyConstraint(['vehiculo_id'], ['vehiculos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favoritos')
    op.drop_table('vehiculos')
    op.drop_table('usuario')
    op.drop_table('user')
    op.drop_table('planetas')
    op.drop_table('personajes')
    # ### end Alembic commands ###