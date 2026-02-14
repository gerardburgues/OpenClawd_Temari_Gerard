#!/usr/bin/env python3
"""
Decodificador: Map laws to temario topics for 3 oposiciones
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
    (r'Constituci[óo]\s+Espanyola', 'CE 1978'),
    
    # Leyes orgánicas con número
    (r'Ley\s+Org[áa]nica\s+(\d+/\d{4})', lambda m: f'LO {m.group(1)}'),
    (r'L\.?O\.?\s+(\d+/\d{4})', lambda m: f'LO {m.group(1)}'),
    
    # Leyes con número  
    (r'Ley\s+(\d+/\d{4})', lambda m: f'Ley {m.group(1)}'),
    (r'Llei\s+(\d+/\d{4})', lambda m: f'Ley {m.group(1)}'),
    
    # Reales Decretos Legislativos
    (r'Real\s+Decreto\s+Legislativo\s+(\d+/\d{4})', lambda m: f'RDL {m.group(1)}'),
    (r'RDL\s+(\d+/\d{4})', lambda m: f'RDL {m.group(1)}'),
    (r'Reial\s+Decret\s+Legislatiu\s+(\d+/\d{4})', lambda m: f'RDL {m.group(1)}'),
    
    # Reales Decretos
    (r'Real\s+Decreto\s+(\d+/\d{4})', lambda m: f'RD {m.group(1)}'),
    (r'RD\s+(\d+/\d{4})', lambda m: f'RD {m.group(1)}'),
    
    # Decreto Foral
    (r'Decreto\s+Foral\s+(\d+/\d{4})', lambda m: f'DF {m.group(1)}'),
    
    # Ley Foral
    (r'Ley\s+Foral\s+(\d+/\d{4})', lambda m: f'LF {m.group(1)}'),
    
    # Estatutos de Autonomía específicos
    (r'Estatut[o]?\s+d[\'e]\s*Autonomia\s+(de|para)?\s*(Catalunya|Catalu[ñn]a)', 'LO 6/2006'),
    (r'Estatuto\s+de\s+Autonom[íi]a\s+para\s+Andaluc[íi]a', 'LO 2/2007'),
    (r'LORAFNA', 'LO 13/1982'),
    (r'Amejoramiento\s+del\s+R[ée]gimen\s+Foral\s+de\s+Navarra', 'LO 13/1982'),
    
    # Códigos
    (r'C[óo]digo\s+Penal', 'LO 10/1995'),
    (r'Ley\s+de\s+Enjuiciamiento\s+Criminal', 'LECrim'),
    
    # Leyes conocidas por nombre
    (r'Estatuto\s+Marco', 'Ley 55/2003'),
    (r'Estatut\s+B[àa]sic\s+de\s+l\'Empleat\s+P[úu]blic', 'RDL 5/2015'),
    (r'Estatuto\s+B[áa]sico\s+del\s+Empleado\s+P[úu]blico', 'RDL 5/2015'),
    (r'TREBEP', 'RDL 5/2015'),
    (r'Procediment[o]?\s+Administrati[uv][o]?\s+Com[úu]', 'Ley 39/2015'),
    (r'LPAC', 'Ley 39/2015'),
    (r'Protecci[óo][n]?\s+de\s+[Dd]atos\s+Personal', 'LO 3/2018'),
    (r'LOPDGDD', 'LO 3/2018'),
    (r'Reglamento\s+General\s+de\s+Protecci[óo]n\s+de\s+Datos', 'RGPD 2016/679'),
    (r'RGPD', 'RGPD 2016/679'),
    (r'Bases\s+del\s+R[ée]gimen\s+Local', 'Ley 7/1985'),
    (r'LRBRL', 'Ley 7/1985'),
    (r'Contractes?\s+del\s+Sector\s+P[úu]blic', 'Ley 9/2017'),
    (r'LCSP', 'Ley 9/2017'),
    (r'Fuerzas\s+y\s+Cuerpos\s+de\s+Seguridad', 'LO 2/1986'),
    (r'seguridad\s+ciudadana', 'LO 4/2015'),
    (r'Protecci[óo]n\s+Integral\s+contra\s+la\s+Violencia\s+de\s+G[ée]nero', 'LO 1/2004'),
    (r'protecci[óo]n\s+integral\s+a\s+la\s+infancia', 'LO 8/2021'),
    (r'Estatuto\s+de\s+la\s+[Vv][íi]ctima', 'Ley 4/2015'),
    (r'extranjeros\s+en\s+Espa[ñn]a', 'LO 4/2000'),
    (r'Tr[áa]fico.*Seguridad\s+Vial', 'RDL 6/2015'),
    (r'LSV', 'RDL 6/2015'),
    (r'Prevenci[óo]n\s+de\s+Riesgos\s+Laborales', 'Ley 31/1995'),
    (r'igualdad\s+efectiva\s+de\s+(mujeres\s+y\s+hombres|dones\s+i\s+homes)', 'LO 3/2007'),
]

# Mapping of referencia to full law info for new laws
NEW_LAWS = {
    'Ley 2/1998 And': {
        'nombre_corto': 'Ley de Salud de Andalucía',
        'nombre_completo': 'Ley 2/1998, de 15 de junio, de Salud de Andalucía',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1998-17900'
    },
    'LF 14/2015 Nav': {
        'nombre_corto': 'LF Violencia Mujeres Navarra',
        'nombre_completo': 'Ley Foral 14/2015, de 10 de abril, para actuar contra la violencia hacia las mujeres',
        'url_boe': None
    },
    'DF 718/1985': {
        'nombre_corto': 'Decreto Creación Policía Foral',
        'nombre_completo': 'Decreto Foral 718/1985, de creación de la Policía Foral de Navarra',
        'url_boe': None
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


def get_or_create_law(referencia, nombre_corto=None, nombre_completo=None, url_boe=None):
    """Get existing law or create new one, return referencia"""
    # Try to get existing
    r = requests.get(f"{API}/legislacion/by-referencia/{referencia}")
    if r.status_code == 200:
        # Increment reference count
        requests.patch(f"{API}/legislacion/by-referencia/{referencia}/increment")
        return referencia
    
    # Check NEW_LAWS dict
    if referencia in NEW_LAWS:
        info = NEW_LAWS[referencia]
        nombre_corto = info.get('nombre_corto')
        nombre_completo = info.get('nombre_completo')
        url_boe = info.get('url_boe')
    
    # Create new
    data = {
        'referencia': referencia,
        'nombre_corto': nombre_corto or referencia,
        'nombre_completo': nombre_completo,
        'url_boe': url_boe,
        'veces_referenciada': 1
    }
    r = requests.post(f"{API}/legislacion/", json=data)
    if r.status_code == 201:
        print(f"  ✓ Created: {referencia}")
    else:
        print(f"  ✗ Failed to create: {referencia} - {r.text}")
    return referencia


def update_tema_laws(tema_id, leyes_vinculadas):
    """Update a tema with its linked laws"""
    r = requests.patch(
        f"{API}/temario/{tema_id}",
        json={'leyes_vinculadas': leyes_vinculadas}
    )
    return r.status_code == 200


def process_oposicion(opos_id, nombre):
    """Process one oposicion: extract laws from temas and update"""
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
            # Ensure all laws exist
            for law_ref in laws:
                get_or_create_law(law_ref)
                all_laws.add(law_ref)
            
            # Update tema
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
        ('65862d6c-3d36-4e93-8e46-429da9f49e62', 'Médico de Familia del SAS'),
        ('5208143e-25c3-4258-9a10-dd7d8ff7e3dd', 'Auxiliar Administrativo Diputación Barcelona'),
        ('ac1bd315-7e6b-416a-a179-4058bd7d22a3', 'Policía Foral de Navarra'),
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
