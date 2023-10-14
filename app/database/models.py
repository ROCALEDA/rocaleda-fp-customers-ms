from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from database import Base

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer(10), primary_key=True)
    userId = Column(Integer(12))
    name = Column(String(100))
    # nit = Column(String, nullable=True)
    # address = Column(String(400), nullable=True)
    # country = Column(String(50), nullable=True)
    # field = Column(String(30), nullable=True)

    projects = relationship("Project", back_populates="customer")

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer(10), primary_key=True, autoincrement=True)
    customerId = Column(Integer, ForeignKey("customer.id"))
    name = Column(String(100))

    customer = relationship("Customer", back_populates="projects")

    performance_evaluations = relationship("PerformanceEvaluation",
                                            back_populates="project")
    open_positions = relationship("OpenPosition", back_populates="project")

class PerformanceEvaluation(Base):
    __tablename__ = "performance_evaluation"

    dateTime = Column(DateTime, primary_key=True)
    projectId = Column(Integer, ForeignKey("project.id"), primary_key=True)
    name = Column(String(80))
    candidateId = Column(Integer)
    score = Column(Integer(3))
    observations = Column(String(255), nullable=True)

    project = relationship("Project", back_populates="performance_evaluations")

class OpenPosition(Base):
    __tablename__ = "open_position"

    id = Column(Integer(10), primary_key=True, autoincrement=True)
    projectId = Column(Integer, ForeignKey("project.id"))
    isOpen = Column(Boolean)
    positionName = Column(String(80))
    payrate = Column(Numeric(12, 2))

    project = relationship("Project", back_populates="open_positions")

    position_candidates = relationship("PositionCandidate",
                                        back_populates="open_position")
    position_technologies = relationship(
        "Technology", secondary="position_details", back_populates="open_positions"
    )

class PositionCandidate(Base):
    __tablename__ = "position_candidate"

    openPositionId = Column(Integer, ForeignKey("open_position.id"), primary_key=True)
    candidateId = Column(Integer, primary_key=True)
    # generalScore = Column(Integer(3), nullable=True)
    # technicalScore = Column(Integer(3), nullable=True)
    # softSkillScore = Column(Integer(3), nullable=True)

    open_position = relationship("OpenPosition", back_populates="position_candidates")

class PositionDetail(Base):
    __tablename__ = "position_details"

    openPositionId = Column(Integer, ForeignKey("open_position.id"), primary_key=True)
    technologyId = Column(Integer, ForeignKey("technology.id"), primary_key=True)
    # technologyYears = Column(Integer(10))
    # seniority = Column(String(20))

class Technology(Base):
    __tablename__ = "technology"

    id = Column(Integer(10), primary_key=True, autoincrement=True)
    name = Column(String(30))

    open_positions = relationship(
        "OpenPosition", secondary="position_details",
        back_populates="position_technologies"
    )
