# Database Schema (PostgreSQL)

Generated from [models.py](models.py).

## users

```sql
CREATE TABLE users (
    id SERIAL,
    email varchar(200) DEFAULT NULL,
    username varchar(45) DEFAULT NULL,
    firstname varchar(45) DEFAULT NULL,
    lastname varchar(45) DEFAULT NULL,
    hash_password varchar(200) DEFAULT NULL,
    is_active boolean DEFAULT NULL,
    role varchar(45) DEFAULT NULL,
    PRIMARY KEY (id)
);

CREATE INDEX ix_users_id ON users (id);

CREATE TABLE jobs (
    id SERIAL,
    title varchar(200) DEFAULT NULL,
    description varchar(1000) DEFAULT NULL,
    department varchar(100) DEFAULT NULL,
    location varchar(100) DEFAULT NULL,
    job_type varchar(45) DEFAULT NULL,
    experience_level varchar(45) DEFAULT NULL,
    salary integer DEFAULT NULL,
    vacancies integer DEFAULT NULL,
    skills_required varchar(1000) DEFAULT NULL,
    qualifications varchar(1000) DEFAULT NULL,
    responsibilities varchar(1000) DEFAULT NULL,
    benefits varchar(1000) DEFAULT NULL,
    application_deadline timestamp DEFAULT NULL,
    is_active boolean DEFAULT NULL,
    posted_by integer DEFAULT NULL,
    created_at timestamp DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (posted_by) REFERENCES users(id)
);

CREATE INDEX ix_jobs_id ON jobs (id);


CREATE TABLE job_applications (
    id SERIAL,
    job_id integer DEFAULT NULL,
    user_id integer DEFAULT NULL,
    applied_date timestamp DEFAULT NULL,
    status varchar(45) DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX ix_job_applications_id ON job_applications (id);
```
