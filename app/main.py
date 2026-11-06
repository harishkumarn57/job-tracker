from fastapi import FastAPI

app = FastAPI(title="Job Application Tracker")


@app.get("/")
def home():
    return {"message": "Job Tracker API is running"}