# Typed — Temarios: Complete Knowledge Base

> Extracted from Notion workspace (Typed/Temarios) — 2026-02-13

---

## Table of Contents

1. [About Typed](#about-typed)
2. [The Temarios Project](#the-temarios-project)
3. [System Architecture](#system-architecture)
4. [Data Model (5 Tables)](#data-model-5-tables)
5. [Agent Pipeline](#agent-pipeline)
   - [Coordination System](#coordination-system-heartbeat--staggered-crons)
   - [Agent 1: Censador (Discovery)](#agent-1--censador-discovery)
   - [Agent 2: Excavador (Syllabus Extraction)](#agent-2--excavador-syllabus-extraction)
   - [Agent 3: Decodificador (Law Mapping)](#agent-3--decodificador-law-mapping)
   - [Agent 4: Arqueólogo (Past Exams)](#agent-4--arqueólogo-past-exams)
6. [Document Processing Pipeline](#document-processing-pipeline)
7. [Question Generation Pipeline](#question-generation-pipeline)
8. [Roadmap](#roadmap)
9. [Risks & Mitigations](#risks--mitigations)
10. [Success Metrics](#success-metrics)
11. [Key Reference Data](#key-reference-data)

---

## About Typed

**Typed** is an **AI-powered study platform** designed specifically for **opositores** (public exam candidates) in Spain. It helps people preparing for civil service exams study more efficiently by transforming their study documents into interactive material.

### Core Features

| Category | Features |
|----------|----------|
| **Auto-generated material** | Test questions, Flashcards (spaced repetition / forgetting curve), Summaries, Concept diagrams |
| **Study assistant** | AI Chat about materials, Mistake notebook, Personalized mock exams |
| **Platforms** | Web app (primary), Mobile app (iOS/Android) |

### Target Customer

- **Opositores in Spain** — people preparing exams for civil service positions
- Study extensive, dense syllabi (laws, regulations, procedures)
- Need to memorize large volumes of information
- Value tools that optimize study time
- Need practice with multiple-choice test questions (standard format in Spanish public exams)

### Business Model

| Plan | Limits |
|------|--------|
| **Free** | Up to 40 pages per document |
| **Paid** | Up to 200 pages per document, more features |

**Contact:** jordi@typedai.com | typedai.com

---

## The Temarios Project

### Problem Statement

1. Each oposicion has official bases listing topics to study, but they **don't link to the actual documents** you need to study
2. Manual topic compilation is **extremely time-consuming**
3. Many users upload the **same document multiple times** to Typed (paying double/triple for the same content)
4. Users pay academies for syllabi that could be freely available

### Objective

Build a **complete database of all oposiciones in Spain** (national + 17 autonomous communities) with syllabus, official bases, and past exams, using AI agents in parallel to automate collection.

### How It Should Work (Internal)

1. Upload bases (official exam rules) of an oposicion
2. AI detects the topics, classified by blocks
3. For each topic, AI identifies which laws/regulations apply and which specific parts to study
4. Generate a structured table with a "Notes/Clarifications" column indicating exactly what part of each document to study

### How It Should Work (External)

Same as internal, but with a folder structure for organizing oposiciones by autonomous community. Should also show which documents are **most commonly shared** across different oposiciones.

### What Has Been Tested

Using Gemini to take a list of topics and identify which laws correspond to each one — **results were good enough** to proceed.

---

## System Architecture

### Tech Stack

| Component | Technology |
|-----------|-----------|
| **Database** | PostgreSQL (own, no Notion dependency) — works as shared task queue between agents |
| **Agents** | OpenClaw with 4 parallel instances, each with its own SOUL.md |
| **Coordination** | Heartbeat system (each agent polls DB periodically) + staggered crons |
| **Dashboard** | React + Vite (Mission Control-style Control Center) |
| **LLM** | Claude (for parsing official documents) |
| **Architecture Reference** | Based on Mission Control pattern from Bhanu Teja P (SiteGPT) — 10 OpenClaw agents coordinated with heartbeats and shared DB |

---

## Data Model (5 Tables)

### 1. `oposiciones` — Master catalog

| Field | Description | Example |
|-------|-------------|---------|
| nombre | Name | "Auxiliar Administrativo del Estado" |
| cuerpo | Corps/body | "C. General Auxiliar AGE" |
| grupo | Group | A1, A2, C1, C2, AP |
| ambito | Scope | "Estatal" or CCAA name |
| organismo | Organization | "MHFP", "Junta de Andalucía" |
| area | Area | "Administración General", "Justicia", "Sanidad" |
| tipo_personal | Personnel type | "Funcionario" or "Laboral" |
| titulacion_requerida | Required qualification | Minimum degree required |
| frecuencia_estimada | Estimated frequency | "Anual", "Bienal", "Irregular" |
| dificultad_estimada | Estimated difficulty | "Baja", "Media", "Alta", "Muy Alta" |
| url_bases | URL to latest published bases | URL |
| pipeline_state | Pipeline status | See pipeline states below |

**Pipeline states:** `Descubierta → Extrayendo temario → Temario OK → Decodificando leyes → Leyes OK → Buscando exámenes → Completa`

### 2. `temario` — Individual topics

| Field | Description |
|-------|-------------|
| oposicion_id | FK to oposicion |
| bloque | Block name (e.g., "Derecho Constitucional") |
| num_tema | Topic number within the program |
| titulo | EXACT title as it appears in the bases |
| leyes_vinculadas | Array of legislation IDs (filled by Decodificador) |
| peso_examen_pct | % weight in exam (filled by Analyst later) |
| prioridad | Study priority (filled later) |

### 3. `convocatorias` — Specific calls/announcements

| Field | Description |
|-------|-------------|
| oposicion_id | FK |
| anyo | Year |
| tipo | "Ordinaria", "Extraordinaria", "Estabilización" |
| plazas_libre / plazas_interna / plazas_total | Seats available |
| fecha_publicacion | Publication date in BOE/bulletin |
| fecha_inicio_plazo / fecha_fin_plazo | Registration period |
| fecha_examen | Exam date (if known) |
| estado | "Convocada", "Plazo abierto", "En proceso", "Resuelta" |
| url_boe | URL to official announcement |
| nota_corte_teorico | Theoretical cutoff score |
| ratio_opositores_plaza | Applicants per seat ratio |

### 4. `examenes` — Past exams with downloadable PDFs

| Field | Description |
|-------|-------------|
| convocatoria_id | FK to convocatoria |
| turno | "Libre" or "Promoción interna" |
| modelo | "A", "B", "C", "D" or "Único" |
| tipo_prueba | "Test teórico", "Supuesto práctico", "Caso práctico", "Psicotécnico" |
| num_preguntas | Number of questions (if test) |
| pdf_examen_url | Direct URL to exam PDF |
| pdf_plantilla_url | Direct URL to answer key PDF |
| fuente | "INAP", "BOE", "Portal CCAA", "Portal organismo", "Web" |
| verificado | true if PDF is accessible and readable |

### 5. `legislacion` — Auto-generated law catalog

| Field | Description | Example |
|-------|-------------|---------|
| referencia | Reference | "Ley 39/2015", "RDL 5/2015" |
| nombre_corto | Short name | "LPAC", "TREBEP" |
| nombre_completo | Full official title | Full text |
| url_boe | Direct URL to consolidated law on boe.es | URL |
| fecha_verificacion | Last verification date | NOW() |
| veces_referenciada | Times referenced across all oposiciones | Counter |

---

## Agent Pipeline

### Coordination System: Heartbeat + Staggered Crons

Each agent "phones home" periodically by querying the PostgreSQL database. On each heartbeat:

1. Reports its status (idle, working, error)
2. Queries for oposiciones in the state it needs to process
3. If work found: claims it (updates state so another agent doesn't take it) and executes
4. If no work: goes back to sleep until next heartbeat

**Staggered crons** prevent API saturation and collisions:

| Agent | Interval | Cron | Reason |
|-------|----------|------|--------|
| Censador | Every 2 min | `*/2 * * * *` | Quick discovery, light tasks |
| Excavador | Every 3 min | `1-59/3 * * * *` | PDF parsing, heavier |
| Decodificador | Every 4 min | `2-59/4 * * * *` | Analysis + BOE verification |
| Arqueólogo | Every 5 min | `3-59/5 * * * *` | Extensive web search, slowest |

**Critical lesson learned (from Mission Control):** Agents can respond "HEARTBEAT_OK" without actually executing the DB query if the prompt isn't well-designed. The agent short-circuits before making the real call. **Solution:** Always test the complete flow with real data from day one.

**Optimistic locking** in PostgreSQL handles collisions: the first agent to update the state wins, the second one sees it changed and looks for another task.

---

### Agent 1 — Censador (Discovery)

- **Icon:** 🗺️
- **Mission:** Discover ALL public oposiciones in Spain and register them in the database
- **Does NOT:** Extract syllabi, search exams, or analyze laws
- **Creates state:** `Descubierta`
- **Heartbeat:** Every 2 minutes
- **Approach:** A single skill using the LLM to navigate any portal (BOE, administracion.gob.es, autonomous portals) without needing specific adapters per CCAA

#### Sources (Priority Order)

**Level 1 — National portals:**
- BOE — Public employment: boe.es/diario_boe/calendarios.php
- administracion.gob.es — Convocatoria search
- INAP: inap.es
- Función Pública (MTDFP)

**Level 2 — All 17 Autonomous Community portals:**
- Andalucía, Aragón, Asturias, Baleares, Canarias, Cantabria, Castilla y León, Castilla-La Mancha, Cataluña, C. Valenciana, Extremadura, Galicia, Madrid, Murcia, Navarra, País Vasco, La Rioja

**Level 3 — Major city councils:**
- Madrid, Barcelona, Valencia, Sevilla, Zaragoza, Málaga, Bilbao

**Level 4 — Provincial councils (Diputaciones)**

#### Categories to Cover

- Administración General (Administrativo, Auxiliar, Gestión, TAC)
- Justicia (Tramitación Procesal, Auxilio Judicial, Gestión Procesal, Letrados)
- Seguridad (Policía Nacional, Guardia Civil, Policía Local, Bomberos)
- Hacienda (Técnico, Inspector, Gestión)
- Sanidad (SAS, SERMAS, SACYL... auxiliar adm., celador, enfermería)
- Educación (Maestros, Profesores Secundaria, Inspectores)
- Correos y Telégrafos
- Instituciones Penitenciarias
- Tráfico
- Organismos autónomos y entes públicos

#### Rules

- Only register oposiciones found in official sources
- Only access official public administration portals
- If a portal is down, log error and move to the next
- Prioritize oposiciones with the most seats and highest demand
- Include ALL groups (A1, A2, C1, C2, AP)

---

### Agent 2 — Excavador (Syllabus Extraction)

- **Icon:** ⛏️
- **Mission:** Extract the official syllabus and convocatoria data for each discovered oposicion
- **Reads state:** `Descubierta` → Updates to `Extrayendo temario` → Then `Temario OK`
- **Heartbeat:** Every 3 minutes

#### Workflow Per Oposicion

1. Read `url_bases` field
2. Navigate to URL and download/read the bases document
3. If PDF: parse with LLM to extract structured information
4. If web page: read content directly
5. Extract complete syllabus (all topics organized by blocks)
6. Extract convocatoria data (seats, dates, requirements)
7. Save everything to DB
8. If bases not accessible: Google search for them

#### Typical Bases Structure

1. Object of the convocatoria
2. Applicant requirements
3. Applications and deadline
4. Selection process (phases, exercises)
5. **PROGRAMA** ← the syllabus is here
6. Tribunal
7. Scoring

#### Rules

- Copy topic titles **EXACTLY** as they appear in the bases — no summarizing, translating, or paraphrasing
- Include subtopics as part of the title (separated by ". ")
- Respect original numbering
- If bases have multiple programs (free turn vs internal promotion), extract the free turn
- If access fails: set pipeline_state to "error" with error_msg

---

### Agent 3 — Decodificador (Law Mapping)

- **Icon:** 🔍
- **Mission:** Map each topic to the specific laws the candidate needs to study
- **Reads state:** `Temario OK` → Updates to `Decodificando leyes` → Then `Leyes OK`
- **Heartbeat:** Every 4 minutes
- **The most valuable agent in the pipeline**

#### What It Does (Example)

- **INPUT:** "Tema 5. El Gobierno y la Administración. Relaciones del Gobierno con las Cortes Generales."
- **OUTPUT:** Ley 50/1997 del Gobierno (Títulos I-V), Ley 40/2015 LRJSP (Título Preliminar y Título I), CE arts. 97-107

Without this agent, the opositor has a list of topics but **doesn't know WHICH laws to open**.

#### Auto-Generated Legislation Catalog

The `legislacion` table starts empty and fills up as the Decodificador works:

1. Check if law already exists in `legislacion` table
2. If YES: reuse its ID, increment `veces_referenciada`
3. If NO: verify the law (anti-hallucination) and insert

**Key efficiency insight:** The first ~20 oposiciones will be slow because the catalog is empty. After that, ~80% of laws will already be catalogued and just get reused.

#### Anti-Hallucination: Mandatory Verification

Before accepting any law as real:

1. Navigate to `boe.es/buscar/act.php`
2. Search for exact reference (e.g., "Ley 39/2015")
3. Confirm: law exists, full name matches, URL works, law is in force (not repealed)
4. **If law doesn't exist on boe.es: DISCARD IT** — it's a hallucination
5. If repealed: include only if the oposicion bases still require it

#### Cross-Validation

Compare mappings between similar oposiciones to detect errors. If Topic 5 of Administrativo AGE maps to Ley 50/1997 and the equivalent topic in Administrativo JA also does, that confirms the mapping is correct.

#### Most Common Laws (Quick Reference)

| Reference | Short Name | Subject |
|-----------|-----------|---------|
| CE 1978 | Constitución | Rights, state organs, territorial organization |
| Ley 39/2015 | LPAC | Common administrative procedure |
| Ley 40/2015 | LRJSP | Legal regime of the public sector |
| RDL 5/2015 | TREBEP | Public employee statute |
| Ley 50/1997 | Ley del Gobierno | Government functions, composition |
| Ley 9/2017 | LCSP | Public sector contracts |
| Ley 47/2003 | LGP | General Budget Law |
| Ley 38/2003 | LGS | General Subsidies Law |
| Ley 19/2013 | Transparencia | Access, transparency, good governance |
| LO 3/2007 | Igualdad | Effective equality women and men |
| LO 3/2018 | LOPDGDD | Data protection |
| Ley 7/1985 | LRBRL | Local regime |
| LO 6/1985 | LOPJ | Judiciary |
| Ley 29/1998 | LJCA | Contentious-administrative jurisdiction |
| Ley 58/2003 | LGT | General Tax Law |

---

### Agent 4 — Arqueólogo (Past Exams)

- **Icon:** 🏺
- **Mission:** Find and register past exam papers for each oposicion
- **Reads state:** `Leyes OK` → Updates to `Buscando exámenes` → Then `Completa`
- **Heartbeat:** Every 5 minutes

#### Cascade Search Strategy

Search in this order (keep going even if you find some — more is better):

1. **Official website** of the convening organization
2. **INAP portal** (inap.es → Public employment → Selective processes)
3. **Autonomous community function public portals**
4. **Web search** with specific queries:
   - `"[oposicion name] examen [year] filetype:pdf"`
   - `"[oposicion name] cuestionario [year] site:boe.es"`
   - `"[oposicion name] plantilla respuestas [year]"`
5. **Official bulletins** (some exams published as annexes in BOE)

Search the last 6 years (2019-2025). Prioritize official domains (.gob.es, .es).

#### Rules

- Only register exams with a **direct URL to the PDF** — no guessing
- **Verify each URL works** (PDF can be opened). If 404, don't register
- Each model (A, B, C, D) gets its own separate record
- Prioritize recent exams (2022-2025) but don't ignore older ones
- **DO NOT download PDFs to disk** — only store URLs
- If a portal requires login: log the limitation, don't try to register

---

## Document Processing Pipeline

Typed's core document processing follows a 4-worker pipeline:

```
USER UPLOADS FILE
       |
       v
 Worker 1         Worker 2              Worker 3             Worker 4 (Orchestrator)
 File Conversion → Text Extraction    → Chapter Save       → Question Generation
                   + Structure           + Launch Orchestrator
```

### Worker 1: File Conversion & S3 Upload

- Downloads raw file from S3
- Converts Office/Image formats to PDF
- Trims pages (free plan: max 40, paid: max 200)
- Uploads final PDF to S3

### Worker 2: Text Extraction & Structure Detection

**The most critical decision point** — determines how the document is processed:

```
PDF File
   |
   v
PyMuPDF Quick Check (sample first 10 pages)
   |
avg >= 100 chars/page?
  /              \
YES               NO
 |                 |
Has TOC?          OCR Engine
/     \           (DeepSeek or Marker)
YES    NO
|       \
PATH A:  PATH B:
PyMuPDF  OCR Engine
+ TOC    (GPU-based)
```

- **PATH A (fast, ~1-2s):** PyMuPDF text extraction + PDF bookmarks for TOC
- **PATH B (slow):** OCR via DeepSeek (default) or Marker (GPU on Modal)
  - Marker: PDF→Markdown conversion, AI organizes headers into TOC
  - For scanned PDFs (avg < 50 chars/page): runs `ocrmypdf` preprocessing first

### Worker 3: Chapter Generation

- Uses pre-extracted structure from Worker 2
- Uploads chapter JSONs to S3
- Creates Chapter objects in database
- Routes to question/flashcard generation

### Worker 4: Question Generation (Orchestrator)

See [Question Generation Pipeline](#question-generation-pipeline) below.

---

## Question Generation Pipeline

The orchestrator runs a multi-step AI pipeline using proposition-based Path A/B system:

### Step 1: Page Division (code only)
- Splits chunks into 2-page blocks

### Step 0: Law Identification (gemini-2.5-flash-lite, 1 call)
- Extracts first 15,000 characters of raw PDF text
- Returns: `{law_name, abbreviation, date, topic_area}`
- Determines if document is legal or general

### Step 2: Concept Extraction (gemini-2.5-flash-lite, semaphore=40)
- Selects prompt based on document type:
  - **No TOC:** extracts ALL concepts
  - **TOC + Law:** law-specific extraction
  - **TOC + General:** general extraction
- Only leaf chapters with direct_content >= 100 chars are processed
- Filtering: percentile 60 + cap 150 (TOC) | score cap 150 (non-TOC)

### Step 3a: Path Classification (gemini-2.5-flash-lite, semaphore=40)
- **Path A (intra-article):** Distractors from sibling propositions with subtle distortions
- **Path B (inter-article):** Distractors from altering specific data points (deadlines, numbers, subjects)

### Step 3b: Distractor Generation (gemini-3-flash-preview, semaphore=40)
- Generates 3 incorrect options per concept
- Uses different prompts for Path A vs Path B, Legal vs General

### Step 3c: Stem Generation (gemini-2.5-flash-lite, semaphore=40)
- Generates the question text for each concept + distractors

### Step 3d: Composition + Randomization (code only)
- Combines stem + correct answer + 3 distractors
- Randomizes option order (A/B/C/D)

### Step 3e: Flashcard Generation (gemini-2.5-flash, parallel)
- Uses composed questions as context
- Generates flashcards in blocks of 50

### Step 4: Database Persistence
- Bulk creates QuestionsDoc + QuestionOption records
- Links to Chapter and KeyConcepts via M2M

### AI Model Usage

| Step | Model | Concurrency | Purpose |
|------|-------|------------|---------|
| Concept extraction | gemini-2.5-flash-lite | Semaphore(40) | Extract propositions per chapter |
| Law identification | gemini-2.5-flash-lite | 1 call total | Detect if document is law-related |
| Path classification | gemini-2.5-flash-lite | Semaphore(40) | Classify each concept as Path A/B |
| Distractor generation | gemini-3-flash-preview | Semaphore(40) | Generate 3 wrong options |
| Stem generation | gemini-2.5-flash-lite | Semaphore(40) | Generate question text |
| Flashcard generation | gemini-2.5-flash | Block-based | Generate flashcards |
| Marker header org | gemini-3-flash-preview | 1 call total | Organize markdown headers into TOC |

All calls go through `openrouter_service.py` with Langfuse `@observe` tracing.

---

## Roadmap

### Phase 0 — Infrastructure (Week 1)
- [ ] Install OpenClaw on dedicated VPS (Docker)
- [ ] Configure PostgreSQL with 5-table schema
- [ ] Deploy dashboard (Control Center)
- [ ] Configure heartbeat system + staggered crons
- [ ] Create base SOUL.md for each agent
- [ ] Test complete heartbeat flow with real data (avoid short-circuit bug)

### Phase 1 — Complete Census (Weeks 2-3)
- [ ] Single Censador skill covering all scopes (national + 17 CCAA + local)
- [ ] Include: Administración General, Justicia, Seguridad, Hacienda, Sanidad, Educación
- [ ] Include common local oposiciones (Auxiliar/Administrativo Ayuntamiento, Policía Local, Bomberos)
- [ ] **Goal:** 300-500 oposiciones catalogued

### Phase 2 — Syllabus Extraction (Weeks 3-5)
- [ ] Single Excavador skill parsing bases from any bulletin (BOE, BOJA, DOGC, BOCM, etc.)
- [ ] Extract exam structure (test, practical case, oral) and weights
- [ ] **Goal:** Topic titles extracted for 80% of catalog

### Phase 2.5 — Law Decoding (Weeks 4-6)
- [ ] Decodificador skill: map each topic to specific laws
- [ ] Auto-generated legislation catalog
- [ ] Anti-hallucination verification against boe.es
- [ ] Cross-validation between similar oposiciones
- [ ] Link to INAP support materials when available
- [ ] **Goal:** 70% of topics with linked laws and direct BOE URLs

### Phase 3 — Exam Recovery (Weeks 5-8)
- [ ] Arqueólogo with cascade search
- [ ] PDF download and storage
- [ ] Link exams with answer keys
- [ ] **Goal:** At least 2-3 past exams for the most popular oposiciones

### Phase 4 — Analysis & Intelligence (Weeks 7-10)
- [ ] Analyst agent: calculate block weight per exam
- [ ] Detect trends between calls
- [ ] Auto-generate "Study Priority" field
- [ ] Calculate historical ratios (applicants/seat, cutoff scores)

### Phase 5 — Public Website for Opositores (Weeks 10-14)
- [ ] Design public frontend (Typed-style)
- [ ] Search by oposicion, CCAA, group
- [ ] Individual oposicion page with syllabus, exams, and analysis
- [ ] Direct access to PDFs and BOE links
- [ ] SEO to rank each oposicion page

---

## Risks & Mitigations

| Risk | Probability | Mitigation |
|------|------------|------------|
| Official websites change structure | High | Use LLM for flexible parsing instead of rigid scraping |
| LLM API cost spikes | Medium | Aggressive caching, only invoke LLM with new content |
| Exams not publicly available | Medium | Document which oposiciones lack public exams |
| OpenClaw security | Medium | Run on isolated VPS, no access to personal accounts |
| Incomplete data for small CCAAs | High | Prioritize 5 highest-volume CCAAs, complete rest gradually |
| Decodificador assigns wrong laws | Medium | Cross-validation + manually review top 20 oposiciones as ground truth |
| Agent short-circuits heartbeat | High | Test full flow with real data from day 1, design SOUL.md to force DB query |
| Agent collisions (two agents grab same oposicion) | Medium | Optimistic lock in PostgreSQL |

---

## Success Metrics

| Metric | Target |
|--------|--------|
| **Census** | 500+ oposiciones catalogued (national + 17 CCAA + local) |
| **Syllabi** | 80% with complete program extracted |
| **Laws decoded** | 70% of topics with linked laws, BOE URLs, and specific articles |
| **Exams** | 60% with at least 2 past exams |
| **Pipeline** | 90% of oposiciones in "Completa" state in 10 weeks |
| **Errors** | Less than 5% of records with unresolved errors |

---

## Key Reference Data

### Key Files in Codebase

| File | Purpose |
|------|---------|
| `typedapp/Files/views.py` | Upload API endpoint (POST) |
| `typedapp/Files/document_processing_worker.py` | Worker 1: conversion, trimming, S3 |
| `typedapp/Files/Services/upload_worker_service.py` | Workers 2+3: extraction, chunking, routing |
| `typedapp/Files/Services/pdf_processing_service.py` | Unified extraction decision logic |
| `typedapp/TOC/toc_extraction_service.py` | PDF bookmark (TOC) extraction |
| `typedapp/Marker/marker_service.py` | Marker OCR service |
| `typedapp/Files/Services/agents/mainAgent/orchestrator_agent.py` | Worker 4: question generation pipeline |
| `typedapp/Files/Services/agents/conceptsAgent/concept_extraction_agent.py` | Concept extraction (v2) |
| `typedapp/Files/Services/agents/generationAgent/generation_agent.py` | Stem + flashcard generation |
| `typedapp/Files/Services/agents/generationAgent/options_generation_agent.py` | Law ID, path classification, distractors |
| `typedapp/Files/Services/agents/dbAgent/persistence_agent.py` | Database persistence |
| `typedapp/services/openrouter_service.py` | Central AI routing (all generation calls) |

### Product Backlog Highlights

**UX/UI:**
- Keyboard accessibility
- Calendar heatmap cursor
- Help center in header
- Visual feedback on document deletion
- Hide sidebar during exams

**Features:**
- Remember previous exam config (number of questions, type)
- Copy on "Summarize document"
- Upload document from summary view
- Save folder name
- Justification language setting

**Functionalities:**
- Onboarding flow
- Paywall system
- Forgetting curve (spaced repetition)
- Practical cases (Supuestos Prácticos)
- Psychotechnical tests
- Social Security practical cases

---

> **Source:** Notion workspace — Typed/Temarios and related pages
> **Last extracted:** 2026-02-13

---

## Temarios Loaded Into Backend

### ETGOA - Escala Técnica de Gestión de Organismos Autónomos (A2)
- **ID:** c8468432-82e4-41d0-bbe2-fd3a12fc01ff
- **Status:** ✅ COMPLETED (2025-02-15)
- **Total temas:** 173
- **Bloques:**
  - Materias Comunes: 38 temas
  - Específico I - Derecho Constitucional y Administrativo: 45 temas
  - Específico II - Economía y Administración Financiera: 45 temas
  - Específico III - Recursos Humanos: 45 temas
- **Source:** BOE convocatoria (Anexo II)
