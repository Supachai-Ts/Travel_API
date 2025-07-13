from fastapi import FastAPI
from tralvel_app.core.database import create_db_and_tables
from tralvel_app.routers import  auth, register, user, province, food, discount


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(register.router, prefix="/register", tags=["register"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(province.router, prefix="/province", tags=["province"])
app.include_router(food.router, prefix="/food", tags=["Food"])
app.include_router(discount.router, prefix="/discount", tags=["discount"])
