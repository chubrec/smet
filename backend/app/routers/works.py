from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db import get_db


router = APIRouter()


@router.get("/", response_model=list[schemas.WorkOut])
def list_all(db: Session = Depends(get_db)):
    return crud.list_works(db)


@router.post("/", response_model=schemas.WorkOut)
def create(data: schemas.WorkCreate, db: Session = Depends(get_db)):
    return crud.create_work(db, data)


@router.get("/{work_id}", response_model=schemas.WorkOut)
def get_one(work_id: int, db: Session = Depends(get_db)):
    obj = crud.get_work(db, work_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Work not found")
    return obj


@router.delete("/{work_id}", status_code=204)
def delete(work_id: int, db: Session = Depends(get_db)):
    crud.delete_work(db, work_id)
    return None

