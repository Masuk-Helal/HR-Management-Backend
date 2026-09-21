from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
# from sqlalchemy.orm import relationship
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    hash_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)  # librarian or member


class Jobs(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    department = Column(String)
    location = Column(String)
    job_type = Column(String)  # full-time, part-time, contract, internship
    experience_level = Column(String)  # entry, mid, senior
    salary = Column(Integer, nullable=True)
    vacancies = Column(Integer, default=1)
    skills_required = Column(Text, nullable=True)
    qualifications = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    application_deadline = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    posted_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)


class JobApplications(Base):
    __tablename__ = 'job_applications'

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    applied_date = Column(DateTime, default=datetime.now)
    status = Column(String, default='pending')
