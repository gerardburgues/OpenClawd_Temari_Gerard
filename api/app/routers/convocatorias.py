import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Convocatoria
from app.schemas import ConvocatoriaCreate, ConvocatoriaRead, ConvocatoriaUpdate

router = APIRouter(prefix="/convocatorias", tags=["convocatorias"])


@router.get("/", response_model=list[ConvocatoriaRead])
async def list_convocatorias(
    oposicion_id: uuid.UUID | None = None,
    anyo: int | None = None,
    estado: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    q = select(Convocatoria)
    if oposicion_id:
        q = q.where(Convocatoria.oposicion_id == oposicion_id)
    if anyo:
        q = q.where(Convocatoria.anyo == anyo)
    if estado:
        q = q.where(Convocatoria.estado == estado)
    q = q.order_by(Convocatoria.anyo.desc()).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{convocatoria_id}", response_model=ConvocatoriaRead)
async def get_convocatoria(convocatoria_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Convocatoria).where(Convocatoria.id == convocatoria_id))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Convocatoria not found")
    return row


@router.post("/", response_model=ConvocatoriaRead, status_code=201)
async def create_convocatoria(data: ConvocatoriaCreate, db: AsyncSession = Depends(get_db)):
    obj = Convocatoria(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch("/{convocatoria_id}", response_model=ConvocatoriaRead)
async def update_convocatoria(
    convocatoria_id: uuid.UUID,
    data: ConvocatoriaUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Convocatoria).where(Convocatoria.id == convocatoria_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Convocatoria not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, val)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{convocatoria_id}", status_code=204)
async def delete_convocatoria(convocatoria_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Convocatoria).where(Convocatoria.id == convocatoria_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Convocatoria not found")
    await db.delete(obj)
    await db.commit()
