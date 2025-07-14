from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from tralvel_app.models.province import Province
from tralvel_app.models.food import Food
from tralvel_app.core.database import get_session
from tralvel_app.core.security import get_current_user
from tralvel_app.models.user import User

router = APIRouter()

@router.get("/")
def get_discount(session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    provinces = session.exec(select(Province)).all()
    foods = session.exec(select(Food)).all()

    result = {}

    for province in provinces:
        discount_rate = 0.4 if province.is_secondary else 0.5 
        food_discounts = []

        for food in foods:
            food_discounts.append({
                "food": food.name,
                "original_price": food.price,
                "discounted_price": round(food.price * discount_rate, 2)
            })

        result[province.name] = food_discounts

    return result
