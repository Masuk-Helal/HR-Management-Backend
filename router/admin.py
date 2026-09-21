

from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from typing import Annotated, Optional
from database import SessionLocal
from models import  Users, Jobs, JobApplications
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from router.auth import get_current_user

router = APIRouter()


class JobCreate(BaseModel):
    title : str
    description : str = Field(default='', max_length=200)
    department : str
    location : str
    job_type : str
    experience_level : str
    salary : Optional[float] = None
    vacancies : int = Field(default=1)
    skills_required : Optional[str] = None
    qualifications : Optional[str] = None
    responsibilities : Optional[str] = None
    benefits : Optional[str] = None
    application_deadline : Optional[datetime] = None

class JobUpdate(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    department : Optional[str] = None
    location : Optional[str] = None
    job_type : Optional[str] = None
    experience_level : Optional[str] = None
    salary : Optional[float] = None
    vacancies : Optional[int] = None
    skills_required : Optional[str] = None
    qualifications : Optional[str] = None
    responsibilities : Optional[str] = None
    benefits : Optional[str] = None
    application_deadline : Optional[datetime] = None
    is_active : Optional[bool] = None
    
    



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



@router.post('/hr/create_job')
def create_job(user: user_dependency, db: db_dependency, new_job: JobCreate):

    if user is None or user.get('role') != 'hr':
        raise HTTPException(status_code=401, detail='Failed Authentication')

    job_model = Jobs(
        **new_job.model_dump(),
        posted_by = user.get('id')
    )

    db.add(job_model)
    db.commit()

    return JSONResponse(status_code=201, content={'message': 'Job created successfully'})


@router.put('/hr/update_job/{job_id}')
def update_job(user: user_dependency, db: db_dependency, update_job: JobUpdate, job_id:int):

    if user is None or user.get('role') != 'hr':
        raise HTTPException(status_code=401, detail='Failed Authentication')

    job = db.query(Jobs).filter(Jobs.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail='Job not found')

    update_data = update_job.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(job,key,value)

    db.commit()

    return JSONResponse(status_code=200, content={'message': 'Job updated successfully'})


@router.delete('/hr/delete_job/{job_id}')
def delete_job(user: user_dependency, db: db_dependency, job_id: int):

    if user is None or user.get('role') != 'hr':
        raise HTTPException(status_code=401, detail='Failed Authentication')

    job = db.query(Jobs).filter(Jobs.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail='Job not found')

    db.query(Jobs).filter(Jobs.id == job_id).delete()
    db.commit()

    return JSONResponse(status_code=200, content={'message': 'Job Deleted successfully'})


@router.get('/hr/applications')
def get_all_applications(user: user_dependency, db: db_dependency):

    if user is None or user.get('role') != 'hr':
        raise HTTPException(status_code=401, detail='Failed Authentication')

    applications = db.query(JobApplications).all()
    return applications


@router.get('/hr/jobs/search')
def search_jobs(user: user_dependency, db: db_dependency, title: Optional[str] = Query(default=None), job_type: Optional[str] = Query(default=None), department: Optional[str] = Query(default=None)):

    if user is None or user.get('role') != 'hr':
        raise HTTPException(status_code=401, detail='Failed Authentication')

    query = db.query(Jobs)

    if title:
        query = query.filter(Jobs.title.ilike(f'%{title}%'))
    if job_type:
        query = query.filter(Jobs.job_type == job_type)
    if department:
        query = query.filter(Jobs.department == department)

    jobs = query.all()
    return jobs




# @router.post('/admin/create_issue')
# def create_issue(user: user_dependency, db: db_dependency, issue_request: IssueBook):

#     if user is None or user.get('role') != 'librarian':
#         raise HTTPException(status_code=401, detail='Failed Authentication')

#     book = db.query(Books).filter(Books.id == issue_request.book_id).first()
#     if book is None:
#         raise HTTPException(status_code=404, detail='Book not found')

#     member = db.query(Users).filter(Users.id == issue_request.user_id).first()
#     if member is None:
#         raise HTTPException(status_code=404, detail='Member not found')

#     if book.available_copies <= 0:
#         raise HTTPException(status_code=400, detail='No Copies Available')

#     loan_days = 14
#     issue_date = datetime.now()

#     issue_model = IssueRecords(
#         book_id=issue_request.book_id,
#         user_id=issue_request.user_id,
#         issue_date=issue_date,
#         due_date=issue_date + timedelta(days=loan_days),
#         status = 'issued'
#     )

#     book.available_copies -= 1
    
#     reservation = db.query(Reservations).filter(
#         Reservations.book_id == issue_request.book_id,
#         Reservations.user_id == issue_request.user_id,
#         Reservations.status == 'pending'
#     )
    
#     if reservation is not None:
#         reservation.status = 'approvd'

#     db.add(issue_model)
#     db.commit()

#     return JSONResponse(status_code=201, content={'message': 'Book added successfully'})


# @router.put('/admin/return_book/{issue_id}')
# def return_book(user: user_dependency, db: db_dependency, issue_id: int):

#     if user is None or user.get('role') != 'librarian':
#         raise HTTPException(status_code=401, detail='Failed Authentication')

#     issue = db.query(IssueRecords).filter(IssueRecords.id == issue_id).first()
#     if issue is None:
#         raise HTTPException(status_code=404, detail='Issue record not found')

#     return_date = datetime.now
#     fine = calculate_fine(issue.due_date, return_date)

#     issue.return_date = return_date
#     issue.status = 'returned'
#     issue.fine_amount = fine

#     book = db.query(Books).filter(Books.id == issue.book_id).first()
#     if book is not None:
#         book.available_copies += 1

#     db.commit()

#     return JSONResponse(status_code=201, content={'message': 'Book returned successfully', 'fine_amount': fine})


# @router.put('/admin/fine_paid/{issue_id}')
# def fine_paid(user: user_dependency, db: db_dependency, issue_id: int):

#     if user is None or user.get('role') != 'librarian':
#         raise HTTPException(status_code=401, detail='Failed Authentication')

#     issue = db.query(IssueRecords).filter(IssueRecords.id == issue_id).first()
#     if issue is None:
#         raise HTTPException(status_code=404, detail='Issue record not found')

#     issue.fine_paid = True

#     db.commit()

#     return JSONResponse(status_code=200, content={'message': 'Fine paid successfully'})