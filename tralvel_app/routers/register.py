from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from tralvel_app.schemas.user import UserCreate
from tralvel_app.models.user import User
from tralvel_app.core.database import get_session


router = APIRouter()

@router.post("/", response_model=User)
def register_user(data: UserCreate, session: Session = Depends(get_session)):
    user = User.from_orm(data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user