from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db import get_db


router = APIRouter()


@router.get("/", response_model=list[schemas.ProjectOut])
def list_all(db: Session = Depends(get_db)):
    return crud.list_projects(db)


@router.post("/", response_model=schemas.ProjectOut)
def create(data: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, data)


@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_one(project_id: int, db: Session = Depends(get_db)):
    obj = crud.get_project(db, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj

