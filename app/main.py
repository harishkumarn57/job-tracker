from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import jobs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker")

app.include_router(jobs.router)


@app.get("/")
def home():
    return {"message": "Job Tracker API is running"}