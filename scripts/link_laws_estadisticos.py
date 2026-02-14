#!/usr/bin/env python3
"""Link legislation to topics for Estadísticos del Estado (INE)."""
import httpx

API = "http://localhost:8001"
OPO_ID = "ef6f95cb-abfc-4741-9135-0d9d13d9e563"

client = httpx.Client(base_url=API, timeout=30)

# Get all legislation
leg_resp = client.get("/legislacion/?limit=200")
leg_map = {l["referencia"]: l["id"] for l in leg_resp.json()}

# Define law mappings - most statistical topics don't have specific laws
TOPIC_LAWS = {
    1: ["Ley 12/1989"],  # Sistema Estadístico Nacional
    2: [],  # EU Regulation - not Spanish law
    3: [],  # Survey design - methodology
    4: [],  # Complex sampling - methodology
    5: [],  # Data collection - methodology
    6: [],  # Non-response - methodology
    7: [],  # Data validation - methodology
    8: [],  # Census - methodology
    9: [],  # Demographics - methodology
    10: [],  # EPA - methodology
    11: [],  # IPC - methodology
    12: [],  # National accounts - methodology (SEC 2010 is EU)
    13: [],  # Sector accounts - methodology
    14: [],  # Business statistics - methodology
    15: ["LO 3/2018", "RGPD 2016/679"],  # Statistical secrecy and data protection
    16: [],  # Classifications - methodology
    17: [],  # Probability theory
    18: [],  # Probability distributions
    19: [],  # Point estimation
    20: [],  # Confidence intervals
    21: [],  # Parametric tests
    22: [],  # ANOVA
    23: [],  # Linear regression
    24: [],  # GLM
    25: [],  # Time series
    26: [],  # Multivariate analysis
    27: [],  # Databases - technology
    28: [],  # Data warehousing - technology
    29: [],  # Big Data - technology
    30: [],  # Programming languages - technology
}

# Get all temario for this oposicion
tem_resp = client.get(f"/temario/?oposicion_id={OPO_ID}&limit=100")
temario = tem_resp.json()

updated = 0

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
            print(f"  ✗ Tema {num}: {r.status_code} {r.text}")
    else:
        print(f"  - Tema {num}: sin leyes específicas (metodología/tecnología)")

print(f"\n--- Complete ---")
print(f"  Updated: {updated}")
