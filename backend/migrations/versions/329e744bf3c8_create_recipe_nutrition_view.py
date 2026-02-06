"""create recipe_nutrition_view

Revision ID: 329e744bf3c8
Revises: a73f2c060218
Create Date: 2026-02-06 11:56:04.231868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '329e744bf3c8'
down_revision: Union[str, Sequence[str], None] = 'a73f2c060218'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE VIEW recipe_nutrition_view AS
        SELECT 
            r.name AS recipe_name,
            SUM(m.quantity * n.kcal) AS total_kcal,
            SUM(m.quantity * n.proteines) AS total_protein
        FROM recipes r
        JOIN mise_en_place m ON r.name = m.recipe_name
        JOIN ingredients i ON m.ingredient_name = i.name
        JOIN nutrients n ON i.group = n.ingredient_group
        GROUP BY r.name
    """)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
