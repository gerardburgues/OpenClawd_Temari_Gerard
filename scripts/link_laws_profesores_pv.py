#!/usr/bin/env python3
"""Link legislation to topics for Profesor Educación Secundaria - País Vasco."""
import httpx

API = "http://localhost:8001"
OPO_ID = "80551157-5a9f-4e76-91e0-80ad8b0be9da"

client = httpx.Client(base_url=API, timeout=30)

# Get all legislation
leg_resp = client.get("/legislacion/?limit=200")
leg_map = {l["referencia"]: l["id"] for l in leg_resp.json()}

# Define law mappings by topic number
TOPIC_LAWS = {
    # Parte A - Legislación Educativa
    1: ["CE 1978"],  # Constitución y derecho a la educación
    2: ["LO 3/1979", "Ley 1/1993 PV"],  # Estatuto PV y Escuela Pública Vasca
    3: ["LO 3/2020"],  # LOMLOE - ESO
    4: ["LO 3/2020"],  # LOMLOE - Bachillerato
    5: ["LO 3/2022"],  # Ley FP
    6: ["LO 3/2020"],  # LOMLOE - atención diversidad
    7: ["RDL 5/2015", "LO 3/2020"],  # EBEP y función docente
    8: ["LO 3/2020", "Ley 1/1993 PV"],  # Organización centros
    9: ["LO 3/2020"],  # Evaluación sistema educativo
    10: ["Ley 1/1993 PV"],  # Euskera - Escuela Pública Vasca
    
    # Parte B - Didáctica y Pedagogía (menos legislación, más metodología)
    11: ["LO 3/2020"],  # Programación didáctica
    12: ["LO 3/2020"],  # Metodología didáctica
    13: ["LO 3/2020"],  # Evaluación
    14: [],  # TIC - más tecnología que ley
    15: ["LO 3/2020"],  # Tutoría y orientación
    16: [],  # Convivencia - metodológico
    17: ["LO 3/2007"],  # Igualdad de género y valores
    18: [],  # Desarrollo psicológico - no legislación específica
}

# Get all temario for this oposicion
tem_resp = client.get(f"/temario/?oposicion_id={OPO_ID}&limit=100")
temario = tem_resp.json()

updated = 0
errors = 0

for tema in temario:
    num = tema["num_tema"]
    tema_id = tema["id"]
    
    if num not in TOPIC_LAWS:
        continue
    
    refs = TOPIC_LAWS[num]
    ley_ids = []
    
    for ref in refs:
        if ref in leg_map:
            ley_ids.append(leg_map[ref])
        else:
            print(f"  ! Law not found: {ref}")
    
    if ley_ids:
        r = client.patch(f"/temario/{tema_id}", json={"leyes_vinculadas": ley_ids})
        if r.status_code == 200:
            updated += 1
            print(f"  ✓ Tema {num}: {len(ley_ids)} leyes vinculadas")
        else:
            errors += 1
            print(f"  ✗ Tema {num}: {r.status_code} {r.text}")
    else:
        print(f"  - Tema {num}: sin leyes específicas (metodología/pedagogía)")

print(f"\n--- Complete ---")
print(f"  Updated: {updated}")
print(f"  Errors: {errors}")
