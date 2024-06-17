"""Initial migration

Revision ID: a3024f0fc362
Revises: 
Create Date: 2024-06-17 06:43:17.273773

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a3024f0fc362'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('covers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=255), nullable=False),
    sa.Column('mime_type', sa.String(length=255), nullable=False),
    sa.Column('md5_hash', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Добавьте роли
    op.execute("INSERT INTO roles (id, name, description) VALUES (1, 'Администратор', 'Суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг')")
    op.execute("INSERT INTO roles (id, name, description) VALUES (2, 'Модератор', 'Может редактировать данные книг и производить модерацию рецензий')")
    op.execute("INSERT INTO roles (id, name, description) VALUES (3, 'Пользователь', 'Может оставлять рецензии')")
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('publisher', sa.String(length=255), nullable=False),
    sa.Column('author', sa.String(length=255), nullable=False),
    sa.Column('pages', sa.Integer(), nullable=False),
    sa.Column('cover_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cover_id'], ['covers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('middle_name', sa.String(length=255), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('book_genre',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('book_id', 'genre_id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('review_text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('username')

    op.drop_table('user')
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.drop_index('name')

    op.drop_table('role')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('description', mysql.VARCHAR(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.create_index('name', ['name'], unique=True)

    op.create_table('user',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('password_hash', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('first_name', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('last_name', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('role_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name='user_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('username', ['username'], unique=True)

    op.drop_table('reviews')
    op.drop_table('book_genre')
    op.drop_table('users')
    op.drop_table('books')
    op.drop_table('roles')
    op.drop_table('genres')
    op.drop_table('covers')
    # ### end Alembic commands ###