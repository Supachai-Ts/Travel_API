from pydantic import BaseModel

class ProvinceCreate(BaseModel):
    name: str
    is_secondary: bool = False
