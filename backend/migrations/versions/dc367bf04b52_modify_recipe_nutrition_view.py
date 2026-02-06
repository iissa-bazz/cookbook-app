"""modify recipe_nutrition_view

Revision ID: dc367bf04b52
Revises: 329e744bf3c8
Create Date: 2026-02-06 12:56:26.093217

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc367bf04b52'
down_revision: Union[str, Sequence[str], None] = '329e744bf3c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        DROP VIEW IF EXISTS recipe_nutrition_view;
        CREATE VIEW recipe_nutrition_view AS
        SELECT 
            r.name AS recipe_name,
            SUM(m.quantity * n.kcal) AS total_kcal,
            SUM(m.quantity * n.proteines) AS total_protein,
            SUM(m.quantity * n.graisses) AS total_fat,
            SUM(m.quantity * n.glucides) AS total_carbs,
            SUM(m.quantity * n.sucres) AS total_sugar,
            SUM(m.quantity * n.fibres_alimentaires) AS total_fiber
        FROM recipes r
        JOIN mise_en_place m ON r.name = m.recipe_name
        JOIN ingredients i ON m.ingredient_name = i.name
        JOIN nutrients n ON i.group = n.ingredient_group
        GROUP BY r.name
    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
