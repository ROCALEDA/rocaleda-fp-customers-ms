from typing import List, TYPE_CHECKING

from app.database.schemas import (
    CustomerBase,
    ProjectCreation,
    ProjectCreationResponse,
    ProjectDetailResponse,
)

if TYPE_CHECKING:
    from app.customer.repositories.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self, customer_repository: "CustomerRepository"):
        self.customer_repository = customer_repository

    async def create_customer(self, new_customer: CustomerBase) -> None:
        new_customer_dict = {"user_id": new_customer.user_id, "name": new_customer.name}

        await self.customer_repository.create_customer(new_customer_dict)

    async def create_project(
        self, customer_id: int, project_data: ProjectCreation
    ) -> ProjectCreationResponse:
        new_project = {
            "customer_id": customer_id,
            "name": project_data.name,
            "description": project_data.description,
        }
        project_item = await self.customer_repository.create_project(new_project)
        for employee in project_data.employees:
            new_employee = {
                "project_id": project_item.id,
                "full_name": employee.full_name,
                "profile_name": employee.profile_name,
            }
            await self.customer_repository.create_employee(new_employee)
        for profile in project_data.profiles:
            soft_skill_rows = [
                await self.customer_repository.get_soft_skill_by_name(skill)
                for skill in profile.soft_skills
            ]

            tech_skills_rows = [
                await self.customer_repository.get_tech_skill_by_name(skill)
                for skill in profile.tech_skills
            ]

            new_open_position = {
                "project_id": project_item.id,
                "position_name": profile.name,
                "soft_skills": soft_skill_rows,
                "technologies": tech_skills_rows,
            }

            for _ in range(profile.amount):
                await self.customer_repository.create_open_position(new_open_position)
        return ProjectCreationResponse.model_validate(
            {
                "id": project_item.id,
                "name": project_item.name,
                "description": project_item.description,
            }
        )

    async def get_customer_projects(
        self, customer_id: int
    ) -> List[ProjectDetailResponse]:
        customer_projects = await self.customer_repository.get_projects(customer_id)
        projects_output = []
        for project in customer_projects:
            positions = []
            for open_position in project.open_positions:
                positions.append(
                    {
                        "id": open_position.id,
                        "is_open": open_position.is_open,
                        "name": open_position.position_name,
                    }
                )
            projects_output.append(
                {
                    "id": project.id,
                    "name": project.name,
                    "is_team_complete": project.is_team_complete,
                    "total_positions": len(project.open_positions),
                    "positions": positions,
                }
            )
        return projects_output
