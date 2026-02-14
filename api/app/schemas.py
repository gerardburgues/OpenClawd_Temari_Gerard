from __future__ import annotations

import uuid
from datetime import datetime, date

from pydantic import BaseModel, ConfigDict


# ── Oposicion ──────────────────────────────────────────────

class OposicionBase(BaseModel):
    nombre: str
    cuerpo: str | None = None
    grupo: str | None = None
    ambito: str
    organismo: str | None = None
    area: str | None = None
    tipo_personal: str | None = None
    titulacion_requerida: str | None = None
    frecuencia_estimada: str | None = None
    dificultad_estimada: str | None = None
    url_bases: str | None = None
    pipeline_state: str = "descubierta"
    agente_activo: str | None = None
    error_msg: str | None = None


class OposicionCreate(OposicionBase):
    pass


class OposicionUpdate(BaseModel):
    nombre: str | None = None
    cuerpo: str | None = None
    grupo: str | None = None
    ambito: str | None = None
    organismo: str | None = None
    area: str | None = None
    tipo_personal: str | None = None
    titulacion_requerida: str | None = None
    frecuencia_estimada: str | None = None
    dificultad_estimada: str | None = None
    url_bases: str | None = None
    pipeline_state: str | None = None
    agente_activo: str | None = None
    error_msg: str | None = None


class OposicionRead(OposicionBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ── Temario ────────────────────────────────────────────────

class TemarioBase(BaseModel):
    oposicion_id: uuid.UUID
    bloque: str | None = None
    num_tema: int
    titulo: str
    leyes_vinculadas: list | None = []
    peso_examen_pct: float | None = None
    prioridad: str | None = None


class TemarioCreate(TemarioBase):
    pass


class TemarioUpdate(BaseModel):
    bloque: str | None = None
    num_tema: int | None = None
    titulo: str | None = None
    leyes_vinculadas: list | None = None
    peso_examen_pct: float | None = None
    prioridad: str | None = None


class TemarioRead(TemarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ── Convocatoria ───────────────────────────────────────────

class ConvocatoriaBase(BaseModel):
    oposicion_id: uuid.UUID
    anyo: int
    tipo: str | None = None
    plazas_libre: int | None = None
    plazas_interna: int | None = None
    plazas_total: int | None = None
    fecha_publicacion: date | None = None
    fecha_inicio_plazo: date | None = None
    fecha_fin_plazo: date | None = None
    fecha_examen: date | None = None
    estado: str | None = None
    url_boe: str | None = None
    nota_corte_teorico: float | None = None
    ratio_opositores_plaza: float | None = None


class ConvocatoriaCreate(ConvocatoriaBase):
    pass


class ConvocatoriaUpdate(BaseModel):
    anyo: int | None = None
    tipo: str | None = None
    plazas_libre: int | None = None
    plazas_interna: int | None = None
    plazas_total: int | None = None
    fecha_publicacion: date | None = None
    fecha_inicio_plazo: date | None = None
    fecha_fin_plazo: date | None = None
    fecha_examen: date | None = None
    estado: str | None = None
    url_boe: str | None = None
    nota_corte_teorico: float | None = None
    ratio_opositores_plaza: float | None = None


class ConvocatoriaRead(ConvocatoriaBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ── Examen ─────────────────────────────────────────────────

class ExamenBase(BaseModel):
    convocatoria_id: uuid.UUID
    turno: str | None = None
    modelo: str | None = None
    tipo_prueba: str | None = None
    num_preguntas: int | None = None
    pdf_examen_url: str | None = None
    pdf_plantilla_url: str | None = None
    fuente: str | None = None
    verificado: bool = False


class ExamenCreate(ExamenBase):
    pass


class ExamenUpdate(BaseModel):
    turno: str | None = None
    modelo: str | None = None
    tipo_prueba: str | None = None
    num_preguntas: int | None = None
    pdf_examen_url: str | None = None
    pdf_plantilla_url: str | None = None
    fuente: str | None = None
    verificado: bool | None = None


class ExamenRead(ExamenBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ── Legislacion ────────────────────────────────────────────

class LegislacionBase(BaseModel):
    referencia: str
    nombre_corto: str | None = None
    nombre_completo: str | None = None
    url_boe: str | None = None
    fecha_verificacion: datetime | None = None
    veces_referenciada: int = 0


class LegislacionCreate(LegislacionBase):
    pass


class LegislacionUpdate(BaseModel):
    referencia: str | None = None
    nombre_corto: str | None = None
    nombre_completo: str | None = None
    url_boe: str | None = None
    fecha_verificacion: datetime | None = None
    veces_referenciada: int | None = None


class LegislacionRead(LegislacionBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
