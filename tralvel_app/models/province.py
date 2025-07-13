from sqlmodel import SQLModel, Field
from typing import Optional

class Province(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    is_secondary: bool = False
    
