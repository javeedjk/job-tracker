from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas, crud
from app.database import engine, get_db
from app.auth import create_access_token, get_current_user
from app.security import verify_password
from app.research_task import run_research_task
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Job Application Tracker")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://job-tracker-ten-beige.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- USER ROUTES ----------

@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)  # OAuth2 form calls it "username" but we use it as email
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}



# ---------- APPLICATION ROUTES ----------
# Now using the real logged-in user instead of a hardcoded id

@app.post("/applications", response_model=schemas.ApplicationOut)
def create_application(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_application(db, application, user_id=current_user.id)


@app.get("/applications", response_model=List[schemas.ApplicationOut])
def list_applications(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_applications(db, user_id=current_user.id)


@app.get("/applications/{application_id}", response_model=schemas.ApplicationOut)
def read_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    app_obj = crud.get_application(db, application_id, user_id=current_user.id)
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj


@app.put("/applications/{application_id}", response_model=schemas.ApplicationOut)
def update_application(
    application_id: int,
    updates: schemas.ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    app_obj = crud.update_application(db, application_id, user_id=current_user.id, updates=updates)
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj


@app.delete("/applications/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    app_obj = crud.delete_application(db, application_id, user_id=current_user.id)
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"detail": "Application deleted successfully"}


# ---------- COMPANY RESEARCH AGENT ROUTES ----------

@app.post("/applications/{application_id}/research")
def trigger_research(
    application_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    app_obj = crud.get_application(db, application_id, user_id=current_user.id)
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    app_obj.research_status = models.ResearchStatus.IN_PROGRESS
    db.commit()

    background_tasks.add_task(run_research_task, application_id)
    return {"detail": "Research started", "status": "in_progress"}


@app.get("/applications/{application_id}/research", response_model=schemas.ResearchStatusOut)
def get_research(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    app_obj = crud.get_application(db, application_id, user_id=current_user.id)
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj