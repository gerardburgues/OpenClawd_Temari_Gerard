#!/usr/bin/env python3
"""
Process 3 oposiciones: extract laws and update database
"""
import json
import re
import requests
from datetime import datetime

API = "http://localhost:8001"

# Law patterns to detect in tema titles
LAW_PATTERNS = [
    # Constitución
    (r'Constituci[óo]n\s+Espa[ñn]ola', 'CE 1978'),
    (r'CE\s+1978', 'CE 1978'),
    
    # Leyes orgánicas con número
    (r'Ley\s+Org[áa]nica\s+(\d+/\d{4})', lambda m: f'LO {m.group(1)}'),
    (r'L\.?O\.?\s+(\d+/\d{4})', lambda m: f'LO {m.group(1)}'),
    
    # Leyes con número  
    (r'Ley\s+(\d+/\d{4})', lambda m: f'Ley {m.group(1)}'),
    
    # Reales Decretos Legislativos
    (r'Real\s+Decreto\s+Legislativo\s+(\d+/\d{4})', lambda m: f'RDL {m.group(1)}'),
    (r'RDL\s+(\d+/\d{4})', lambda m: f'RDL {m.group(1)}'),
    
    # Reales Decretos
    (r'Real\s+Decreto\s+(\d+/\d{4})', lambda m: f'RD {m.group(1)}'),
    (r'RD\s+(\d+/\d{4})', lambda m: f'RD {m.group(1)}'),
    
    # Directivas europeas
    (r'Directiva\s+(\d+/\d+)', lambda m: f'Directiva {m.group(1)}'),
    
    # Reglamentos europeos
    (r'Reglamento\s+\(?UE\)?\s*(\d+/\d{4})', lambda m: f'Reglamento UE {m.group(1)}'),
    (r'RGPD', 'RGPD 2016/679'),
    
    # Known laws by name
    (r'Estatuto\s+B[áa]sico\s+del\s+Empleado\s+P[úu]blico', 'RDL 5/2015'),
    (r'TREBEP', 'RDL 5/2015'),
    (r'Procedimiento\s+Administrativo\s+Com[úu]n', 'Ley 39/2015'),
    (r'LPAC', 'Ley 39/2015'),
    (r'Protecci[óo]n\s+de\s+Datos\s+Personal', 'LO 3/2018'),
    (r'LOPDGDD', 'LO 3/2018'),
    (r'Bases\s+del\s+R[ée]gimen\s+Local', 'Ley 7/1985'),
    (r'LRBRL', 'Ley 7/1985'),
    (r'Contratos\s+del\s+Sector\s+P[úu]blico', 'Ley 9/2017'),
    (r'LCSP', 'Ley 9/2017'),
    (r'Prevenci[óo]n\s+de\s+Riesgos\s+Laborales', 'Ley 31/1995'),
    (r'igualdad\s+efectiva\s+de\s+mujeres\s+y\s+hombres', 'LO 3/2007'),
    (r'General\s+de\s+Sanidad', 'Ley 14/1986'),
    (r'Patrimonio\s+Hist[óo]rico\s+Espa[ñn]ol', 'Ley 16/1985'),
    (r'Energ[íi]a\s+Nuclear', 'Ley 25/1964'),
    (r'Biblioteca\s+Nacional\s+de\s+Espa[ñn]a', 'Ley 1/2015'),
    (r'lectura.*libro.*bibliotecas', 'Ley 10/2007'),
]

# Known laws database
KNOWN_LAWS = {
    'CE 1978': {
        'nombre_corto': 'Constitución Española',
        'nombre_completo': 'Constitución Española de 1978',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229'
    },
    'LO 3/2007': {
        'nombre_corto': 'Ley de Igualdad',
        'nombre_completo': 'Ley Orgánica 3/2007, de 22 de marzo, para la igualdad efectiva de mujeres y hombres',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2007-6115'
    },
    'LO 3/2018': {
        'nombre_corto': 'LOPDGDD',
        'nombre_completo': 'Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673'
    },
    'Ley 31/1995': {
        'nombre_corto': 'Ley PRL',
        'nombre_completo': 'Ley 31/1995, de 8 de noviembre, de prevención de Riesgos Laborales',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1995-24292'
    },
    'Ley 14/1986': {
        'nombre_corto': 'Ley General de Sanidad',
        'nombre_completo': 'Ley 14/1986, de 25 de abril, General de Sanidad',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1986-10499'
    },
    'Ley 16/1985': {
        'nombre_corto': 'Ley Patrimonio Histórico',
        'nombre_completo': 'Ley 16/1985, de 25 de junio, del Patrimonio Histórico Español',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1985-12534'
    },
    'Ley 10/2007': {
        'nombre_corto': 'Ley de la Lectura',
        'nombre_completo': 'Ley 10/2007, de 22 de junio, de la lectura, del libro y de las bibliotecas',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2007-12351'
    },
    'Ley 1/2015': {
        'nombre_corto': 'Ley BNE',
        'nombre_completo': 'Ley 1/2015, de 24 de marzo, reguladora de la Biblioteca Nacional de España',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-3248'
    },
    'Ley 25/1964': {
        'nombre_corto': 'Ley de Energía Nuclear',
        'nombre_completo': 'Ley 25/1964, de 29 de abril, sobre energía nuclear',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1964-7544'
    },
    'Ley 27/2006': {
        'nombre_corto': 'Ley Acceso Información Ambiental',
        'nombre_completo': 'Ley 27/2006, de 18 de julio, por la que se regulan los derechos de acceso a la información, de participación pública y de acceso a la justicia en materia de medio ambiente',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2006-13010'
    },
    'Ley 4/1994 Murcia': {
        'nombre_corto': 'Ley Salud Murcia',
        'nombre_completo': 'Ley 4/1994, de 26 de julio, de Salud de la Región de Murcia',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1994-21178'
    },
    'RDL 5/2015': {
        'nombre_corto': 'TREBEP',
        'nombre_completo': 'Real Decreto Legislativo 5/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley del Estatuto Básico del Empleado Público',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11719'
    },
    'Ley 39/2015': {
        'nombre_corto': 'LPAC',
        'nombre_completo': 'Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565'
    },
    'Ley 9/2017': {
        'nombre_corto': 'LCSP',
        'nombre_completo': 'Ley 9/2017, de 8 de noviembre, de Contratos del Sector Público',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902'
    },
    'Ley 40/2015': {
        'nombre_corto': 'LRJSP',
        'nombre_completo': 'Ley 40/2015, de 1 de octubre, de Régimen Jurídico del Sector Público',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-10566'
    },
    'Ley 38/2003': {
        'nombre_corto': 'Ley General de Subvenciones',
        'nombre_completo': 'Ley 38/2003, de 17 de noviembre, General de Subvenciones',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2003-20977'
    },
    'Ley 19/2013': {
        'nombre_corto': 'Ley Transparencia',
        'nombre_completo': 'Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887'
    },
    'RGPD 2016/679': {
        'nombre_corto': 'RGPD',
        'nombre_completo': 'Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016, relativo a la protección de las personas físicas en lo que respecta al tratamiento de datos personales',
        'url_boe': 'https://www.boe.es/doue/2016/119/L00001-00088.pdf'
    },
}


def extract_laws(titulo):
    """Extract law references from a tema title"""
    found = set()
    for pattern, result in LAW_PATTERNS:
        matches = re.finditer(pattern, titulo, re.IGNORECASE)
        for match in matches:
            if callable(result):
                ref = result(match)
            else:
                ref = result
            found.add(ref)
    return list(found)


def get_or_create_law(referencia):
    """Get existing law or create new one"""
    # Try to get existing
    r = requests.get(f"{API}/legislacion/by-referencia/{referencia}")
    if r.status_code == 200:
        # Increment reference count
        requests.patch(f"{API}/legislacion/by-referencia/{referencia}/increment")
        return True
    
    # Get info from known laws
    info = KNOWN_LAWS.get(referencia, {})
    
    # Create new
    data = {
        'referencia': referencia,
        'nombre_corto': info.get('nombre_corto', referencia),
        'nombre_completo': info.get('nombre_completo'),
        'url_boe': info.get('url_boe'),
        'veces_referenciada': 1
    }
    r = requests.post(f"{API}/legislacion/", json=data)
    if r.status_code == 201:
        print(f"  ✓ Created law: {referencia}")
        return True
    else:
        print(f"  ✗ Failed to create: {referencia} - {r.text}")
        return False


def update_tema_laws(tema_id, leyes_vinculadas):
    """Update a tema with its linked laws"""
    r = requests.patch(
        f"{API}/temario/{tema_id}",
        json={'leyes_vinculadas': leyes_vinculadas}
    )
    return r.status_code == 200


def process_oposicion(opos_id, nombre):
    """Process one oposicion"""
    print(f"\n{'='*60}")
    print(f"Processing: {nombre}")
    print('='*60)
    
    # Get temas
    r = requests.get(f"{API}/temario/?oposicion_id={opos_id}&limit=500")
    temas = r.json()
    
    total_laws = 0
    temas_with_laws = 0
    all_laws = set()
    
    for tema in temas:
        titulo = tema['titulo']
        tema_id = tema['id']
        num = tema['num_tema']
        
        laws = extract_laws(titulo)
        
        if laws:
            # Ensure all laws exist in DB
            for law_ref in laws:
                get_or_create_law(law_ref)
                all_laws.add(law_ref)
            
            # Update tema with laws
            if update_tema_laws(tema_id, laws):
                print(f"  Tema {num}: {', '.join(laws)}")
                temas_with_laws += 1
                total_laws += len(laws)
    
    print(f"\nSummary for {nombre}:")
    print(f"  - {len(temas)} temas total")
    print(f"  - {temas_with_laws} temas with laws")
    print(f"  - {len(all_laws)} unique laws: {', '.join(sorted(all_laws))}")
    
    return temas_with_laws, all_laws


def finalize_oposicion(opos_id):
    """Mark oposicion as leyes_ok"""
    r = requests.patch(
        f"{API}/oposiciones/{opos_id}",
        json={'pipeline_state': 'leyes_ok', 'agente_activo': None}
    )
    return r.status_code == 200


def main():
    oposiciones = [
        ('341693c6-a757-4981-9843-5d8c33108521', 'Bibliotecario del Estado'),
        ('7d1701d2-2b02-43b4-b722-b95456f637dd', 'Escala Superior del Cuerpo de Seguridad Nuclear y Protección Radiológica'),
        ('392d33e7-b310-4f57-835c-67c6c1e4fc39', 'TCAE del Servicio Murciano de Salud (SMS)'),
    ]
    
    results = []
    
    for opos_id, nombre in oposiciones:
        temas_linked, laws = process_oposicion(opos_id, nombre)
        
        if finalize_oposicion(opos_id):
            print(f"✓ Marked as leyes_ok: {nombre}")
        else:
            print(f"✗ Failed to finalize: {nombre}")
        
        results.append({
            'nombre': nombre,
            'temas_with_laws': temas_linked,
            'laws': list(laws)
        })
    
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    for r in results:
        print(f"\n{r['nombre']}:")
        print(f"  Temas with laws: {r['temas_with_laws']}")
        print(f"  Laws: {', '.join(sorted(r['laws']))}")


if __name__ == '__main__':
    main()
