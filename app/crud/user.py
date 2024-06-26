from sqlalchemy.orm import Session
from app.models.user import User as DBUser
from app.schemas.user import UserCreate, UserUpdate
from app.utils import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(DBUser).filter(DBUser.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBUser).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user:
        db_user.username = user_update.username
        db_user.email = user_update.email
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
