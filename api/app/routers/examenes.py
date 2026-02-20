import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Examen
from app.schemas import ExamenCreate, ExamenRead, ExamenUpdate

router = APIRouter(prefix="/examenes", tags=["examenes"])


@router.get("/", response_model=list[ExamenRead])
async def list_examenes(
    convocatoria_id: uuid.UUID | None = None,
    turno: str | None = None,
    tipo_prueba: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    q = select(Examen)
    if convocatoria_id:
        q = q.where(Examen.convocatoria_id == convocatoria_id)
    if turno:
        q = q.where(Examen.turno == turno)
    if tipo_prueba:
        q = q.where(Examen.tipo_prueba == tipo_prueba)
    q = q.offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{examen_id}", response_model=ExamenRead)
async def get_examen(examen_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Examen).where(Examen.id == examen_id))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Examen not found")
    return row


@router.post("/", response_model=ExamenRead, status_code=201)
async def create_examen(data: ExamenCreate, db: AsyncSession = Depends(get_db)):
    obj = Examen(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch("/{examen_id}", response_model=ExamenRead)
async def update_examen(
    examen_id: uuid.UUID,
    data: ExamenUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Examen).where(Examen.id == examen_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Examen not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, val)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{examen_id}", status_code=204)
async def delete_examen(examen_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Examen).where(Examen.id == examen_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Examen not found")
    await db.delete(obj)
    await db.commit()
