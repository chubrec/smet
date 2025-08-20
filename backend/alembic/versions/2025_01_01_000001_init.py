from alembic import op
import sqlalchemy as sa


revision = '000001_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'work_categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'works',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('base_rate', sa.Numeric(12, 2), nullable=False),
        sa.Column('min_rate', sa.Numeric(12, 2), nullable=True),
        sa.Column('max_rate', sa.Numeric(12, 2), nullable=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('work_categories.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'materials',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('price', sa.Numeric(12, 2), nullable=False),
        sa.Column('vendor', sa.String(length=100), nullable=True),
        sa.Column('sku', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('client_name', sa.String(length=150), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'estimates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('discount_percent', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('surcharge_percent', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'estimate_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('estimate_id', sa.Integer(), sa.ForeignKey('estimates.id'), nullable=False),
        sa.Column('work_id', sa.Integer(), sa.ForeignKey('works.id'), nullable=True),
        sa.Column('material_id', sa.Integer(), sa.ForeignKey('materials.id'), nullable=True),
        sa.Column('quantity', sa.Numeric(12, 2), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('unit_price', sa.Numeric(12, 2), nullable=False),
        sa.Column('title_override', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('estimate_items')
    op.drop_table('estimates')
    op.drop_table('projects')
    op.drop_table('materials')
    op.drop_table('works')
    op.drop_table('work_categories')

