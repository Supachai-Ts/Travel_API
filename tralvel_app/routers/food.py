from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from tralvel_app.models.food import Food
from tralvel_app.schemas.food import FoodCreate
from tralvel_app.core.database import get_session
from tralvel_app.core.security import get_current_user
from tralvel_app.models.user import User

router = APIRouter()

@router.post("/", response_model=Food)
def create_food(data: FoodCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    food = Food(**data.dict())
    session.add(food)
    session.commit()
    session.refresh(food)
    return food

@router.get("/", response_model=list[Food])
def list_foods(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return session.exec(select(Food)).all()

@router.put("/{food_id}", response_model=Food)
def update_food(food_id: int, data: FoodCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    food = session.get(Food, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    food.name = data.name
    food.price = data.price
    session.add(food)
    session.commit()
    session.refresh(food)
    return food

@router.delete("/{food_id}")
def delete_food(food_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    food = session.get(Food, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    session.delete(food)
    session.commit()
    return {"ok": True, "message": f"Food id {food_id} deleted"}
