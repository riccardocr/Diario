"""Creazione Tabelle Post User Diario

Revision ID: 87c55413054c
Revises: 
Create Date: 2022-02-08 13:45:15.478541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87c55413054c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=12), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('diario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.Date(), nullable=True),
    sa.Column('anno', sa.String(length=4), nullable=True),
    sa.Column('mese', sa.String(length=2), nullable=True),
    sa.Column('va_pensieri', sa.Integer(), nullable=True),
    sa.Column('va_parole', sa.Integer(), nullable=True),
    sa.Column('va_atti', sa.Integer(), nullable=True),
    sa.Column('s_ipocrisia', sa.Integer(), nullable=True),
    sa.Column('s_menzogne', sa.Integer(), nullable=True),
    sa.Column('s_guadagni_illeciti', sa.Integer(), nullable=True),
    sa.Column('c_pensieri', sa.Integer(), nullable=True),
    sa.Column('c_parole', sa.Integer(), nullable=True),
    sa.Column('c_atti', sa.Integer(), nullable=True),
    sa.Column('u_vanità_di_conoscenza', sa.Integer(), nullable=True),
    sa.Column('u_orgoglio_di_possesso', sa.Integer(), nullable=True),
    sa.Column('u_abuso_di_potere', sa.Integer(), nullable=True),
    sa.Column('d_cibi_errati', sa.Integer(), nullable=True),
    sa.Column('d_alcool', sa.Integer(), nullable=True),
    sa.Column('d_droghe', sa.Integer(), nullable=True),
    sa.Column('Totale', sa.Integer(), nullable=True),
    sa.Column('Luce_interiore', sa.Time(), nullable=True),
    sa.Column('Suono_interiore', sa.Time(), nullable=True),
    sa.Column('fisico_e_morale', sa.Integer(), nullable=True),
    sa.Column('finanziario', sa.Integer(), nullable=True),
    sa.Column('Esperienze_di_visione_interiore', sa.Text(), nullable=True),
    sa.Column('Esperienze_di_ascolto_interiore', sa.Text(), nullable=True),
    sa.Column('Grado_di_superamento_della_coscienza_fisica', sa.Text(), nullable=True),
    sa.Column('Difficoltà_nella_meditazione', sa.Text(), nullable=True),
    sa.Column('Settori_da_migliorare', sa.Text(), nullable=True),
    sa.Column('Salvato_SN', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('slug', sa.String(length=250), nullable=True),
    sa.Column('description', sa.String(length=240), nullable=True),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('image', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('diario')
    op.drop_table('user')
    # ### end Alembic commands ###
