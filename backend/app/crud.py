from sqlalchemy.orm import Session

from . import models, schemas


# Work CRUD
def create_work(db: Session, work: schemas.WorkCreate) -> models.Work:
    db_work = models.Work(**work.model_dump())
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work


def list_works(db: Session) -> list[models.Work]:
    return db.query(models.Work).all()


def get_work(db: Session, work_id: int) -> models.Work | None:
    return db.query(models.Work).get(work_id)


def delete_work(db: Session, work_id: int) -> None:
    obj = db.query(models.Work).get(work_id)
    if obj:
        db.delete(obj)
        db.commit()


# Material CRUD
def create_material(db: Session, material: schemas.MaterialCreate) -> models.Material:
    obj = models.Material(**material.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_materials(db: Session) -> list[models.Material]:
    return db.query(models.Material).all()


def get_material(db: Session, material_id: int) -> models.Material | None:
    return db.query(models.Material).get(material_id)


def delete_material(db: Session, material_id: int) -> None:
    obj = db.query(models.Material).get(material_id)
    if obj:
        db.delete(obj)
        db.commit()


# Project CRUD
def create_project(db: Session, project: schemas.ProjectCreate) -> models.Project:
    obj = models.Project(**project.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_projects(db: Session) -> list[models.Project]:
    return db.query(models.Project).all()


def get_project(db: Session, project_id: int) -> models.Project | None:
    return db.query(models.Project).get(project_id)


# Estimate CRUD
def create_estimate(db: Session, estimate: schemas.EstimateCreate) -> models.Estimate:
    obj = models.Estimate(
        project_id=estimate.project_id,
        name=estimate.name,
        discount_percent=estimate.discount_percent,
        surcharge_percent=estimate.surcharge_percent,
    )
    db.add(obj)
    db.flush()
    for item in estimate.items:
        db_item = models.EstimateItem(estimate_id=obj.id, **item.model_dump())
        db.add(db_item)
    db.commit()
    db.refresh(obj)
    return obj


def get_estimate(db: Session, estimate_id: int) -> models.Estimate | None:
    return db.query(models.Estimate).get(estimate_id)


def list_estimates_for_project(db: Session, project_id: int) -> list[models.Estimate]:
    return db.query(models.Estimate).filter(models.Estimate.project_id == project_id).all()


def compute_totals(estimate: models.Estimate) -> schemas.Totals:
    subtotal = sum(float(item.quantity) * float(item.unit_price) for item in estimate.items)
    discount = subtotal * float(estimate.discount_percent) / 100.0
    after_discount = subtotal - discount
    surcharge = after_discount * float(estimate.surcharge_percent) / 100.0
    total = after_discount + surcharge
    return schemas.Totals(
        subtotal=round(subtotal, 2),
        discount=round(discount, 2),
        surcharge=round(surcharge, 2),
        total=round(total, 2),
    )

