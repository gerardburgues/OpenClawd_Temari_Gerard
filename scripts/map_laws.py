#!/usr/bin/env python3
"""
Decodificador: Map laws to temario topics
"""
import re
import json
import requests
from datetime import datetime, timezone
from typing import Optional

API_BASE = "http://localhost:8001"

# Law patterns to extract from tema titles
LAW_PATTERNS = [
    # Constitución
    (r"Constitución Española(?:\s+de\s+1978)?", "CE 1978", "Constitución Española", "Constitución Española de 27 de diciembre de 1978", "BOE-A-1978-31229"),
    
    # Leyes Orgánicas
    (r"Ley\s+Orgánica\s+(\d+/\d{4})", "LO {}", "LO {}", None, None),
    (r"LO\s+(\d+/\d{4})", "LO {}", "LO {}", None, None),
    
    # Leyes ordinarias
    (r"Ley\s+(\d+/\d{4})", "Ley {}", "Ley {}", None, None),
    
    # Reales Decretos
    (r"Real\s+Decreto\s+(?:Legislativo\s+)?(\d+/\d{4})", "RD {}", "RD {}", None, None),
    (r"RD\s+(\d+/\d{4})", "RD {}", "RD {}", None, None),
    (r"RDL\s+(\d+/\d{4})", "RDL {}", "RDL {}", None, None),
    
    # Órdenes
    (r"Orden\s+(\w+/\d+/\d{4})", "Orden {}", "Orden {}", None, None),
    
    # Estatutos de Autonomía
    (r"Estatuto\s+de\s+Autonomía\s+(?:de\s+la\s+)?(?:Comunitat\s+)?Valenciana?", "EACV", "Estatuto de Autonomía de la Comunitat Valenciana", "Ley Orgánica 5/1982, de 1 de julio, de Estatuto de Autonomía de la Comunidad Valenciana (actualizada por LO 1/2006)", "BOE-A-2006-13087"),
    (r"Estatuto\s+de\s+Autonomía\s+del\s+País\s+Vasco", "EAPV", "Estatuto de Autonomía del País Vasco", "Ley Orgánica 3/1979, de 18 de diciembre, de Estatuto de Autonomía para el País Vasco", "BOE-A-1979-30177"),
    
    # Reglamentos específicos
    (r"Reglamento\s+General\s+de\s+Circulación", "RGC", "Reglamento General de Circulación", "Real Decreto 1428/2003, de 21 de noviembre, por el que se aprueba el Reglamento General de Circulación", "BOE-A-2003-23514"),
    (r"Reglamento\s+General\s+de\s+Conductores", "RGCond", "Reglamento General de Conductores", "Real Decreto 818/2009, de 8 de mayo, por el que se aprueba el Reglamento General de Conductores", "BOE-A-2009-9481"),
    (r"Reglamento\s+General\s+de\s+Vehículos", "RGV", "Reglamento General de Vehículos", "Real Decreto 2822/1998, de 23 de diciembre, por el que se aprueba el Reglamento General de Vehículos", "BOE-A-1999-1826"),
    
    # Código Penal
    (r"Código\s+Penal", "CP", "Código Penal", "Ley Orgánica 10/1995, de 23 de noviembre, del Código Penal", "BOE-A-1995-25444"),
    
    # LECrim
    (r"Ley\s+de\s+Enjuiciamiento\s+Criminal", "LECrim", "Ley de Enjuiciamiento Criminal", "Real decreto de 14 de septiembre de 1882 por el que se aprueba la Ley de Enjuiciamiento Criminal", "BOE-A-1882-6036"),
    
    # TREBEP
    (r"(?:TREBEP|Estatuto\s+Básico\s+del\s+Empleado\s+Público)", "TREBEP", "Estatuto Básico del Empleado Público", "Real Decreto Legislativo 5/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley del Estatuto Básico del Empleado Público", "BOE-A-2015-11719"),
]

# Known laws with full details
KNOWN_LAWS = {
    "LO 2/1986": ("Ley de Fuerzas y Cuerpos de Seguridad", "Ley Orgánica 2/1986, de 13 de marzo, de Fuerzas y Cuerpos de Seguridad", "BOE-A-1986-6859"),
    "LO 4/2015": ("Ley de Seguridad Ciudadana", "Ley Orgánica 4/2015, de 30 de marzo, de protección de la seguridad ciudadana", "BOE-A-2015-3442"),
    "LO 1/2004": ("Ley de Violencia de Género", "Ley Orgánica 1/2004, de 28 de diciembre, de Medidas de Protección Integral contra la Violencia de Género", "BOE-A-2004-21760"),
    "LO 3/2007": ("Ley de Igualdad", "Ley Orgánica 3/2007, de 22 de marzo, para la igualdad efectiva de mujeres y hombres", "BOE-A-2007-6115"),
    "LO 5/2000": ("LORPM", "Ley Orgánica 5/2000, de 12 de enero, reguladora de la responsabilidad penal de los menores", "BOE-A-2000-641"),
    "LO 3/2018": ("LOPDGDD", "Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales", "BOE-A-2018-16673"),
    "LO 4/2000": ("Ley de Extranjería", "Ley Orgánica 4/2000, de 11 de enero, sobre derechos y libertades de los extranjeros en España", "BOE-A-2000-544"),
    "LO 8/2021": ("LOPIVI", "Ley Orgánica 8/2021, de 4 de junio, de protección integral a la infancia y la adolescencia frente a la violencia", "BOE-A-2021-9347"),
    "Ley 39/2015": ("LPACAP", "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas", "BOE-A-2015-10565"),
    "Ley 40/2015": ("LRJSP", "Ley 40/2015, de 1 de octubre, de Régimen Jurídico del Sector Público", "BOE-A-2015-10566"),
    "Ley 17/2015": ("Ley de Protección Civil", "Ley 17/2015, de 9 de julio, del Sistema Nacional de Protección Civil", "BOE-A-2015-7730"),
    "Ley 17/2017": ("Ley Policías Locales CV", "Ley 17/2017, de 13 de diciembre, de coordinación de Policías Locales de la Comunitat Valenciana", "BOE-A-2018-893"),
    "Ley 15/2012": ("Ley Seguridad Euskadi", "Ley 15/2012, de 28 de junio, de Ordenación del Sistema de Seguridad Pública de Euskadi", "BOE-A-2012-12501"),
    "Ley 4/2005": ("Ley Igualdad Euskadi", "Ley 4/2005, de 18 de febrero, para la Igualdad de Mujeres y Hombres", None),
    "Ley 10/1982": ("Ley Euskera", "Ley 10/1982, de 24 de noviembre, básica de normalización del uso del Euskera", None),
    "RDL 6/2015": ("Ley de Tráfico", "Real Decreto Legislativo 6/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley sobre Tráfico, Circulación de Vehículos a Motor y Seguridad Vial", "BOE-A-2015-11722"),
    "RD 5/2015": ("TREBEP", "Real Decreto Legislativo 5/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley del Estatuto Básico del Empleado Público", "BOE-A-2015-11719"),
    "Reglamento UE 2016/679": ("RGPD", "Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016, relativo a la protección de las personas físicas en lo que respecta al tratamiento de datos personales", None),
    "Orden FOM/2872/2010": ("Títulos Habilitantes Ferroviarios", "Orden FOM/2872/2010, de 5 de noviembre, por la que se determinan las condiciones para la obtención de los títulos habilitantes que permiten el ejercicio de las funciones del personal ferroviario", "BOE-A-2010-17037"),
    "RD 929/2020": ("Seguridad Operacional Ferroviaria", "Real Decreto 929/2020, de 27 de octubre, sobre seguridad operacional e interoperabilidad ferroviarias", "BOE-A-2020-13297"),
}

def extract_laws_from_title(titulo: str) -> list[dict]:
    """Extract law references from a tema title"""
    laws = []
    titulo_upper = titulo.upper()
    
    # Check for Constitution
    if "CONSTITUCIÓN" in titulo_upper:
        laws.append({
            "referencia": "CE 1978",
            "nombre_corto": "Constitución Española",
            "nombre_completo": "Constitución Española de 27 de diciembre de 1978",
            "boe_id": "BOE-A-1978-31229"
        })
    
    # Check for specific LO patterns with numbers
    lo_matches = re.findall(r"Ley\s+Orgánica\s+(\d+)/(\d{4})", titulo, re.IGNORECASE)
    for num, year in lo_matches:
        ref = f"LO {num}/{year}"
        if ref in KNOWN_LAWS:
            nombre_corto, nombre_completo, boe_id = KNOWN_LAWS[ref]
            laws.append({"referencia": ref, "nombre_corto": nombre_corto, "nombre_completo": nombre_completo, "boe_id": boe_id})
        else:
            laws.append({"referencia": ref, "nombre_corto": ref, "nombre_completo": None, "boe_id": None})
    
    # Check for Ley patterns
    ley_matches = re.findall(r"(?<!Orgánica\s)Ley\s+(\d+)/(\d{4})", titulo, re.IGNORECASE)
    for num, year in ley_matches:
        ref = f"Ley {num}/{year}"
        if ref in KNOWN_LAWS:
            nombre_corto, nombre_completo, boe_id = KNOWN_LAWS[ref]
            laws.append({"referencia": ref, "nombre_corto": nombre_corto, "nombre_completo": nombre_completo, "boe_id": boe_id})
        else:
            laws.append({"referencia": ref, "nombre_corto": ref, "nombre_completo": None, "boe_id": None})
    
    # Check for RDL patterns
    rdl_matches = re.findall(r"Real\s+Decreto\s+Legislativo\s+(\d+)/(\d{4})", titulo, re.IGNORECASE)
    for num, year in rdl_matches:
        ref = f"RDL {num}/{year}"
        if ref in KNOWN_LAWS:
            nombre_corto, nombre_completo, boe_id = KNOWN_LAWS[ref]
            laws.append({"referencia": ref, "nombre_corto": nombre_corto, "nombre_completo": nombre_completo, "boe_id": boe_id})
        else:
            laws.append({"referencia": ref, "nombre_corto": ref, "nombre_completo": None, "boe_id": None})
    
    # Check for RD patterns (but not RDL)
    rd_matches = re.findall(r"(?:Real\s+Decreto|RD)\s+(\d+)/(\d{4})(?!\s*,\s*texto\s+refundido)", titulo, re.IGNORECASE)
    for num, year in rd_matches:
        ref = f"RD {num}/{year}"
        if ref in KNOWN_LAWS:
            nombre_corto, nombre_completo, boe_id = KNOWN_LAWS[ref]
            laws.append({"referencia": ref, "nombre_corto": nombre_corto, "nombre_completo": nombre_completo, "boe_id": boe_id})
        else:
            laws.append({"referencia": ref, "nombre_corto": ref, "nombre_completo": None, "boe_id": None})
    
    # Check for Orden patterns
    orden_matches = re.findall(r"Orden\s+(\w+/\d+/\d{4})", titulo, re.IGNORECASE)
    for orden_ref in orden_matches:
        ref = f"Orden {orden_ref}"
        if ref in KNOWN_LAWS:
            nombre_corto, nombre_completo, boe_id = KNOWN_LAWS[ref]
            laws.append({"referencia": ref, "nombre_corto": nombre_corto, "nombre_completo": nombre_completo, "boe_id": boe_id})
        else:
            laws.append({"referencia": ref, "nombre_corto": ref, "nombre_completo": None, "boe_id": None})
    
    # Check for Reglamento UE
    if "REGLAMENTO" in titulo_upper and "2016/679" in titulo:
        laws.append({
            "referencia": "Reglamento UE 2016/679",
            "nombre_corto": "RGPD",
            "nombre_completo": "Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016, relativo a la protección de las personas físicas en lo que respecta al tratamiento de datos personales",
            "boe_id": None
        })
    
    # Check for specific reglamentos by name
    if "REGLAMENTO GENERAL DE CIRCULACIÓN" in titulo_upper:
        laws.append({
            "referencia": "RGC",
            "nombre_corto": "Reglamento General de Circulación",
            "nombre_completo": "Real Decreto 1428/2003, de 21 de noviembre, por el que se aprueba el Reglamento General de Circulación",
            "boe_id": "BOE-A-2003-23514"
        })
    
    if "REGLAMENTO GENERAL DE CONDUCTORES" in titulo_upper:
        laws.append({
            "referencia": "RGCond",
            "nombre_corto": "Reglamento General de Conductores",
            "nombre_completo": "Real Decreto 818/2009, de 8 de mayo, por el que se aprueba el Reglamento General de Conductores",
            "boe_id": "BOE-A-2009-9481"
        })
    
    if "REGLAMENTO GENERAL DE VEHÍCULOS" in titulo_upper:
        laws.append({
            "referencia": "RGV",
            "nombre_corto": "Reglamento General de Vehículos",
            "nombre_completo": "Real Decreto 2822/1998, de 23 de diciembre, por el que se aprueba el Reglamento General de Vehículos",
            "boe_id": "BOE-A-1999-1826"
        })
    
    # Check for Código Penal
    if "CÓDIGO PENAL" in titulo_upper:
        laws.append({
            "referencia": "CP",
            "nombre_corto": "Código Penal",
            "nombre_completo": "Ley Orgánica 10/1995, de 23 de noviembre, del Código Penal",
            "boe_id": "BOE-A-1995-25444"
        })
    
    # Check for LECrim
    if "LEY DE ENJUICIAMIENTO CRIMINAL" in titulo_upper or "LECRIM" in titulo_upper:
        laws.append({
            "referencia": "LECrim",
            "nombre_corto": "Ley de Enjuiciamiento Criminal",
            "nombre_completo": "Real decreto de 14 de septiembre de 1882 por el que se aprueba la Ley de Enjuiciamiento Criminal",
            "boe_id": "BOE-A-1882-6036"
        })
    
    # Check for TREBEP
    if "TREBEP" in titulo_upper or "ESTATUTO BÁSICO DEL EMPLEADO PÚBLICO" in titulo_upper:
        laws.append({
            "referencia": "TREBEP",
            "nombre_corto": "Estatuto Básico del Empleado Público",
            "nombre_completo": "Real Decreto Legislativo 5/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley del Estatuto Básico del Empleado Público",
            "boe_id": "BOE-A-2015-11719"
        })
    
    # Check for Estatutos de Autonomía
    if "ESTATUTO DE AUTONOMÍA" in titulo_upper:
        if "VALENCIAN" in titulo_upper or "COMUNITAT" in titulo_upper:
            laws.append({
                "referencia": "EACV",
                "nombre_corto": "Estatuto de Autonomía de la Comunitat Valenciana",
                "nombre_completo": "Ley Orgánica 5/1982, de 1 de julio, de Estatuto de Autonomía de la Comunidad Valenciana (actualizada por LO 1/2006)",
                "boe_id": "BOE-A-2006-13087"
            })
        elif "PAÍS VASCO" in titulo_upper or "EUSKADI" in titulo_upper:
            laws.append({
                "referencia": "EAPV",
                "nombre_corto": "Estatuto de Autonomía del País Vasco",
                "nombre_completo": "Ley Orgánica 3/1979, de 18 de diciembre, de Estatuto de Autonomía para el País Vasco",
                "boe_id": "BOE-A-1979-30177"
            })
    
    # Deduplicate by referencia
    seen = set()
    unique_laws = []
    for law in laws:
        if law["referencia"] not in seen:
            seen.add(law["referencia"])
            unique_laws.append(law)
    
    return unique_laws


def get_or_create_legislation(law_data: dict) -> str:
    """Get existing legislation record or create new one, return referencia"""
    from urllib.parse import quote
    
    ref = law_data["referencia"]
    encoded_ref = quote(ref, safe='')
    
    # Try to get existing
    resp = requests.get(f"{API_BASE}/legislacion/by-referencia/{encoded_ref}")
    if resp.status_code == 200:
        # Increment reference count
        requests.patch(f"{API_BASE}/legislacion/by-referencia/{encoded_ref}/increment")
        return ref
    
    # Create new
    url_boe = None
    if law_data.get("boe_id"):
        url_boe = f"https://www.boe.es/buscar/act.php?id={law_data['boe_id']}"
    
    payload = {
        "referencia": ref,
        "nombre_corto": law_data.get("nombre_corto"),
        "nombre_completo": law_data.get("nombre_completo"),
        "url_boe": url_boe,
        "veces_referenciada": 1
    }
    
    resp = requests.post(f"{API_BASE}/legislacion/", json=payload)
    if resp.status_code in (200, 201):
        print(f"    ✓ Created legislation: {ref}")
    elif "duplicate" in resp.text.lower() or resp.status_code == 500:
        # Already exists, try to increment
        requests.patch(f"{API_BASE}/legislacion/by-referencia/{encoded_ref}/increment")
        print(f"    ~ Existing legislation: {ref}")
    else:
        print(f"    ✗ Failed to create {ref}: {resp.text}")
    
    return ref


def update_tema_laws(tema_id: str, leyes: list[str]):
    """Update a tema with linked laws"""
    resp = requests.patch(
        f"{API_BASE}/temario/{tema_id}",
        json={"leyes_vinculadas": leyes}
    )
    return resp.status_code in (200, 201)


def process_oposicion(oposicion_id: str, nombre: str):
    """Process all temas for an oposicion"""
    print(f"\n{'='*60}")
    print(f"Processing: {nombre}")
    print(f"{'='*60}")
    
    # Get temas
    resp = requests.get(f"{API_BASE}/temario/", params={"oposicion_id": oposicion_id})
    if resp.status_code != 200:
        print(f"ERROR: Could not fetch temas: {resp.text}")
        return False
    
    temas = resp.json()
    print(f"Found {len(temas)} temas")
    
    total_laws_linked = 0
    
    for tema in temas:
        titulo = tema["titulo"]
        tema_id = tema["id"]
        num = tema["num_tema"]
        
        # Skip if already has laws linked
        if tema.get("leyes_vinculadas") and len(tema["leyes_vinculadas"]) > 0:
            print(f"  Tema {num}: Already has {len(tema['leyes_vinculadas'])} laws linked")
            continue
        
        # Extract laws from title
        laws = extract_laws_from_title(titulo)
        
        if not laws:
            print(f"  Tema {num}: No laws identified")
            continue
        
        print(f"  Tema {num}: Found {len(laws)} law(s): {[l['referencia'] for l in laws]}")
        
        # Create/get legislation records
        law_refs = []
        for law_data in laws:
            ref = get_or_create_legislation(law_data)
            law_refs.append(ref)
        
        # Update tema
        if update_tema_laws(tema_id, law_refs):
            total_laws_linked += len(law_refs)
        else:
            print(f"    ✗ Failed to update tema {num}")
    
    print(f"\nTotal laws linked for {nombre}: {total_laws_linked}")
    
    # Mark oposicion as leyes_ok
    resp = requests.patch(
        f"{API_BASE}/oposiciones/{oposicion_id}",
        json={"pipeline_state": "leyes_ok", "agente_activo": None}
    )
    
    if resp.status_code in (200, 201):
        print(f"✓ Marked {nombre} as leyes_ok")
        return True
    else:
        print(f"✗ Failed to mark as leyes_ok: {resp.text}")
        return False


def main():
    # Oposiciones to process
    oposiciones = [
        ("68cbf631-db07-459d-a261-7969a253d64c", "Policía Local Valencia"),
        ("c49167dd-533d-4b1e-b2df-df526d405af5", "Policía Local Bilbao"),
        ("8ba90356-294e-4f4a-b4d2-66e4af810737", "Maquinista Renfe"),
    ]
    
    results = []
    for opos_id, nombre in oposiciones:
        success = process_oposicion(opos_id, nombre)
        results.append((nombre, success))
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for nombre, success in results:
        status = "✓" if success else "✗"
        print(f"  {status} {nombre}")


if __name__ == "__main__":
    main()
