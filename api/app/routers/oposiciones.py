import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Oposicion
from app.schemas import OposicionCreate, OposicionRead, OposicionUpdate

router = APIRouter(prefix="/oposiciones", tags=["oposiciones"])


@router.get("/", response_model=list[OposicionRead])
async def list_oposiciones(
    pipeline_state: str | None = None,
    ambito: str | None = None,
    grupo: str | None = None,
    area: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    q = select(Oposicion)
    if pipeline_state:
        q = q.where(Oposicion.pipeline_state == pipeline_state)
    if ambito:
        q = q.where(Oposicion.ambito == ambito)
    if grupo:
        q = q.where(Oposicion.grupo == grupo)
    if area:
        q = q.where(Oposicion.area == area)
    q = q.offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/count")
async def count_oposiciones(
    pipeline_state: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(func.count(Oposicion.id))
    if pipeline_state:
        q = q.where(Oposicion.pipeline_state == pipeline_state)
    result = await db.execute(q)
    return {"count": result.scalar()}


@router.get("/{oposicion_id}", response_model=OposicionRead)
async def get_oposicion(oposicion_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Oposicion).where(Oposicion.id == oposicion_id))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Oposicion not found")
    return row


@router.post("/", response_model=OposicionRead, status_code=201)
async def create_oposicion(data: OposicionCreate, db: AsyncSession = Depends(get_db)):
    obj = Oposicion(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch("/{oposicion_id}", response_model=OposicionRead)
async def update_oposicion(
    oposicion_id: uuid.UUID,
    data: OposicionUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Oposicion).where(Oposicion.id == oposicion_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Oposicion not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, val)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{oposicion_id}", status_code=204)
async def delete_oposicion(oposicion_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Oposicion).where(Oposicion.id == oposicion_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Oposicion not found")
    await db.delete(obj)
    await db.commit()
