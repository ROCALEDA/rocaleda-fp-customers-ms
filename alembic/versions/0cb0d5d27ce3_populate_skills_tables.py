"""Populate skills tables

Revision ID: 0cb0d5d27ce3
Revises: fb3813299277
Create Date: 2023-10-20 14:43:31.361481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cb0d5d27ce3'
down_revision: Union[str, None] = 'fb3813299277'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

soft_skill_table = sa.table(
    "soft_skill",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String),
    sa.Column("description", sa.String),
)

soft_skill_data = [
    {
        "id": 1,
        "name": "Leadership",
        "description": "The ability to guide, inspire, and influence a group towards achieving a common goal. Leaders are often looked up to as role models and are responsible for steering a team in the right direction.",
    },
    {
        "id": 2,
        "name": "Responsibility",
        "description": "Taking ownership of one's actions and their outcomes. It involves being accountable for what you do, ensuring that tasks are completed, and taking corrective actions when necessary.",
    },
    {
        "id": 3,
        "name": "Ownership",
        "description": "A commitment to seeing a project or task through to its completion. It's about taking full responsibility and pride in the work you do, regardless of whether it's individually or as part of a team.",
    },
    {
        "id": 4,
        "name": "Communication",
        "description": "The ability to convey ideas, feelings, and information clearly and effectively. Good communication is two-sided: it involves both expressing oneself and listening to others.",
    },
    {
        "id": 5,
        "name": "Teamwork",
        "description": "Working collaboratively with others to achieve shared goals. It involves understanding group dynamics, respecting diverse viewpoints, and playing to the strengths of each team member.",
    },
    {
        "id": 6,
        "name": "Adaptability",
        "description": "Being open to change and having the flexibility to adjust to shifting priorities or circumstances. In a fast-paced environment, adaptability is key to addressing challenges and seizing new opportunities.",
    },
    {
        "id": 7,
        "name": "Empathy",
        "description": "Understanding and sharing the feelings of another. It's about being sensitive to the experiences of others and showing genuine care and concern.",
    },
    {
        "id": 8,
        "name": "Management",
        "description": "The act of overseeing people or projects to achieve desired outcomes. Good management involves planning, decision-making, and ensuring resources are used efficiently and effectively.",
    },
]


technologies_table = sa.table(
    "technology",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String),
)

tech_skill_data = [
    {"id": 1, "name": "Frontend"},
    {"id": 2, "name": "Backend"},
    {"id": 3, "name": "ReactJS"},
    {"id": 4, "name": "NodeJS"},
    {"id": 5, "name": "NextJS"},
    {"id": 6, "name": "Python"},
    {"id": 7, "name": "Flask"},
    {"id": 8, "name": "AWS"},
    {"id": 9, "name": "Architecture"},
    {"id": 10, "name": "NestJS"},
    {"id": 11, "name": "Angular"},
    {"id": 12, "name": "GCP"},
    {"id": 13, "name": "Azure"},
    {"id": 14, "name": "DevOps"},
    {"id": 15, "name": "Java"},
    {"id": 16, "name": "SpringBoot"},
    {"id": 17, "name": "FastAPI"},
    {"id": 18, "name": "Data Science"},
    {"id": 19, "name": "SQL"},
    {"id": 20, "name": "NoSQL"},
    {"id": 21, "name": "MongoDB"},
    {"id": 22, "name": "Redis"},
    {"id": 23, "name": "CSS"},
    {"id": 24, "name": "Typescript"},
]

def upgrade() -> None:
    op.bulk_insert(soft_skill_table, soft_skill_data)
    op.bulk_insert(technologies_table, tech_skill_data)
    pass


def downgrade() -> None:
    op.execute(
        soft_skill_table.delete().where(
            soft_skill_table.c.id.in_([skill["id"] for skill in soft_skill_data])
        )
    )
    op.execute(
        technologies_table.delete().where(
            technologies_table.c.id.in_([skill["id"] for skill in tech_skill_data])
        )
    )
    pass
