import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import oposiciones, temario, convocatorias, examenes, legislacion

# Import models so Base.metadata knows about all tables
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app = FastAPI(
    title="Typed Temarios API",
    description="API for the Typed oposiciones catalog — used by OpenClaw agents",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(oposiciones.router)
app.include_router(temario.router)
app.include_router(convocatorias.router)
app.include_router(examenes.router)
app.include_router(legislacion.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
