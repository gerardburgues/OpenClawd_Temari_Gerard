import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Legislacion
from app.schemas import LegislacionCreate, LegislacionRead, LegislacionUpdate

router = APIRouter(prefix="/legislacion", tags=["legislacion"])


@router.get("/", response_model=list[LegislacionRead])
async def list_legislacion(
    referencia: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    q = select(Legislacion)
    if referencia:
        q = q.where(Legislacion.referencia.ilike(f"%{referencia}%"))
    q = q.order_by(Legislacion.veces_referenciada.desc()).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/by-referencia/{referencia}", response_model=LegislacionRead)
async def get_by_referencia(referencia: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Legislacion).where(Legislacion.referencia == referencia))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Legislacion not found")
    return row


@router.get("/{ley_id}", response_model=LegislacionRead)
async def get_legislacion(ley_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Legislacion).where(Legislacion.id == ley_id))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Legislacion not found")
    return row


@router.post("/", response_model=LegislacionRead, status_code=201)
async def create_legislacion(data: LegislacionCreate, db: AsyncSession = Depends(get_db)):
    obj = Legislacion(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch("/{ley_id}", response_model=LegislacionRead)
async def update_legislacion(
    ley_id: uuid.UUID,
    data: LegislacionUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Legislacion).where(Legislacion.id == ley_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Legislacion not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, val)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch("/by-referencia/{referencia}/increment", response_model=LegislacionRead)
async def increment_referencia(referencia: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Legislacion).where(Legislacion.referencia == referencia))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Legislacion not found")
    obj.veces_referenciada += 1
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{ley_id}", status_code=204)
async def delete_legislacion(ley_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Legislacion).where(Legislacion.id == ley_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Legislacion not found")
    await db.delete(obj)
    await db.commit()
