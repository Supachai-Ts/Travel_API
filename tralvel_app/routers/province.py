from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from tralvel_app.schemas.province import ProvinceCreate
from tralvel_app.models.province import Province
from tralvel_app.core.database import get_session

router = APIRouter()

@router.post("/", response_model=Province)
def create_province(data: ProvinceCreate, session: Session = Depends(get_session)):
    prov = Province.from_orm(data)
    session.add(prov)
    session.commit()
    session.refresh(prov)
    return prov

@router.get("/", response_model=list[Province])
def list_provinces(session: Session = Depends(get_session)):
    return session.exec(select(Province)).all()

@router.put("/{province_id}", response_model=Province)
def update_province(province_id: int, data: ProvinceCreate, session: Session = Depends(get_session)):
    prov = session.get(Province, province_id)
    if not prov:
        raise HTTPException(status_code=404, detail="Province not found")
    prov.name = data.name
    prov.is_secondary = data.is_secondary
    session.add(prov)
    session.commit()
    session.refresh(prov)
    return prov

@router.delete("/{province_id}")
def delete_province(province_id: int, session: Session = Depends(get_session)):
    prov = session.get(Province, province_id)
    if not prov:
        raise HTTPException(status_code=404, detail="Province not found")
    session.delete(prov)
    session.commit()
    return {"ok": True, "message": f"Province id {province_id} deleted"}
