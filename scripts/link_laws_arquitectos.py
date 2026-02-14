#!/usr/bin/env python3
"""Link legislation to topics for Arquitectos de la Hacienda Pública."""
import httpx
import json

API = "http://localhost:8001"
OPO_ID = "b5fac144-af65-4b7a-afab-2c60bd751bc5"

client = httpx.Client(base_url=API, timeout=30)

# Get all legislation
leg_resp = client.get("/legislacion/?limit=200")
leg_map = {l["referencia"]: l["id"] for l in leg_resp.json()}

# Define law mappings by topic number
TOPIC_LAWS = {
    # Bloque I - Derecho Constitucional, Administrativo
    1: ["CE 1978"],
    2: ["CE 1978", "LO 6/1985", "LO 2/1979", "LO 3/1981"],
    3: ["CE 1978", "Ley 50/1997", "Ley 40/2015"],
    4: ["CE 1978", "Ley 7/1985"],
    5: [],  # EU Law - no Spanish legislation
    6: ["CE 1978", "Ley 39/2015"],
    7: ["Ley 39/2015"],
    8: ["Ley 39/2015"],
    9: ["Ley 29/1998"],
    10: ["Ley 39/2015", "Ley 40/2015"],
    11: ["Ley 9/2017"],
    12: ["Ley 40/2015", "Ley 9/2017"],
    13: ["RDL 5/2015"],
    14: ["Ley 19/2013", "Ley 40/2015"],
    15: ["LO 3/2007"],
    16: ["Ley 39/2015", "Ley 40/2015"],
    17: ["Ley 47/2003"],
    18: ["Ley 38/2003"],
    
    # Bloque II - Derecho Civil y Mercantil
    19: ["Codigo Civil"],
    20: ["Codigo Civil"],
    21: ["Codigo Civil", "LAU 29/1994"],
    22: ["Codigo Civil"],
    23: ["Codigo Civil", "Ley Hipotecaria"],
    24: ["Codigo Civil"],
    25: ["Ley Hipotecaria"],
    26: ["Codigo Civil"],
    27: ["Codigo Civil"],
    28: ["Codigo de Comercio"],
    29: ["RDL 1/2010"],
    30: ["Codigo de Comercio"],
    31: ["Codigo de Comercio"],
    32: ["RDL 1/2020"],
    33: ["Ley Hipotecaria"],
    34: ["RDL 1/2004", "Ley Hipotecaria"],
    35: [],  # Notariado
    36: ["Codigo Civil"],
    37: ["Ley 1/2000"],
    
    # Bloque III - Catastro
    38: ["RDL 1/2004"],
    39: ["RDL 1/2004"],
    40: ["RDL 1/2004"],
    41: ["RDL 1/2004"],
    42: ["RDL 1/2004"],
    43: ["RDL 1/2004", "Ley 7/1985"],
    44: ["RDL 1/2004"],
    45: ["RDL 1/2004"],
    46: ["RDL 1/2004"],
    47: [],  # EU Cadastre comparison
    
    # Bloque IV - Valoración, Urbanismo, Edificación
    48: [],  # Theory of value - no specific law
    49: [],  # Valuation methods
    50: ["RDL 1/2004"],
    51: ["Ley 58/2003", "RDL 1/2004"],
    52: ["RDL 7/2015"],
    53: ["Orden ECO/805/2003"],
    54: ["CE 1978", "RDL 7/2015"],
    55: ["RDL 7/2015"],
    56: ["RDL 7/2015"],
    57: ["RDL 7/2015"],
    58: [],  # Territorial planning - regional laws
    59: ["Ley 38/1999"],
    60: ["RD 314/2006"],
    61: [],  # Housing - general topic
    62: [],  # Construction - technical topic
    63: [],  # Real estate market
    64: ["Ley 33/2003"],
    65: ["Ley 9/2017"],
    66: ["Ley 9/2017"],
    67: ["Ley 16/1954", "RDL 7/2015"],
    68: ["Ley 33/2003", "LAU 29/1994"],
    69: ["RDL 7/2015"],
    70: ["RDL 7/2015"],
    
    # Bloque V - Hacienda Pública, Derecho Financiero
    71: ["CE 1978", "Ley 47/2003"],
    72: ["Ley 58/2003"],
    73: ["Ley 58/2003"],
    74: ["Ley 58/2003"],
    75: ["Ley 35/2006"],
    76: ["Ley 27/2014"],
    77: ["Ley 37/1992"],
    78: ["RDL 1/1993"],
    79: ["Ley 29/1987"],
    80: ["RDL 2/2004"],
    81: ["RDL 2/2004"],
    82: ["Ley 19/1991"],
    83: ["Ley 22/2009"],
    84: ["RDL 2/2004"],
    85: [],  # EU tax system
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
        print(f"  - Tema {num}: sin leyes específicas")

print(f"\n--- Complete ---")
print(f"  Updated: {updated}")
print(f"  Errors: {errors}")
