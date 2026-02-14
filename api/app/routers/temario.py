import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Temario
from app.schemas import TemarioCreate, TemarioRead, TemarioUpdate

router = APIRouter(prefix="/temario", tags=["temario"])


@router.get("/", response_model=list[TemarioRead])
async def list_temas(
    oposicion_id: uuid.UUID | None = None,
    bloque: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Temario)
    if oposicion_id:
        q = q.where(Temario.oposicion_id == oposicion_id)
    if bloque:
        q = q.where(Temario.bloque == bloque)
    q = q.order_by(Temario.num_tema).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{tema_id}", response_model=TemarioRead)
async def get_tema(tema_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Temario).where(Temario.id == tema_id))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Tema not found")
    return row


@router.post("/", response_model=TemarioRead, status_code=201)
async def create_tema(data: TemarioCreate, db: AsyncSession = Depends(get_db)):
    obj = Temario(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.post("/bulk", response_model=list[TemarioRead], status_code=201)
async def create_temas_bulk(data: list[TemarioCreate], db: AsyncSession = Depends(get_db)):
    objs = [Temario(**d.model_dump()) for d in data]
    db.add_all(objs)
    await db.commit()
    for obj in objs:
        await db.refresh(obj)
    return objs


@router.patch("/{tema_id}", response_model=TemarioRead)
async def update_tema(
    tema_id: uuid.UUID,
    data: TemarioUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Temario).where(Temario.id == tema_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Tema not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, val)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{tema_id}", status_code=204)
async def delete_tema(tema_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Temario).where(Temario.id == tema_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Tema not found")
    await db.delete(obj)
    await db.commit()
