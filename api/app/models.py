import uuid
from datetime import datetime, date

from sqlalchemy import (
    String, Integer, Float, Boolean, Text, Date, DateTime, ForeignKey, JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Oposicion(Base):
    __tablename__ = "oposiciones"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(500))
    cuerpo: Mapped[str | None] = mapped_column(String(300))
    grupo: Mapped[str | None] = mapped_column(String(10))  # A1, A2, C1, C2, AP
    ambito: Mapped[str] = mapped_column(String(200))
    organismo: Mapped[str | None] = mapped_column(String(300))
    area: Mapped[str | None] = mapped_column(String(200))
    tipo_personal: Mapped[str | None] = mapped_column(String(50))  # Funcionario / Laboral
    titulacion_requerida: Mapped[str | None] = mapped_column(String(300))
    frecuencia_estimada: Mapped[str | None] = mapped_column(String(50))
    dificultad_estimada: Mapped[str | None] = mapped_column(String(50))
    url_bases: Mapped[str | None] = mapped_column(Text)

    pipeline_state: Mapped[str] = mapped_column(String(50), default="descubierta")
    agente_activo: Mapped[str | None] = mapped_column(String(50))
    error_msg: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    temas: Mapped[list["Temario"]] = relationship(back_populates="oposicion", cascade="all, delete-orphan")
    convocatorias: Mapped[list["Convocatoria"]] = relationship(back_populates="oposicion", cascade="all, delete-orphan")


class Temario(Base):
    __tablename__ = "temario"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    oposicion_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("oposiciones.id", ondelete="CASCADE"))
    bloque: Mapped[str | None] = mapped_column(String(300))
    num_tema: Mapped[int] = mapped_column(Integer)
    titulo: Mapped[str] = mapped_column(Text)
    leyes_vinculadas: Mapped[list | None] = mapped_column(JSON, default=list)
    peso_examen_pct: Mapped[float | None] = mapped_column(Float)
    prioridad: Mapped[str | None] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    oposicion: Mapped["Oposicion"] = relationship(back_populates="temas")


class Convocatoria(Base):
    __tablename__ = "convocatorias"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    oposicion_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("oposiciones.id", ondelete="CASCADE"))
    anyo: Mapped[int] = mapped_column(Integer)
    tipo: Mapped[str | None] = mapped_column(String(100))  # Ordinaria, Extraordinaria, Estabilización
    plazas_libre: Mapped[int | None] = mapped_column(Integer)
    plazas_interna: Mapped[int | None] = mapped_column(Integer)
    plazas_total: Mapped[int | None] = mapped_column(Integer)
    fecha_publicacion: Mapped[date | None] = mapped_column(Date)
    fecha_inicio_plazo: Mapped[date | None] = mapped_column(Date)
    fecha_fin_plazo: Mapped[date | None] = mapped_column(Date)
    fecha_examen: Mapped[date | None] = mapped_column(Date)
    estado: Mapped[str | None] = mapped_column(String(50))  # Convocada, Plazo abierto, En proceso, Resuelta
    url_boe: Mapped[str | None] = mapped_column(Text)
    nota_corte_teorico: Mapped[float | None] = mapped_column(Float)
    ratio_opositores_plaza: Mapped[float | None] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    oposicion: Mapped["Oposicion"] = relationship(back_populates="convocatorias")
    examenes: Mapped[list["Examen"]] = relationship(back_populates="convocatoria", cascade="all, delete-orphan")


class Examen(Base):
    __tablename__ = "examenes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    convocatoria_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("convocatorias.id", ondelete="CASCADE"))
    turno: Mapped[str | None] = mapped_column(String(50))  # Libre, Promoción interna
    modelo: Mapped[str | None] = mapped_column(String(20))  # A, B, C, D, Único
    tipo_prueba: Mapped[str | None] = mapped_column(String(100))
    num_preguntas: Mapped[int | None] = mapped_column(Integer)
    pdf_examen_url: Mapped[str | None] = mapped_column(Text)
    pdf_plantilla_url: Mapped[str | None] = mapped_column(Text)
    fuente: Mapped[str | None] = mapped_column(String(100))  # INAP, BOE, Portal CCAA, etc.
    verificado: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    convocatoria: Mapped["Convocatoria"] = relationship(back_populates="examenes")


class Legislacion(Base):
    __tablename__ = "legislacion"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    referencia: Mapped[str] = mapped_column(String(100), unique=True)  # "Ley 39/2015"
    nombre_corto: Mapped[str | None] = mapped_column(String(100))     # "LPAC"
    nombre_completo: Mapped[str | None] = mapped_column(Text)
    url_boe: Mapped[str | None] = mapped_column(Text)
    fecha_verificacion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    veces_referenciada: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
