from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional
import models
from models import Jobs, Users, JobApplications
from database import engine, SessionLocal
from fastapi.responses import JSONResponse
from router import auth, admin
from router.auth import get_current_user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(admin.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get('/jobs/all')
def get_all_jobs(db: db_dependency):

    jobs = db.query(Jobs).all()
    return jobs


@app.get('/jobs/search')
def search_jobs(db: db_dependency, title: Optional[str] = Query(default=None), job_type: Optional[str] = Query(default=None), department: Optional[str] = Query(default=None)):

    query = db.query(Jobs)

    if title:
        query = query.filter(Jobs.title.ilike(f'%{title}%'))
    if job_type:
        query = query.filter(Jobs.job_type == job_type)
    if department:
        query = query.filter(Jobs.department == department)

    jobs = query.all()
    return jobs




@app.get('/job/{job_id}')
def get_specific_job( user: user_dependency, db: db_dependency, job_id: int ):
    if user is None:
        raise HTTPException( status_code=401, detail='Failed Authentication')

    job = db.query(Jobs).filter(Jobs.id == job_id).first()

    if job is None:
        raise HTTPException( status_code=404,detail='Job not found')

    return job

@app.post('/apply/{job_id}')
def apply_job(user: user_dependency, db: db_dependency, job_id: int):

    if user is None:
        raise HTTPException(status_code=401, detail='Failed Authentication')

    job = db.query(Jobs).filter(Jobs.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail='Job not found')

    application_model = JobApplications(
        job_id = job_id,
        user_id = user.get('id'),
        status = 'pending'
    )

    db.add(application_model)
    db.commit()

    return JSONResponse(status_code=201, content={'message': 'Job applied successfully'})


@app.delete('/apply/cancel/{application_id}')
def cancel_application(user: user_dependency, db: db_dependency, application_id: int):

    if user is None:
        raise HTTPException(status_code=401, detail='Failed Authentication')

    application = db.query(JobApplications).filter(JobApplications.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail='Application not found')

    application.status = 'cancelled'
    db.commit()

    return JSONResponse(status_code=201, content={'message': 'Application cancelled successfully'})


@app.get('/apply/my')
def my_applications(user: user_dependency, db: db_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail='Failed Authentication')

    applications = db.query(JobApplications).filter(JobApplications.user_id == user.get('id')).all()
    return applications
