"""initial migration

Revision ID: d3e8e225591f
Revises:
Create Date: 2020-12-07 13:37:53.356949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d3e8e225591f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "dungeon",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=True),
        sa.Column("rooms", sa.Integer(), nullable=True),
        sa.Column("treasures", sa.Integer(), nullable=True),
        sa.Column("traps", sa.Integer(), nullable=True),
        sa.Column("boss_level", sa.Boolean(), nullable=True),
        sa.Column("xp_drop", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "monster",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=True),
        sa.Column("race", sa.String(length=80), nullable=True),
        sa.Column("health_points", sa.Integer(), nullable=True),
        sa.Column("armor_points", sa.Integer(), nullable=True),
        sa.Column("attack_damage", sa.Integer(), nullable=True),
        sa.Column("xp_drop", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "monsters",
        sa.Column("monster_id", sa.Integer(), nullable=False),
        sa.Column("dungeon_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dungeon_id"],
            ["dungeon.id"],
        ),
        sa.ForeignKeyConstraint(
            ["monster_id"],
            ["monster.id"],
        ),
        sa.PrimaryKeyConstraint("monster_id", "dungeon_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("monsters")
    op.drop_table("monster")
    op.drop_table("dungeon")
    # ### end Alembic commands ###