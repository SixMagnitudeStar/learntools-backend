"""Add style column to ArticleBlock

Revision ID: 0c9953efb090
Revises: 2bb782999f4c
Create Date: 2025-11-10 10:18:09.937962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = '0c9953efb090'
down_revision: Union[str, Sequence[str], None] = '2bb782999f4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 新增 style 欄位
    op.add_column('article_block', sa.Column('style', sa.String(length=50), nullable=True))

def downgrade():
    # 移除 style 欄位
    op.drop_column('article_block', 'style')