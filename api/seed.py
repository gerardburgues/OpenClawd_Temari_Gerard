"""Seed the database with hardcoded frontend data via the FastAPI endpoints."""

import json
import httpx
import sys

API = "http://localhost:8001"


def load(path: str):
    with open(path) as f:
        return json.load(f)


def main():
    client = httpx.Client(base_url=API, timeout=30)

    # Check API is up
    r = client.get("/health")
    if r.status_code != 200:
        print("API not reachable at", API)
        sys.exit(1)

    # Maps: old string id -> new UUID
    opo_map = {}
    conv_map = {}
    ley_map = {}

    # ── 1. Legislacion (no FK dependencies) ────────────────
    print("Inserting legislacion...")
    for ley in load("src/data/legislacion.json"):
        old_id = ley.pop("id")
        r = client.post("/legislacion/", json=ley)
        if r.status_code == 201:
            ley_map[old_id] = r.json()["id"]
            print(f"  + {ley['referencia']}")
        else:
            print(f"  ! {ley['referencia']}: {r.status_code} {r.text}")

    # ── 2. Oposiciones ─────────────────────────────────────
    print("\nInserting oposiciones...")
    for opo in load("src/data/oposiciones.json"):
        old_id = opo.pop("id")
        opo.pop("pipeline_started_at", None)  # not in our schema
        r = client.post("/oposiciones/", json=opo)
        if r.status_code == 201:
            opo_map[old_id] = r.json()["id"]
            print(f"  + {opo['nombre']} ({opo['grupo']}, {opo['ambito']})")
        else:
            print(f"  ! {opo['nombre']}: {r.status_code} {r.text}")

    # ── 3. Temario (depends on oposiciones + legislacion) ──
    print("\nInserting temario...")
    for tema in load("src/data/temario.json"):
        tema.pop("id")
        tema.pop("material_inap", None)  # not in our schema

        old_opo_id = tema["oposicion_id"]
        if old_opo_id not in opo_map:
            print(f"  ! Skipping tema {tema['num_tema']}: oposicion {old_opo_id} not found")
            continue
        tema["oposicion_id"] = opo_map[old_opo_id]

        # Remap leyes_vinculadas from old IDs to new UUIDs
        tema["leyes_vinculadas"] = [
            ley_map[lid] for lid in (tema.get("leyes_vinculadas") or []) if lid in ley_map
        ]

        r = client.post("/temario/", json=tema)
        if r.status_code == 201:
            print(f"  + Tema {tema['num_tema']}: {tema['titulo'][:60]}...")
        else:
            print(f"  ! Tema {tema['num_tema']}: {r.status_code} {r.text}")

    # ── 4. Convocatorias (depends on oposiciones) ──────────
    print("\nInserting convocatorias...")
    for conv in load("src/data/convocatorias.json"):
        old_id = conv.pop("id")

        old_opo_id = conv["oposicion_id"]
        if old_opo_id not in opo_map:
            print(f"  ! Skipping conv {old_id}: oposicion {old_opo_id} not found")
            continue
        conv["oposicion_id"] = opo_map[old_opo_id]

        r = client.post("/convocatorias/", json=conv)
        if r.status_code == 201:
            conv_map[old_id] = r.json()["id"]
            print(f"  + {old_opo_id} / {conv['anyo']} ({conv.get('tipo', '')})")
        else:
            print(f"  ! {old_id}: {r.status_code} {r.text}")

    # ── 5. Examenes (depends on convocatorias) ─────────────
    print("\nInserting examenes...")
    for exam in load("src/data/examenes.json"):
        exam.pop("id")

        old_conv_id = exam["convocatoria_id"]
        if old_conv_id not in conv_map:
            print(f"  ! Skipping exam: convocatoria {old_conv_id} not found")
            continue
        exam["convocatoria_id"] = conv_map[old_conv_id]

        r = client.post("/examenes/", json=exam)
        if r.status_code == 201:
            print(f"  + {exam.get('turno')} / {exam.get('modelo')} ({exam.get('fuente')})")
        else:
            print(f"  ! {old_conv_id}: {r.status_code} {r.text}")

    # ── Summary ────────────────────────────────────────────
    print("\n--- Seed complete ---")
    print(f"  Legislacion: {len(ley_map)}")
    print(f"  Oposiciones: {len(opo_map)}")
    print(f"  Convocatorias: {len(conv_map)}")

    counts = client.get("/oposiciones/count").json()
    print(f"\n  DB total oposiciones: {counts['count']}")


if __name__ == "__main__":
    main()
