"""create products table

Revision ID: 20260803_0001
Revises:
Create Date: 2026-08-03 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "20260803_0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.String(length=128), nullable=False),
        sa.Column("supplier", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("price", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="USD"),
        sa.Column("image_url", sa.Text()),
        sa.Column("product_url", sa.Text()),
        sa.Column("stock", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("supplier", "external_id", name="uq_products_supplier_external_id"),
    )
    op.create_index("ix_products_id", "products", ["id"])
    op.create_index("ix_products_supplier", "products", ["supplier"])
    op.create_index("ix_products_title", "products", ["title"])

def downgrade():
    op.drop_index("ix_products_title", table_name="products")
    op.drop_index("ix_products_supplier", table_name="products")
    op.drop_index("ix_products_id", table_name="products")
    op.drop_table("products")
