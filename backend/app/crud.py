from sqlalchemy.orm import Session
from app import models, schemas
from app.security import hash_password


# ---------- USER CRUD ----------

def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # reloads it with the id Postgres assigned
    return new_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# ---------- APPLICATION CRUD ----------

def create_application(db: Session, application: schemas.ApplicationCreate, user_id: int):
    new_app = models.Application(
        **application.model_dump(),
        user_id=user_id,
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app


def get_applications(db: Session, user_id: int):
    return db.query(models.Application).filter(models.Application.user_id == user_id).all()


def get_application(db: Session, application_id: int, user_id: int):
    return db.query(models.Application).filter(
        models.Application.id == application_id,
        models.Application.user_id == user_id,
    ).first()


def update_application(db: Session, application_id: int, user_id: int, updates: schemas.ApplicationUpdate):
    app_obj = get_application(db, application_id, user_id)
    if not app_obj:
        return None

    update_data = updates.model_dump(exclude_unset=True)  # only fields actually sent
    for key, value in update_data.items():
        setattr(app_obj, key, value)

    db.commit()
    db.refresh(app_obj)
    return app_obj


def delete_application(db: Session, application_id: int, user_id: int):
    app_obj = get_application(db, application_id, user_id)
    if not app_obj:
        return None

    db.delete(app_obj)
    db.commit()
    return app_obj