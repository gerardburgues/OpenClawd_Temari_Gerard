#!/usr/bin/env python3
"""
Process TCAE del SACYL specifically - this has many explicit laws in tema titles.
"""
import json
import re
import requests
from urllib.parse import quote

API_BASE = "http://localhost:8001"
OPOSICION_ID = "81d3e91b-2bd6-4352-9021-327b1dc3f9fc"

# More comprehensive patterns for SACYL temario
def extract_laws_sacyl(titulo):
    """Extract laws from SACYL temario titles."""
    laws = []
    
    # Explicit patterns found in SACYL temario
    patterns = [
        (r"Constituci[oó]n\s+Espa[ñn]ola", "CE 1978"),
        (r"Estatuto\s+de\s+Autonom[ií]a\s+de\s+Castilla\s+y\s+Le[oó]n", "LO 14/2007 CyL"),
        (r"Ley\s+14/1986", "Ley 14/1986"),
        (r"Ley\s+16/2003", "Ley 16/2003"),
        (r"Ley\s+8/2010", "Ley 8/2010 CyL"),
        (r"Ley\s+55/2003", "Ley 55/2003"),
        (r"Ley\s+41/2002", "Ley 41/2002"),
        (r"Ley\s+31/1995", "Ley 31/1995"),
        (r"Ley\s+Org[aá]nica\s+3/2018", "LO 3/2018"),
        (r"Ley\s+Org[aá]nica\s+3/2007", "LO 3/2007"),
        (r"Ley\s+Org[aá]nica\s+1/2004", "LO 1/2004"),
        (r"Ley\s+1/2003", "Ley 1/2003 CyL"),
        (r"Reglamento\s+General\s+de\s+Proteccion\s+de\s+Datos", "RGPD 2016/679"),
        (r"\(UE\)\s+2016/679", "RGPD 2016/679"),
    ]
    
    for pattern, ref in patterns:
        if re.search(pattern, titulo, re.IGNORECASE):
            if ref not in laws:
                laws.append(ref)
    
    return laws

# Law definitions for creating new records
LAWS_TO_CREATE = {
    "LO 14/2007 CyL": {
        "referencia": "LO 14/2007 CyL",
        "nombre_corto": "Estatuto Autonomía Castilla y León",
        "nombre_completo": "Ley Orgánica 14/2007, de 30 de noviembre, de reforma del Estatuto de Autonomía de Castilla y León",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2007-20635"
    },
    "Ley 8/2010 CyL": {
        "referencia": "Ley 8/2010 CyL",
        "nombre_corto": "Ley Ordenación Sistema Salud CyL",
        "nombre_completo": "Ley 8/2010, de 30 de agosto, de Ordenación del Sistema de Salud de Castilla y León",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2010-15237"
    },
    "Ley 1/2003 CyL": {
        "referencia": "Ley 1/2003 CyL",
        "nombre_corto": "Ley Igualdad Castilla y León",
        "nombre_completo": "Ley 1/2003, de 3 de marzo, de Igualdad de Oportunidades entre Mujeres y Hombres en Castilla y León",
        "url_boe": "https://www.boe.es/buscar/doc.php?id=BOE-A-2003-6306"
    },
}


def get_or_create_law(referencia):
    """Get existing law or create new one."""
    # Try to get by referencia
    try:
        encoded_ref = quote(referencia, safe='')
        resp = requests.get(f"{API_BASE}/legislacion/by-referencia/{encoded_ref}")
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    
    # Create if not exists and we have definition
    if referencia in LAWS_TO_CREATE:
        resp = requests.post(f"{API_BASE}/legislacion/", json=LAWS_TO_CREATE[referencia])
        if resp.status_code == 201:
            print(f"  ✓ Created: {referencia}")
            return resp.json()
        else:
            print(f"  ✗ Failed to create {referencia}: {resp.text[:100]}")
    
    return None


def main():
    print("Processing TCAE del SACYL...")
    print("="*60)
    
    # Get temas
    resp = requests.get(f"{API_BASE}/temario/?oposicion_id={OPOSICION_ID}&limit=100")
    resp.raise_for_status()
    temas = resp.json()
    print(f"Found {len(temas)} temas\n")
    
    laws_linked = []
    laws_created = set()
    
    for tema in temas:
        titulo = tema["titulo"]
        laws = extract_laws_sacyl(titulo)
        
        if laws:
            print(f"Tema {tema['num_tema']}: {titulo[:70]}...")
            print(f"  Laws: {laws}")
            
            # Ensure laws exist
            for ref in laws:
                ley = get_or_create_law(ref)
                if ley and ref in LAWS_TO_CREATE:
                    laws_created.add(ref)
                laws_linked.append(ref)
            
            # Update tema
            resp = requests.patch(f"{API_BASE}/temario/{tema['id']}", json={"leyes_vinculadas": laws})
            if resp.status_code == 200:
                print(f"  ✓ Updated tema {tema['num_tema']}")
            else:
                print(f"  ✗ Failed to update tema: {resp.text[:100]}")
    
    # Mark oposicion as leyes_ok
    resp = requests.patch(f"{API_BASE}/oposiciones/{OPOSICION_ID}", json={
        "pipeline_state": "leyes_ok",
        "agente_activo": None
    })
    resp.raise_for_status()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Temas with laws: {len([t for t in temas if extract_laws_sacyl(t['titulo'])])}/{len(temas)}")
    print(f"Unique laws linked: {len(set(laws_linked))}")
    print(f"New laws created: {len(laws_created)}")
    if laws_created:
        for law in laws_created:
            print(f"  - {law}")
    print("\n✓ TCAE del SACYL marked as leyes_ok")


if __name__ == "__main__":
    main()
