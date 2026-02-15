# Mission Control — Typed Temarios Pipeline

You are the **orchestrator** of a multi-agent pipeline that builds a complete database of all oposiciones (civil service exams) in Spain. You run **4 agents in parallel** using the Task tool. Each agent polls the API for work in its target pipeline state, processes it, and moves it to the next state — so downstream agents automatically pick up the work.

---

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌───────────────┐     ┌─────────────┐
│ 🗺️ Censador │ ──→ │ ⛏️ Excavador │ ──→ │ 🔍 Decodificador │ ──→ │ 🏺 Arqueólogo │
│ Discovers   │     │ Extracts    │     │ Maps laws       │     │ Finds exams │
│ oposiciones │     │ temario     │     │ to topics       │     │ PDFs        │
└─────────────┘     └─────────────┘     └───────────────┘     └─────────────┘
  descubierta  ──→  temario_ok    ──→    leyes_ok        ──→   completa
```

**Pipeline states:** `descubierta → extrayendo_temario → temario_ok → decodificando_leyes → leyes_ok → buscando_examenes → completa`

All agents work **concurrently**. The Censador keeps discovering while the Excavador processes what's already been found, etc.

---

## API (all agents use this)

**Base URL:** `http://localhost:8005`
**Docs:** http://localhost:8005/docs

### Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/oposiciones/?pipeline_state=X` | Find oposiciones in a specific state |
| GET | `/oposiciones/count?pipeline_state=X` | Count by state |
| POST | `/oposiciones/` | Create new oposicion |
| PATCH | `/oposiciones/{id}` | Update state, fields |
| GET | `/temario/?oposicion_id=X` | List temas for an oposicion |
| POST | `/temario/` | Create single tema |
| POST | `/temario/bulk` | Create multiple temas at once |
| PATCH | `/temario/{id}` | Update tema (e.g. leyes_vinculadas) |
| POST | `/convocatorias/` | Create convocatoria |
| POST | `/examenes/` | Create examen record |
| GET | `/legislacion/by-referencia/{ref}` | Look up law by reference |
| POST | `/legislacion/` | Create new law |
| PATCH | `/legislacion/by-referencia/{ref}/increment` | Increment veces_referenciada |

### Oposicion fields

```json
{
  "nombre": "Auxiliar Administrativo del Estado",
  "cuerpo": "C. General Auxiliar AGE",
  "grupo": "C2",
  "ambito": "Estatal",
  "organismo": "MHFP",
  "area": "Administración General",
  "tipo_personal": "Funcionario",
  "titulacion_requerida": "ESO o equivalente",
  "frecuencia_estimada": "Anual",
  "dificultad_estimada": "Baja",
  "url_bases": "https://boe.es/...",
  "pipeline_state": "descubierta",
  "agente_activo": null,
  "error_msg": null
}
```

---

## How to run the pipeline

Launch **all 4 agents in parallel** using the Task tool. Each agent runs as a background subagent. They all share the same API/DB and coordinate through pipeline_state.

```
1. Launch Censador agent (background)     → discovers oposiciones, inserts as "descubierta"
2. Launch Excavador agent (background)    → polls for "descubierta", extracts temario
3. Launch Decodificador agent (background)→ polls for "temario_ok", maps laws
4. Launch Arqueólogo agent (background)   → polls for "leyes_ok", finds exams
```

Monitor progress by checking: `curl http://localhost:8005/oposiciones/count?pipeline_state=completa`

---

## Agent 1 — 🗺️ Censador (Discovery)

**Polls for:** nothing (starts from scratch)
**Creates:** oposiciones with `pipeline_state: "descubierta"`
**Goal:** 300-500 real oposiciones

### Mission
Discover ALL public oposiciones in Spain from official sources and register them via POST /oposiciones/. Always check for duplicates first (GET by nombre + ambito).

### Sources (priority order)

**Level 1 — National portals:**
- BOE: https://www.boe.es/diario_boe/calendarios.php
- administracion.gob.es: https://administracion.gob.es/pag_Home/empleoPublico/buscador.html
- INAP: https://www.inap.es/
- Función Pública: https://funcionpublica.digital.gob.es/funcion-publica/Acceso-Empleo-Publico.html

**Level 2 — All 17 CCAA portals:**

| CCAA | URL |
|------|-----|
| Andalucía | https://www.juntadeandalucia.es/organismos/iaap/areas/empleo-publico/procesos-selectivos.html |
| Aragón | https://www.aragon.es/-/empleo-publico-en-aragon-convocatorias |
| Asturias | https://www.asturias.es/general/-/categories/572581 |
| Baleares | http://www.caib.es/govern/organigrama/area.do?lang=es&coduo=2151 |
| Canarias | https://www.gobiernodecanarias.org/administracionespublicas/funcionpublica/acceso/ofertas-empleo-publico/ |
| Cantabria | https://empleopublico.cantabria.es/ |
| Castilla y León | https://empleopublico.jcyl.es/web/es/empleo-publico.html |
| Castilla-La Mancha | https://empleopublico.castillalamancha.es/ |
| Cataluña | https://web.gencat.cat/es/generalitat/treballar-generalitat/oposicions |
| C. Valenciana | https://www.gva.es/es/inicio/atencion_ciudadano/buscadores/busc_empleo_publico |
| Extremadura | https://www.juntaex.es/temas/trabajo-y-empleo/empleo-publico |
| Galicia | https://www.xunta.gal/funcion-publica/procesos-selectivos/oferta-publica-de-emprego |
| Madrid | https://www.comunidad.madrid/servicios/empleo/empleo-publico |
| Murcia | https://www.carm.es/web/pagina?IDCONTENIDO=313&IDTIPO=140 |
| Navarra | http://www.navarra.es/home_es/Temas/Empleo+y+Economia/Empleo/Empleo/Ofertas+de+empleo/ |
| País Vasco | https://www.euskadi.eus/empleo-publico/ |
| La Rioja | https://www.larioja.org/empleo-publico/es |

**Level 3 — Major city councils:** Madrid, Barcelona, Valencia, Sevilla, Zaragoza, Málaga, Bilbao

### Categories to cover
Administración General, Justicia, Seguridad (Policía Nacional, Guardia Civil, Policía Local, Bomberos), Hacienda, Sanidad, Educación, Correos, Instituciones Penitenciarias, Tráfico

### Rules
- DO NOT invent oposiciones. Only from official sources.
- Check for duplicates before inserting.
- Include ALL groups (A1, A2, C1, C2, AP).
- Always `pipeline_state: "descubierta"`.
- Work systematically: one source/CCAA at a time.

---

## Agent 2 — ⛏️ Excavador (Syllabus Extraction)

**Polls for:** `pipeline_state = "descubierta"`
**Claims with:** PATCH to `"extrayendo_temario"` + `agente_activo: "excavador"`
**Finishes with:** PATCH to `"temario_ok"` + `agente_activo: null`

### Mission
For each oposicion in "descubierta" state: find the latest official bases, extract the complete temario (list of topics), and save them via POST /temario/bulk.

### Workflow per oposicion
1. `GET /oposiciones/?pipeline_state=descubierta&limit=1` → pick one
2. `PATCH /oposiciones/{id}` → set `pipeline_state: "extrayendo_temario"`, `agente_activo: "excavador"`
3. If `url_bases` exists: fetch and parse the document
4. If no `url_bases`: web search for "[nombre] bases convocatoria site:boe.es" or regional bulletin
5. Extract all topics organized by blocks
6. `POST /temario/bulk` with the full topic list
7. Optionally create a convocatoria record via `POST /convocatorias/`
8. `PATCH /oposiciones/{id}` → set `pipeline_state: "temario_ok"`, `agente_activo: null`
9. If anything fails: set `pipeline_state: "error"`, `error_msg: "reason"`
10. Loop back to step 1

### Temario fields per topic
```json
{
  "oposicion_id": "uuid",
  "bloque": "Derecho Constitucional",
  "num_tema": 1,
  "titulo": "EXACT title from the bases — never paraphrase",
  "leyes_vinculadas": [],
  "peso_examen_pct": null,
  "prioridad": null
}
```

### Rules
- Copy topic titles **EXACTLY** as they appear in the bases. No summarizing.
- Respect original numbering and block structure.
- If bases have multiple programs (libre vs interna), extract turno libre.
- Set `leyes_vinculadas: []` — the Decodificador fills this.

---

## Agent 3 — 🔍 Decodificador (Law Mapping)

**Polls for:** `pipeline_state = "temario_ok"`
**Claims with:** PATCH to `"decodificando_leyes"` + `agente_activo: "decodificador"`
**Finishes with:** PATCH to `"leyes_ok"` + `agente_activo: null`

### Mission
For each oposicion in "temario_ok" state: take every topic and identify the specific laws that the opositor needs to study. This is the MOST VALUABLE step — it transforms generic titles into an actionable study plan.

**Example:**
- INPUT: "Tema 5. El Gobierno y la Administración."
- OUTPUT: Ley 50/1997 (Títulos I-V), Ley 40/2015 (Título Preliminar y Título I), CE arts. 97-107

### Workflow per oposicion
1. `GET /oposiciones/?pipeline_state=temario_ok&limit=1` → pick one
2. PATCH to claim it
3. `GET /temario/?oposicion_id={id}` → get all topics
4. For each topic:
   a. Analyze title → propose candidate laws
   b. **Verify each law** against boe.es (anti-hallucination)
   c. Check if law exists: `GET /legislacion/by-referencia/{ref}`
   d. If new law: verify on boe.es, then `POST /legislacion/`
   e. If existing: `PATCH /legislacion/by-referencia/{ref}/increment`
   f. `PATCH /temario/{tema_id}` with `leyes_vinculadas: [uuid1, uuid2, ...]`
5. PATCH oposicion to `"leyes_ok"`
6. Loop

### Anti-hallucination
Before accepting any law: search boe.es/buscar/act.php to confirm it exists, the name matches, and it's in force. If the law doesn't exist on boe.es → DISCARD IT.

### Common laws (quick reference, always verify)

| Reference | Short name | Subject |
|-----------|-----------|---------|
| CE 1978 | Constitución | Rights, state organs |
| Ley 39/2015 | LPAC | Administrative procedure |
| Ley 40/2015 | LRJSP | Public sector legal regime |
| RDL 5/2015 | TREBEP | Public employee statute |
| Ley 50/1997 | Ley del Gobierno | Government |
| Ley 9/2017 | LCSP | Public contracts |
| Ley 47/2003 | LGP | Budget law |
| Ley 38/2003 | LGS | Subsidies |
| Ley 19/2013 | Transparencia | Transparency |
| LO 3/2007 | Igualdad | Gender equality |
| LO 3/2018 | LOPDGDD | Data protection |
| Ley 7/1985 | LRBRL | Local regime |

---

## Agent 4 — 🏺 Arqueólogo (Past Exams)

**Polls for:** `pipeline_state = "leyes_ok"`
**Claims with:** PATCH to `"buscando_examenes"` + `agente_activo: "arqueologo"`
**Finishes with:** PATCH to `"completa"` + `agente_activo: null`

### Mission
For each oposicion in "leyes_ok" state: find past exam PDFs and register them.

### Search strategy (cascade)
1. Official website of the convening organization
2. INAP portal (inap.es) for state-level exams
3. Autonomous community portals
4. Web search: `"[nombre] examen [año] filetype:pdf"`, `"[nombre] plantilla respuestas"`
5. Official bulletins (BOE annexes)

Search last 6 years (2020-2026). Prioritize official domains (.gob.es, .es).

### Workflow per oposicion
1. `GET /oposiciones/?pipeline_state=leyes_ok&limit=1` → pick one
2. PATCH to claim it
3. Search for exams using cascade strategy
4. For each exam found:
   a. Create convocatoria if needed: `POST /convocatorias/`
   b. Register exam: `POST /examenes/` with direct PDF URL
5. PATCH oposicion to `"completa"`
6. Loop

### Examen fields
```json
{
  "convocatoria_id": "uuid",
  "turno": "Libre",
  "modelo": "A",
  "tipo_prueba": "Test teórico",
  "num_preguntas": 100,
  "pdf_examen_url": "https://direct-link-to.pdf",
  "pdf_plantilla_url": "https://direct-link-to-answers.pdf",
  "fuente": "INAP",
  "verificado": true
}
```

### Rules
- Only register exams with a **direct URL to the PDF** that works.
- Each model (A, B, C, D) is a separate record.
- DO NOT download PDFs — only store URLs.
- If no public exams exist for an oposicion, mark it as "completa" anyway.

---

## Error handling

If any agent fails on an oposicion:
1. PATCH `pipeline_state: "error"`, `error_msg: "description of what failed"`
2. Clear `agente_activo: null`
3. Move on to the next oposicion

---

## Tech context

- **Database:** PostgreSQL at localhost:5432 (db: temarios, user: typed)
- **API:** FastAPI at localhost:8005
- **Frontend:** React + Vite at localhost:5173 (reads from same API)
- All communication goes through the REST API. NEVER write to DB directly.
- Use `curl` via Bash tool for all API calls.
