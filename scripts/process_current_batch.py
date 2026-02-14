#!/usr/bin/env python3
"""
Process 3 oposiciones from temario_ok to leyes_ok.
Maps laws to topics, creates missing legislation records.
"""
import json
import re
import requests
from datetime import datetime

API_BASE = "http://localhost:8001"

# Law patterns to detect in tema titles
LAW_PATTERNS = [
    (r"Constituci[oó]n\s+Espa[ñn]ola(?:\s+de\s+1978)?", "CE 1978"),
    (r"Ley\s+Org[aá]nica\s+(\d+)/(\d+)", lambda m: f"LO {m.group(1)}/{m.group(2)}"),
    (r"LO\s+(\d+)/(\d+)", lambda m: f"LO {m.group(1)}/{m.group(2)}"),
    (r"Ley\s+(\d+)/(\d+)", lambda m: f"Ley {m.group(1)}/{m.group(2)}"),
    (r"Real\s+Decreto\s+Legislativo\s+(\d+)/(\d+)", lambda m: f"RDL {m.group(1)}/{m.group(2)}"),
    (r"RDL\s+(\d+)/(\d+)", lambda m: f"RDL {m.group(1)}/{m.group(2)}"),
    (r"Real\s+Decreto\s+(\d+)/(\d+)", lambda m: f"RD {m.group(1)}/{m.group(2)}"),
    (r"RD\s+(\d+)/(\d+)", lambda m: f"RD {m.group(1)}/{m.group(2)}"),
    (r"Decreto\s+(\d+)/(\d+)", lambda m: f"Decreto {m.group(1)}/{m.group(2)}"),
    (r"Reglamento\s+\(UE\)\s+(\d+)/(\d+)", lambda m: f"Reglamento UE {m.group(1)}/{m.group(2)}"),
    (r"Reglamento\s+General\s+de\s+Proteccion\s+de\s+Datos", "RGPD 2016/679"),
    (r"RGPD", "RGPD 2016/679"),
    (r"Estatuto\s+de\s+Autonom[ií]a\s+de\s+Castilla\s+y\s+Le[oó]n", "LO 14/2007 CyL"),
    (r"Estatuto\s+de\s+Autonom[ií]a\s+de\s+Catalu[nñ]a", "LO 6/2006 Cat"),
    (r"Estatuto\s+de\s+Autonom[ií]a\s+de\s+(?:la\s+)?(?:Comunidad\s+de\s+)?Madrid", "LO 3/1983 CM"),
]

# Known laws with their BOE URLs (for creating missing records)
KNOWN_LAWS = {
    "CE 1978": {
        "nombre_corto": "Constitución Española",
        "nombre_completo": "Constitución Española de 27 de diciembre de 1978",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229"
    },
    "LO 14/2007 CyL": {
        "nombre_corto": "Estatuto Autonomía Castilla y León",
        "nombre_completo": "Ley Orgánica 14/2007, de 30 de noviembre, de reforma del Estatuto de Autonomía de Castilla y León",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2007-20635"
    },
    "Ley 8/2010 CyL": {
        "nombre_corto": "Ley Ordenación Sistema Salud CyL",
        "nombre_completo": "Ley 8/2010, de 30 de agosto, de Ordenación del Sistema de Salud de Castilla y León",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2010-15237"
    },
    "Ley 1/2003 CyL": {
        "nombre_corto": "Ley Igualdad Castilla y León",
        "nombre_completo": "Ley 1/2003, de 3 de marzo, de Igualdad de Oportunidades entre Mujeres y Hombres en Castilla y León",
        "url_boe": "https://www.boe.es/buscar/doc.php?id=BOE-A-2003-6306"
    },
    "LO 6/2006 Cat": {
        "nombre_corto": "Estatuto Autonomía Catalunya",
        "nombre_completo": "Ley Orgánica 6/2006, de 19 de julio, de reforma del Estatuto de Autonomía de Cataluña",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2006-13087"
    },
    "LO 3/1983 CM": {
        "nombre_corto": "Estatuto Autonomía Madrid",
        "nombre_completo": "Ley Orgánica 3/1983, de 25 de febrero, de Estatuto de Autonomía de la Comunidad de Madrid",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-1983-6317"
    },
    "Ley 14/1986": {
        "nombre_corto": "Ley General de Sanidad",
        "nombre_completo": "Ley 14/1986, de 25 de abril, General de Sanidad",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-1986-10499"
    },
    "Ley 16/2003": {
        "nombre_corto": "Ley de Cohesión y Calidad del SNS",
        "nombre_completo": "Ley 16/2003, de 28 de mayo, de cohesión y calidad del Sistema Nacional de Salud",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2003-10715"
    },
    "Ley 55/2003": {
        "nombre_corto": "Estatuto Marco",
        "nombre_completo": "Ley 55/2003, de 16 de diciembre, del Estatuto Marco del personal estatutario de los servicios de salud",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2003-23101"
    },
    "Ley 41/2002": {
        "nombre_corto": "Ley de Autonomía del Paciente",
        "nombre_completo": "Ley 41/2002, de 14 de noviembre, básica reguladora de la autonomía del paciente y de derechos y obligaciones en materia de información y documentación clínica",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2002-22188"
    },
    "Ley 31/1995": {
        "nombre_corto": "LPRL",
        "nombre_completo": "Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-1995-24292"
    },
    "LO 3/2018": {
        "nombre_corto": "LOPDGDD",
        "nombre_completo": "Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673"
    },
    "RGPD 2016/679": {
        "nombre_corto": "RGPD",
        "nombre_completo": "Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, relativo a la protección de datos personales",
        "url_boe": "https://www.boe.es/buscar/doc.php?id=DOUE-L-2016-80807"
    },
    "LO 3/2007": {
        "nombre_corto": "LO Igualdad",
        "nombre_completo": "Ley Orgánica 3/2007, de 22 de marzo, para la igualdad efectiva de mujeres y hombres",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2007-6115"
    },
    "LO 1/2004": {
        "nombre_corto": "LO Violencia de Género",
        "nombre_completo": "Ley Orgánica 1/2004, de 28 de diciembre, de Medidas de Protección Integral contra la Violencia de Género",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2004-21760"
    },
}


def get_existing_legislation():
    """Fetch all existing legislation records."""
    all_legs = []
    skip = 0
    limit = 200
    while True:
        resp = requests.get(f"{API_BASE}/legislacion/?limit={limit}&skip={skip}")
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        all_legs.extend(batch)
        if len(batch) < limit:
            break
        skip += limit
    return {ley["referencia"]: ley for ley in all_legs}


def extract_laws_from_titulo(titulo):
    """Extract law references from a tema title."""
    laws = set()
    titulo_normalized = titulo.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
    
    for pattern, result in LAW_PATTERNS:
        for match in re.finditer(pattern, titulo_normalized, re.IGNORECASE):
            if callable(result):
                laws.add(result(match))
            else:
                laws.add(result)
    
    return list(laws)


def create_legislation(referencia, existing_legislation):
    """Create a new legislation record if it doesn't exist."""
    if referencia in existing_legislation:
        return existing_legislation[referencia]
    
    # Check known laws
    if referencia in KNOWN_LAWS:
        data = {"referencia": referencia, **KNOWN_LAWS[referencia]}
    else:
        # Create minimal record
        data = {"referencia": referencia}
    
    resp = requests.post(f"{API_BASE}/legislacion/", json=data)
    if resp.status_code == 201:
        ley = resp.json()
        existing_legislation[referencia] = ley
        print(f"  ✓ Created: {referencia}")
        return ley
    elif resp.status_code == 422 or "already exists" in resp.text.lower():
        # Already exists, fetch it
        resp2 = requests.get(f"{API_BASE}/legislacion/by-referencia/{referencia}")
        if resp2.status_code == 200:
            ley = resp2.json()
            existing_legislation[referencia] = ley
            return ley
    print(f"  ✗ Failed to create: {referencia} - {resp.text}")
    return None


def increment_legislation_count(referencia):
    """Increment the reference count for a legislation record."""
    try:
        resp = requests.patch(f"{API_BASE}/legislacion/by-referencia/{referencia}/increment")
        resp.raise_for_status()
    except Exception as e:
        print(f"  Warning: Could not increment count for {referencia}: {e}")


def update_tema_leyes(tema_id, leyes_vinculadas):
    """Update a tema with linked laws."""
    resp = requests.patch(f"{API_BASE}/temario/{tema_id}", json={"leyes_vinculadas": leyes_vinculadas})
    resp.raise_for_status()
    return resp.json()


def process_oposicion(oposicion, existing_legislation):
    """Process a single oposicion: analyze temas and link laws."""
    opo_id = oposicion["id"]
    opo_name = oposicion["nombre"]
    print(f"\n{'='*60}")
    print(f"Processing: {opo_name}")
    print(f"ID: {opo_id}")
    print(f"{'='*60}")
    
    # Get temas
    resp = requests.get(f"{API_BASE}/temario/?oposicion_id={opo_id}&limit=200")
    resp.raise_for_status()
    temas = resp.json()
    
    print(f"Found {len(temas)} temas")
    
    temas_with_laws = 0
    laws_linked = []
    new_laws_created = []
    
    for tema in temas:
        titulo = tema["titulo"]
        laws = extract_laws_from_titulo(titulo)
        
        if laws:
            temas_with_laws += 1
            print(f"\nTema {tema['num_tema']}: {titulo[:80]}...")
            print(f"  Laws found: {laws}")
            
            # Ensure all laws exist
            for law_ref in laws:
                if law_ref not in existing_legislation:
                    ley = create_legislation(law_ref, existing_legislation)
                    if ley:
                        new_laws_created.append(law_ref)
                increment_legislation_count(law_ref)
                laws_linked.append(law_ref)
            
            # Update tema with leyes_vinculadas
            update_tema_leyes(tema["id"], laws)
    
    print(f"\nSummary for {opo_name}:")
    print(f"  - Temas with laws: {temas_with_laws}/{len(temas)}")
    print(f"  - Unique laws linked: {len(set(laws_linked))}")
    print(f"  - New laws created: {len(new_laws_created)}")
    
    # Mark as leyes_ok
    resp = requests.patch(f"{API_BASE}/oposiciones/{opo_id}", json={
        "pipeline_state": "leyes_ok",
        "agente_activo": None
    })
    resp.raise_for_status()
    print(f"  ✓ Pipeline state updated to leyes_ok")
    
    return {
        "nombre": opo_name,
        "temas_total": len(temas),
        "temas_with_laws": temas_with_laws,
        "unique_laws": len(set(laws_linked)),
        "new_laws": new_laws_created
    }


def main():
    print("="*60)
    print("Decodificador Run - Map Laws to Topics")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Load existing legislation
    print("\nLoading existing legislation...")
    existing_legislation = get_existing_legislation()
    print(f"Found {len(existing_legislation)} existing legislation records")
    
    # Get oposiciones in temario_ok state
    resp = requests.get(f"{API_BASE}/oposiciones/?pipeline_state=temario_ok&limit=3")
    resp.raise_for_status()
    oposiciones = resp.json()
    
    if not oposiciones:
        print("\nNo oposiciones in temario_ok state. Nothing to process.")
        return
    
    print(f"\nFound {len(oposiciones)} oposiciones to process:")
    for opo in oposiciones:
        print(f"  - {opo['nombre']} ({opo['grupo']} - {opo['ambito']})")
    
    # Process each oposicion
    results = []
    for opo in oposiciones:
        # Claim the oposicion
        resp = requests.patch(f"{API_BASE}/oposiciones/{opo['id']}", json={
            "pipeline_state": "decodificando_leyes",
            "agente_activo": "decodificador"
        })
        resp.raise_for_status()
        
        result = process_oposicion(opo, existing_legislation)
        results.append(result)
    
    # Print final summary
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    
    total_temas = sum(r["temas_total"] for r in results)
    total_with_laws = sum(r["temas_with_laws"] for r in results)
    all_new_laws = []
    for r in results:
        all_new_laws.extend(r["new_laws"])
    
    print(f"Oposiciones processed: {len(results)}")
    print(f"Total temas analyzed: {total_temas}")
    print(f"Temas with laws: {total_with_laws}")
    print(f"New legislation records created: {len(all_new_laws)}")
    
    if all_new_laws:
        print("\nNew laws created:")
        for law in all_new_laws:
            print(f"  - {law}")
    
    print("\nAll oposiciones marked as leyes_ok ✓")


if __name__ == "__main__":
    main()
