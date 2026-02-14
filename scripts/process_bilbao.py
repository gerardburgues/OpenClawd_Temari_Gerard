#!/usr/bin/env python3
"""Process Policía Local Bilbao - map laws to temas"""
import requests
import re

API = "http://localhost:8001"
OPOS_ID = "ceeaa95a-4e1f-40f1-9166-f86dd78c028b"

# Mapping of extracted references to standard references
LAW_MAPPINGS = {
    'CE 1978': {'ref': 'CE 1978', 'nombre': 'Constitución Española', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229'},
    'EAPV': {'ref': 'LO 3/1979', 'nombre': 'Estatuto de Autonomía del País Vasco', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1979-30177'},
    'LO 2/1986': {'ref': 'LO 2/1986', 'nombre': 'Ley Orgánica de Fuerzas y Cuerpos de Seguridad', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1986-6859'},
    'Ley 4/1992': {'ref': 'Ley 4/1992', 'nombre': 'Ley de Policía del País Vasco', 'boe': 'https://www.boe.es/buscar/doc.php?id=BOE-A-1992-23496'},
    'LO 4/2015': {'ref': 'LO 4/2015', 'nombre': 'Ley de Protección de la Seguridad Ciudadana', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-3442'},
    'LO 10/1995': {'ref': 'LO 10/1995', 'nombre': 'Código Penal', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444'},
    'RDL 6/2015': {'ref': 'RDL 6/2015', 'nombre': 'Ley de Tráfico, Circulación y Seguridad Vial', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11722'},
    'Ley 39/2015': {'ref': 'Ley 39/2015', 'nombre': 'Ley del Procedimiento Administrativo Común', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565'},
    'LO 3/2018': {'ref': 'LO 3/2018', 'nombre': 'Ley de Protección de Datos Personales', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673'},
    'LO 3/2007': {'ref': 'LO 3/2007', 'nombre': 'Ley para la Igualdad Efectiva de Mujeres y Hombres', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2007-6115'},
    'LO 1/2004': {'ref': 'LO 1/2004', 'nombre': 'Ley de Medidas de Protección Integral contra la Violencia de Género', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2004-21760'},
    'Ley 7/1985': {'ref': 'Ley 7/1985', 'nombre': 'Ley Reguladora de las Bases del Régimen Local', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1985-5392'},
    'RGC': {'ref': 'RGC', 'nombre': 'Reglamento General de Circulación', 'boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2003-23514'},
}

# Manual mapping for each tema based on analysis
TEMA_LAWS = {
    1: ['CE 1978'],
    2: ['CE 1978'],
    3: ['CE 1978'],
    4: ['CE 1978'],
    5: ['LO 3/1979'],  # Estatuto Autonomía País Vasco
    6: ['LO 3/1979'],
    7: ['LO 3/1979'],
    8: ['Ley 7/1985'],
    9: ['Ley 7/1985'],
    10: ['RDL 5/2015'],  # TREBEP
    11: ['LO 2/1986'],
    12: ['Ley 4/1992'],
    13: ['LO 4/2015'],
    14: ['LO 10/1995', 'LECrim'],
    15: ['LO 10/1995'],
    16: ['LO 10/1995'],
    17: ['LO 10/1995'],
    18: ['LO 10/1995'],
    19: ['RDL 6/2015'],
    20: ['RGC'],
    21: ['RGC', 'RDL 6/2015'],
    22: ['RDL 6/2015', 'LECrim'],
    23: ['Ley 39/2015'],
    24: ['LO 3/2018', 'RGPD 2016/679'],
    25: ['LO 3/2007', 'LO 1/2004'],
}

def ensure_law_exists(ref):
    """Ensure law exists in legislacion table"""
    r = requests.get(f"{API}/legislacion/by-referencia/{ref}")
    if r.status_code == 200:
        # Increment reference count
        requests.patch(f"{API}/legislacion/by-referencia/{ref}/increment")
        return True
    return False

def update_tema(tema_id, laws):
    """Update tema with leyes_vinculadas"""
    r = requests.patch(
        f"{API}/temario/{tema_id}",
        json={'leyes_vinculadas': laws}
    )
    return r.status_code == 200

def main():
    # Get temas
    r = requests.get(f"{API}/temario/?oposicion_id={OPOS_ID}&limit=100")
    temas = r.json()
    
    print("=" * 60)
    print("POLICÍA LOCAL BILBAO - Mapping Laws")
    print("=" * 60)
    
    updated = 0
    all_laws = set()
    
    for tema in temas:
        num = tema['num_tema']
        tema_id = tema['id']
        
        if num in TEMA_LAWS:
            laws = TEMA_LAWS[num]
            
            # Ensure all laws exist
            for ref in laws:
                ensure_law_exists(ref)
                all_laws.add(ref)
            
            # Update tema
            if update_tema(tema_id, laws):
                print(f"✓ Tema {num}: {', '.join(laws)}")
                updated += 1
    
    print(f"\nTotal: {updated} temas updated")
    print(f"Unique laws: {', '.join(sorted(all_laws))}")
    
    # Mark as leyes_ok
    r = requests.patch(
        f"{API}/oposiciones/{OPOS_ID}",
        json={'pipeline_state': 'leyes_ok', 'agente_activo': None}
    )
    if r.status_code == 200:
        print("✓ Marked as leyes_ok")
    
if __name__ == '__main__':
    main()
