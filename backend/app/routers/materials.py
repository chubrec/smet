from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db import get_db


router = APIRouter()


@router.get("/", response_model=list[schemas.MaterialOut])
def list_all(db: Session = Depends(get_db)):
    return crud.list_materials(db)


@router.post("/", response_model=schemas.MaterialOut)
def create(data: schemas.MaterialCreate, db: Session = Depends(get_db)):
    return crud.create_material(db, data)


@router.get("/{material_id}", response_model=schemas.MaterialOut)
def get_one(material_id: int, db: Session = Depends(get_db)):
    obj = crud.get_material(db, material_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Material not found")
    return obj


@router.delete("/{material_id}", status_code=204)
def delete(material_id: int, db: Session = Depends(get_db)):
    crud.delete_material(db, material_id)
    return None

