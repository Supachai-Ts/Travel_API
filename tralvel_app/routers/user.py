from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from tralvel_app.schemas.user import UserCreate
from tralvel_app.models.user import User
from tralvel_app.core.database import get_session

router = APIRouter()

@router.get("/", response_model=list[User])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserCreate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.firstname = user_update.firstname
    user.lastname = user_update.lastname
    user.age = user_update.age
    user.username = user_update.username
    user.password = user_update.password

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return user