from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db import get_db


router = APIRouter()


@router.post("/", response_model=schemas.EstimateOut)
def create(data: schemas.EstimateCreate, db: Session = Depends(get_db)):
    return crud.create_estimate(db, data)


@router.get("/{estimate_id}", response_model=schemas.EstimateOut)
def get_one(estimate_id: int, db: Session = Depends(get_db)):
    obj = crud.get_estimate(db, estimate_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Estimate not found")
    return obj


@router.get("/{estimate_id}/totals", response_model=schemas.Totals)
def totals(estimate_id: int, db: Session = Depends(get_db)):
    obj = crud.get_estimate(db, estimate_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Estimate not found")
    return crud.compute_totals(obj)


@router.get("/project/{project_id}", response_model=list[schemas.EstimateOut])
def list_for_project(project_id: int, db: Session = Depends(get_db)):
    return crud.list_estimates_for_project(db, project_id)

