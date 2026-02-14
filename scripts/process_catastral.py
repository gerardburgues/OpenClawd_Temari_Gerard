#!/usr/bin/env python3
"""Process Gestión Catastral - map laws to temas"""
import requests

API = "http://localhost:8001"
OPOS_ID = "eadeba30-9e72-4c05-897e-eff03bad384e"

# Laws to ensure exist - many fiscal laws
NEW_LAWS = {
    'TRLCI': {
        'nombre_corto': 'Texto Refundido Ley Catastro Inmobiliario',
        'nombre_completo': 'Real Decreto Legislativo 1/2004, de 5 de marzo, por el que se aprueba el texto refundido de la Ley del Catastro Inmobiliario',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2004-4163'
    },
    'LISD': {
        'nombre_corto': 'Ley del Impuesto sobre Sucesiones y Donaciones', 
        'nombre_completo': 'Ley 29/1987, de 18 de diciembre, del Impuesto sobre Sucesiones y Donaciones',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1987-28141'
    },
    'LITPAJD': {
        'nombre_corto': 'Ley ITP y AJD',
        'nombre_completo': 'Real Decreto Legislativo 1/1993, de 24 de septiembre, Texto Refundido de la Ley del Impuesto sobre Transmisiones Patrimoniales y Actos Jurídicos Documentados',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1993-25359'
    },
    'TRLHL': {
        'nombre_corto': 'Texto Refundido Ley Haciendas Locales',
        'nombre_completo': 'Real Decreto Legislativo 2/2004, de 5 de marzo, por el que se aprueba el texto refundido de la Ley Reguladora de las Haciendas Locales',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2004-4214'
    },
    'Ley 49/2002': {
        'nombre_corto': 'Ley de Régimen Fiscal de Entidades sin Fines Lucrativos',
        'nombre_completo': 'Ley 49/2002, de 23 de diciembre, de régimen fiscal de las entidades sin fines lucrativos y de los incentivos fiscales al mecenazgo',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-25039'
    },
    'LH': {
        'nombre_corto': 'Ley Hipotecaria',
        'nombre_completo': 'Decreto de 8 de febrero de 1946 por el que se aprueba la nueva redacción oficial de la Ley Hipotecaria',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1946-2453'
    },
    'RH': {
        'nombre_corto': 'Reglamento Hipotecario',
        'nombre_completo': 'Decreto de 14 de febrero de 1947 por el que se aprueba el Reglamento Hipotecario',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1947-3843'
    },
    'LEF': {
        'nombre_corto': 'Ley de Expropiación Forzosa',
        'nombre_completo': 'Ley de 16 de diciembre de 1954 sobre expropiación forzosa',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1954-15431'
    },
    'TRLSRU': {
        'nombre_corto': 'Texto Refundido Ley Suelo',
        'nombre_completo': 'Real Decreto Legislativo 7/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley de Suelo y Rehabilitación Urbana',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11723'
    },
    'LSC': {
        'nombre_corto': 'Ley de Sociedades de Capital',
        'nombre_completo': 'Real Decreto Legislativo 1/2010, de 2 de julio, por el que se aprueba el texto refundido de la Ley de Sociedades de Capital',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2010-10544'
    },
    'RRM': {
        'nombre_corto': 'Reglamento Registro Mercantil',
        'nombre_completo': 'Real Decreto 1784/1996, de 19 de julio, por el que se aprueba el Reglamento del Registro Mercantil',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1996-17533'
    },
    'LGT': {
        'nombre_corto': 'Ley General Tributaria',
        'nombre_completo': 'Ley 58/2003, de 17 de diciembre, General Tributaria',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-2003-23186'
    },
    'LPH': {
        'nombre_corto': 'Ley de Propiedad Horizontal',
        'nombre_completo': 'Ley 49/1960, de 21 de julio, sobre propiedad horizontal',
        'url_boe': 'https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906'
    },
}

# Mapping for each tema
TEMA_LAWS = {
    1: [],  # UE - Tratados
    2: ['CE 1978'],
    3: ['CE 1978'],
    4: ['CE 1978', 'Ley 39/2015', 'Ley 40/2015'],  # Fuentes derecho admin
    5: ['Ley 39/2015', 'Ley 40/2015'],
    6: ['Ley 39/2015'],
    7: ['Ley 39/2015'],
    8: ['Ley 39/2015'],
    9: ['Ley 39/2015'],
    10: ['Ley 29/1998'],  # LJCA
    11: ['Ley 40/2015'],  # Responsabilidad patrimonial
    12: ['Ley 9/2017'],  # LCSP
    13: ['Ley 33/2003'],  # Patrimonio AAPP
    14: ['LEF'],  # Expropiación
    15: [],  # Servicio público
    16: ['RDL 7/2015'],  # TRLSRU
    17: ['RDL 7/2015'],
    18: [],  # VPO - normativa diversa
    19: ['Ley 40/2015'],  # Organización AGE
    20: ['RDL 5/2015'],  # TREBEP
    21: ['LO 3/2007', 'LO 1/2004', 'Ley 39/2006'],
    22: ['Ley 19/2013'],  # Transparencia
    23: ['CC'],  # Código Civil
    24: ['CC'],
    25: ['CC'],
    26: ['CC'],
    27: ['CC'],
    28: ['CC'],
    29: ['CC'],
    30: ['CC', 'LPH'],
    31: ['CC'],
    32: ['CC', 'LH'],
    33: ['LH'],  # Ley Hipotecaria
    34: ['LH', 'TRLCI'],  # Coordinación Catastro-Registro
    35: ['CC'],
    36: ['CC'],
    37: ['LEF'],
    38: ['CCom'],  # Código Comercio
    39: ['LSC'],
    40: ['LSC'],
    41: ['LSC'],
    42: ['LSC'],
    43: ['CE 1978', 'LGT'],
    44: ['LGT'],
    45: ['LGT'],
    46: ['LGT'],
    47: ['LGT'],
    48: ['LGT', 'LO 10/1995'],  # Delitos Hacienda
    49: ['LIRPF'],
    50: ['LIRPF'],
    51: ['LIRPF'],
    52: ['LISD'],  # IP e ISD
    53: ['LIS'],
    54: ['LITPAJD'],
    55: ['Ley 37/1992'],  # IVA
    56: ['Ley 37/1992'],
    57: ['TRLHL'],  # IBI
    58: ['TRLHL'],  # IAE, IVTM, ICIO, IIVTNU
    59: ['TRLHL'],  # Tasas locales
    60: [],  # Financiación CCAA
    61: ['TRLCI', 'TRLHL'],  # Catastro e IBI
    62: ['TRLCI'],  # Valor de referencia
    63: ['TRLCI'],  # Valoración colectiva
    64: ['TRLCI', 'TRLHL'],  # Sujetos pasivos IBI
    65: ['TRLCI'],  # Catastro Inmobiliario
    66: ['TRLCI'],
    67: ['TRLCI'],
    68: ['TRLCI'],
    69: ['TRLCI'],
    70: ['TRLCI'],
    71: ['TRLCI'],
    72: ['TRLCI'],
    73: ['TRLCI'],
    74: ['TRLCI', 'LGT'],
    75: ['TRLCI'],
    76: ['TRLCI'],
    77: ['TRLCI'],
    78: ['TRLCI', 'LO 3/2018'],
    79: ['TRLCI', 'LH'],
    80: ['TRLCI', 'RDL 7/2015'],
    81: ['TRLCI'],
    82: ['TRLCI'],
    83: [],  # SIG - técnico
    84: [],  # Fotogrametría - técnico
    85: ['Ley 39/2015', 'TRLCI'],  # Administración electrónica
    86: ['TRLCI'],
    87: [],  # UE Catastro
    88: [],  # Plan estratégico
}

def ensure_law_exists(ref):
    r = requests.get(f"{API}/legislacion/by-referencia/{ref}")
    if r.status_code == 200:
        requests.patch(f"{API}/legislacion/by-referencia/{ref}/increment")
        return True
    
    # Create new if in NEW_LAWS
    if ref in NEW_LAWS:
        info = NEW_LAWS[ref]
        data = {
            'referencia': ref,
            'nombre_corto': info['nombre_corto'],
            'nombre_completo': info['nombre_completo'],
            'url_boe': info['url_boe'],
            'veces_referenciada': 1
        }
        r = requests.post(f"{API}/legislacion/", json=data)
        if r.status_code == 201:
            print(f"  + Created: {ref}")
            return True
    return False

def update_tema(tema_id, laws):
    r = requests.patch(
        f"{API}/temario/{tema_id}",
        json={'leyes_vinculadas': laws}
    )
    return r.status_code == 200

def main():
    r = requests.get(f"{API}/temario/?oposicion_id={OPOS_ID}&limit=100")
    temas = r.json()
    
    print("=" * 60)
    print("GESTIÓN CATASTRAL - Mapping Laws")
    print("=" * 60)
    
    updated = 0
    all_laws = set()
    
    for tema in temas:
        num = tema['num_tema']
        tema_id = tema['id']
        
        if num in TEMA_LAWS and TEMA_LAWS[num]:
            laws = TEMA_LAWS[num]
            for ref in laws:
                ensure_law_exists(ref)
                all_laws.add(ref)
            
            if update_tema(tema_id, laws):
                print(f"✓ Tema {num}: {', '.join(laws)}")
                updated += 1
        elif num in TEMA_LAWS:
            update_tema(tema_id, [])
    
    print(f"\nTotal: {updated} temas with laws")
    print(f"Unique laws ({len(all_laws)}): {', '.join(sorted(all_laws))}")
    
    # Mark as leyes_ok
    r = requests.patch(
        f"{API}/oposiciones/{OPOS_ID}",
        json={'pipeline_state': 'leyes_ok', 'agente_activo': None}
    )
    if r.status_code == 200:
        print("✓ Marked as leyes_ok")

if __name__ == '__main__':
    main()
