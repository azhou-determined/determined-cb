from sqlalchemy import Column, String, DateTime, Enum, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from common import Status
from db import Base


class Job(Base):
    __tablename__ = "job"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(Enum(Status), nullable=False)
    branch = Column(String, nullable=False)
    user = Column(String, nullable=False)
    commit = Column(String, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Float(precision=3))
    circleci_url = Column(String)
    tests = relationship("Test", backref="job", lazy=True)


class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("job.id"))
    name = Column(String, nullable=False)
    classname = Column(String, nullable=False)
    status = Column(Enum(Status), nullable=False)
    duration = Column(Float(precision=3))
