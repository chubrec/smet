import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from openpyxl import Workbook

from .. import crud
from ..db import get_db


router = APIRouter()


@router.get("/estimate/{estimate_id}/pdf")
def export_pdf(estimate_id: int, db: Session = Depends(get_db)):
    estimate = crud.get_estimate(db, estimate_id)
    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    totals = crud.compute_totals(estimate)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Estimate: {estimate.name}")
    y -= 20
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Project ID: {estimate.project_id}")
    y -= 20
    p.drawString(50, y, "Items:")
    y -= 20
    for item in estimate.items:
        label = item.title_override or (item.work.name if item.work else (item.material.name if item.material else "Item"))
        p.drawString(60, y, f"{label}: {float(item.quantity)} {item.unit} x {float(item.unit_price)}")
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50

    y -= 10
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Subtotal: {totals.subtotal}")
    y -= 15
    p.drawString(50, y, f"Discount: {totals.discount}")
    y -= 15
    p.drawString(50, y, f"Surcharge: {totals.surcharge}")
    y -= 15
    p.drawString(50, y, f"Total: {totals.total}")
    p.showPage()
    p.save()

    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=estimate_{estimate.id}.pdf"})


@router.get("/estimate/{estimate_id}/xlsx")
def export_xlsx(estimate_id: int, db: Session = Depends(get_db)):
    estimate = crud.get_estimate(db, estimate_id)
    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    totals = crud.compute_totals(estimate)

    wb = Workbook()
    ws = wb.active
    ws.title = "Estimate"

    ws.append(["Name", "Unit", "Qty", "Unit Price", "Cost"])
    for item in estimate.items:
        label = item.title_override or (item.work.name if item.work else (item.material.name if item.material else "Item"))
        qty = float(item.quantity)
        price = float(item.unit_price)
        ws.append([label, item.unit, qty, price, qty * price])

    ws.append([])
    ws.append(["Subtotal", totals.subtotal])
    ws.append(["Discount", totals.discount])
    ws.append(["Surcharge", totals.surcharge])
    ws.append(["Total", totals.total])

    bio = io.BytesIO()
    wb.save(bio)
    bio.seek(0)
    return StreamingResponse(bio, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename=estimate_{estimate.id}.xlsx"})

