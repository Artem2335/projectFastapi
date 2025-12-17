"""Initial database schema

Revision ID: 001
Revises: 
Create Date: 2025-12-17

Creates:
- users table
- movies table  
- reviews table
- ratings table
- favorites table
"""
from alembic import op
import sqlalchemy as sa


revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema"""
    
    # Enable PRAGMA foreign_keys for SQLite
    op.execute('PRAGMA foreign_keys=ON')
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('is_user', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('is_moderator', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_users_email', 'users', ['email'])
    
    # Create movies table
    op.create_table(
        'movies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('genre', sa.String(length=100), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('poster_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    
    # Create reviews table
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('movie_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('approved', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )
    
    # Create ratings table
    op.create_table(
        'ratings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('movie_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )
    
    # Create favorites table
    op.create_table(
        'favorites',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('movie_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )


def downgrade() -> None:
    """Drop all tables"""
    op.drop_table('favorites')
    op.drop_table('ratings')
    op.drop_table('reviews')
    op.drop_table('movies')
    op.drop_table('users')
    
    # Disable PRAGMA foreign_keys
    op.execute('PRAGMA foreign_keys=OFF')
