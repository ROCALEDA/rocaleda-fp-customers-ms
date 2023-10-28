from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from .database import Base


class Customer(Base):
    __tablename__ = "customer"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    # nit = Column(String(15), nullable=True)
    # address = Column(String(255), nullable=True)
    # country = Column(String(50), nullable=True)
    # field = Column(String(30), nullable=True)

    # children relationships
    projects = relationship("Project", back_populates="customer")


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.user_id"))
    name = Column(String(100))
    description = Column(String(255))
    is_team_complete = Column(Boolean, default=False)

    # parents relationships
    customer = relationship("Customer", back_populates="projects")

    # children relationships
    open_positions = relationship("OpenPosition", back_populates="project")
    employees = relationship("Employee", back_populates="project")
    # performance_evaluations = relationship(
    #     "PerformanceEvaluation", back_populates="project"
    # )


# class PerformanceEvaluation(Base):
#    __tablename__ = "performance_evaluation"

#    scheduled = Column(DateTime, primary_key=True)
#    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)
#    name = Column(String(80))
#    candidate_id = Column(Integer)
#    score = Column(Integer)
#    observations = Column(String(255), nullable=True)

# parents relationships
# project = relationship("Project", back_populates="performance_evaluations")


class Employee(Base):
    __tablename__ = "employee"

    # id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)
    full_name = Column(String(100), primary_key=True)
    profile_name = Column(String(30))

    # parents relationships
    project = relationship("Project", back_populates="employees")


class OpenPosition(Base):
    __tablename__ = "open_position"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("project.id"))
    is_open = Column(Boolean, default=True)
    position_name = Column(String(80))
    candidate_id = Column(Integer, nullable=True)
    # payrate = Column(Numeric(12, 2), nullable=True)

    # parents relationships
    project = relationship("Project", back_populates="open_positions")

    # children relationships
    soft_skills = relationship(
        "SoftSkill", secondary="position_soft_skill", back_populates="open_positions"
    )
    technologies = relationship(
        "Technology", secondary="position_technology", back_populates="open_positions"
    )
    # position_candidates = relationship(
    #     "PositionCandidate", back_populates="open_position"
    # )


class PositionSoftSkill(Base):
    __tablename__ = "position_soft_skill"

    open_position_id = Column(Integer, ForeignKey("open_position.id"), primary_key=True)
    soft_skill_id = Column(Integer, ForeignKey("soft_skill.id"), primary_key=True)


class SoftSkill(Base):
    __tablename__ = "soft_skill"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(255))

    open_positions = relationship(
        "OpenPosition", secondary="position_soft_skill", back_populates="soft_skills"
    )


class PositionTechnology(Base):
    __tablename__ = "position_technology"

    open_position_id = Column(Integer, ForeignKey("open_position.id"), primary_key=True)
    technology_id = Column(Integer, ForeignKey("technology.id"), primary_key=True)
    # technology_years = Column(Integer(10))
    # seniority = Column(String(20))


class Technology(Base):
    __tablename__ = "technology"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))

    # relationships
    open_positions = relationship(
        "OpenPosition",
        secondary="position_technology",
        back_populates="technologies",
    )


# class PositionCandidate(Base):
#     __tablename__ = "position_candidate"

#    open_position_id = Column(Integer, ForeignKey("open_position.id"), primary_key=True)
#    candidate_id = Column(Integer, primary_key=True)
#    general_score = Column(Integer(3), nullable=True)
#    technical_score = Column(Integer(3), nullable=True)
#    softskill_score = Column(Integer(3), nullable=True)

# parents relationships
# open_position = relationship("OpenPosition", back_populates="position_candidates")
