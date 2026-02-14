#!/usr/bin/env python3
"""
Process 3 oposiciones: Letrados SS, Guardia Civil Suboficiales, Médico Osakidetza
Map laws to temas and update
"""
import json
import requests

API = "http://localhost:8001"

# Law mappings for each oposición
LETRADOS_SS_LAWS = {
    # Bloque Seguridad Social
    ("Seguridad Social", 1): ["CE 1978", "RDL 8/2015"],  # LGSS + Pacto Toledo
    ("Seguridad Social", 2): ["RDL 8/2015", "LO 4/2000"],
    ("Seguridad Social", 3): ["RDL 8/2015"],
    ("Seguridad Social", 4): ["RDL 8/2015", "Ley 47/2003"],  # LGP
    ("Seguridad Social", 5): ["RDL 8/2015"],
    ("Seguridad Social", 6): ["RDL 8/2015"],
    ("Seguridad Social", 7): ["RDL 8/2015"],
    ("Seguridad Social", 8): ["RDL 8/2015"],
    ("Seguridad Social", 9): ["RDL 8/2015"],
    ("Seguridad Social", 10): ["Ley 39/2006", "RDL 1/2013"],  # Dependencia, Discapacidad
    # Bloque Derecho Civil
    ("Derecho Civil", 1): ["CC 1889"],
    ("Derecho Civil", 2): ["CC 1889"],
    ("Derecho Civil", 3): ["CE 1978", "CC 1889"],
    ("Derecho Civil", 4): ["CC 1889"],
    ("Derecho Civil", 5): ["CC 1889"],
    ("Derecho Civil", 6): ["CC 1889"],
    ("Derecho Civil", 7): ["CC 1889"],
    ("Derecho Civil", 8): ["CC 1889"],
    ("Derecho Civil", 9): ["CC 1889"],
    ("Derecho Civil", 10): ["CC 1889"],
    # Bloque Derecho Procesal Laboral
    ("Derecho Procesal Laboral", 1): ["LRJS", "LO 6/1985"],  # Ley 36/2011 LRJS
    ("Derecho Procesal Laboral", 2): ["LRJS", "Ley 39/2015"],
    ("Derecho Procesal Laboral", 3): ["LRJS"],
    ("Derecho Procesal Laboral", 4): ["LRJS"],
    ("Derecho Procesal Laboral", 5): ["LRJS", "RDL 2/2015"],  # ET
}

GUARDIA_CIVIL_LAWS = {
    1: ["DUDH", "PIDCP", "CEDH"],  # Treaties
    2: ["TUE", "TFUE", "CDFUE"],  # EU Treaties
    3: [],  # Schengen - EU regulation
    4: ["RD 240/2007", "LO 4/2000"],
    5: ["Ley 12/2009"],
    6: [],  # International convention - no Spanish law
    7: ["RGPD 2016/679", "LO 3/2018", "LO 7/2021"],
    8: ["LO 1/2004"],
    9: ["LO 3/2007", "RD 247/2024"],
    10: ["CC 1889"],
    11: ["LO 10/1995"],
    12: ["LECrim"],
    13: ["LO 6/1984", "LO 19/1994", "Ley 4/2015"],
    14: ["LO 1/1996", "LO 5/2000", "RD 1774/2004"],
    15: ["LO 4/2015"],
    16: ["RD 137/1993", "RD 989/2015", "RD 130/2017"],
    17: ["LO 12/1995", "RD 1649/1998"],  # Contrabando
    18: ["Ley 5/2014"],
    19: ["Ley 42/2007"],
    20: ["RDL 6/2015"],
    21: ["RD 367/1997", "RD 1009/2023", "RD 207/2024"],
    22: ["LO 2/1986", "RD 1087/2010"],
    23: ["LO 11/2007", "LO 12/2007", "Ley 29/2014"],
    24: ["RD 179/2005", "RD 470/2019"],
    25: ["RDL 5/2015", "RD 176/2022"],
}

MEDICO_OSAKIDETZA_LAWS = {
    1: ["Ley 44/2003"],  # LOPS
    2: ["Ley 16/2003"],  # Cohesión SNS
    3: ["Ley 55/2003"],  # Estatuto Marco
    4: ["Ley 8/1997 PV"],  # Ordenación Sanitaria Euskadi
    5: ["Ley 8/1997 PV"],  # Osakidetza
    6: ["Ley 8/1997 PV"],  # Derechos
    7: ["Ley 41/2002"],  # Autonomía paciente
    8: ["Ley 41/2002"],  # Voluntades anticipadas
    9: ["LO 3/2018"],  # LOPDGDD
    10: ["LO 3/2007", "Ley 4/2005 PV"],  # Igualdad
    # Temas 11-15: Estratégicos - sin legislación
    # Temas 16-52: Clínicos - mayormente sin legislación
    50: ["Ley 41/2002"],  # Bioética - Autonomía paciente
    52: ["LO 1/2004"],  # Violencia de género
}

# New laws to create
NEW_LAWS = {
    "RDL 8/2015": {
        "nombre_corto": "LGSS",
        "nombre_completo": "Real Decreto Legislativo 8/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley General de la Seguridad Social",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
    },
    "LRJS": {
        "nombre_corto": "Ley Reguladora Jurisdicción Social",
        "nombre_completo": "Ley 36/2011, de 10 de octubre, reguladora de la jurisdicción social",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2011-15936"
    },
    "RDL 2/2015": {
        "nombre_corto": "Estatuto de los Trabajadores",
        "nombre_completo": "Real Decreto Legislativo 2/2015, de 23 de octubre, por el que se aprueba el texto refundido de la Ley del Estatuto de los Trabajadores",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430"
    },
    "DUDH": {
        "nombre_corto": "Declaración Universal Derechos Humanos",
        "nombre_completo": "Declaración Universal de Derechos Humanos de 10 de diciembre de 1948",
        "url_boe": None
    },
    "PIDCP": {
        "nombre_corto": "Pacto Internacional Derechos Civiles y Políticos",
        "nombre_completo": "Pacto Internacional de Derechos Civiles y Políticos",
        "url_boe": "https://www.boe.es/buscar/doc.php?id=BOE-A-1977-10733"
    },
    "CEDH": {
        "nombre_corto": "Convenio Europeo Derechos Humanos",
        "nombre_completo": "Convenio para la Protección de los Derechos Humanos y de las Libertades Fundamentales",
        "url_boe": "https://www.boe.es/buscar/doc.php?id=BOE-A-1979-24010"
    },
    "TUE": {
        "nombre_corto": "Tratado de la Unión Europea",
        "nombre_completo": "Tratado de la Unión Europea (Maastricht/Lisboa)",
        "url_boe": None
    },
    "TFUE": {
        "nombre_corto": "Tratado de Funcionamiento UE",
        "nombre_completo": "Tratado de Funcionamiento de la Unión Europea",
        "url_boe": None
    },
    "CDFUE": {
        "nombre_corto": "Carta Derechos Fundamentales UE",
        "nombre_completo": "Carta de los Derechos Fundamentales de la Unión Europea",
        "url_boe": None
    },
    "RD 240/2007": {
        "nombre_corto": "RD Libre Circulación UE",
        "nombre_completo": "Real Decreto 240/2007, de 16 de febrero, sobre entrada, libre circulación y residencia en España de ciudadanos UE",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2007-4184"
    },
    "Ley 12/2009": {
        "nombre_corto": "Ley de Asilo",
        "nombre_completo": "Ley 12/2009, de 30 de octubre, reguladora del derecho de asilo y de la protección subsidiaria",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2009-17242"
    },
    "LO 7/2021": {
        "nombre_corto": "LOPD Prevención Delitos",
        "nombre_completo": "Ley Orgánica 7/2021, de 26 de mayo, de protección de datos personales tratados para fines de prevención",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2021-8806"
    },
    "RD 247/2024": {
        "nombre_corto": "Protocolo Acoso AGE",
        "nombre_completo": "Real Decreto 247/2024, Protocolo de actuación frente al acoso sexual y al acoso por razón de sexo en la AGE",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2024-5089"
    },
    "LO 6/1984": {
        "nombre_corto": "Ley Habeas Corpus",
        "nombre_completo": "Ley Orgánica 6/1984, de 24 de mayo, reguladora del procedimiento de Habeas Corpus",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-1984-11620"
    },
    "LO 19/1994": {
        "nombre_corto": "Protección Testigos y Peritos",
        "nombre_completo": "Ley Orgánica 19/1994, de 23 de diciembre, de protección a testigos y peritos",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-1994-28510"
    },
    "Ley 4/2015": {
        "nombre_corto": "Estatuto de la Víctima",
        "nombre_completo": "Ley 4/2015, de 27 de abril, del Estatuto de la víctima del delito",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-4606"
    },
    "LO 1/1996": {
        "nombre_corto": "Protección Jurídica del Menor",
        "nombre_completo": "Ley Orgánica 1/1996, de 15 de enero, de Protección Jurídica del Menor",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-1996-1069"
    },
    "LO 5/2000": {
        "nombre_corto": "Responsabilidad Penal Menores",
        "nombre_completo": "Ley Orgánica 5/2000, de 12 de enero, reguladora de la responsabilidad penal de los menores",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2000-641"
    },
    "RD 1774/2004": {
        "nombre_corto": "Reglamento LO 5/2000",
        "nombre_completo": "Real Decreto 1774/2004, Reglamento de la Ley Orgánica 5/2000",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2004-14476"
    },
    "RD 137/1993": {
        "nombre_corto": "Reglamento de Armas",
        "nombre_completo": "Real Decreto 137/1993, de 29 de enero, por el que se aprueba el Reglamento de Armas",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-1993-6202"
    },
    "RD 989/2015": {
        "nombre_corto": "Reglamento Artículos Pirotécnicos",
        "nombre_completo": "Real Decreto 989/2015, de 30 de octubre, por el que se aprueba el Reglamento de artículos pirotécnicos y cartuchería",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-12845"
    },
    "RD 130/2017": {
        "nombre_corto": "Reglamento de Explosivos",
        "nombre_completo": "Real Decreto 130/2017, de 24 de febrero, por el que se aprueba el Reglamento de Explosivos",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2017-2100"
    },
    "LO 12/1995": {
        "nombre_corto": "Ley de Contrabando",
        "nombre_completo": "Ley Orgánica 12/1995, de 12 de diciembre, de Represión del Contrabando",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-1995-26714"
    },
    "Ley 5/2014": {
        "nombre_corto": "Ley de Seguridad Privada",
        "nombre_completo": "Ley 5/2014, de 4 de abril, de Seguridad Privada",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2014-3649"
    },
    "Ley 42/2007": {
        "nombre_corto": "Ley Patrimonio Natural y Biodiversidad",
        "nombre_completo": "Ley 42/2007, de 13 de diciembre, del Patrimonio Natural y de la Biodiversidad",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2007-21490"
    },
    "RD 367/1997": {
        "nombre_corto": "Organización Periférica DGGC",
        "nombre_completo": "Real Decreto 367/1997, por el que se desarrolla la organización periférica de la Dirección General de la Guardia Civil",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-1997-6081"
    },
    "RD 1009/2023": {
        "nombre_corto": "Estructura Orgánica Ministerios",
        "nombre_completo": "Real Decreto 1009/2023, por el que se establece la estructura orgánica básica de los departamentos ministeriales",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2023-24409"
    },
    "RD 207/2024": {
        "nombre_corto": "Estructura Ministerio Interior",
        "nombre_completo": "Real Decreto 207/2024, por el que se desarrolla la estructura orgánica básica del Ministerio del Interior",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2024-4024"
    },
    "RD 1087/2010": {
        "nombre_corto": "Reglamento Juntas Locales Seguridad",
        "nombre_completo": "Real Decreto 1087/2010, Reglamento de las Juntas Locales de Seguridad",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2010-13577"
    },
    "LO 11/2007": {
        "nombre_corto": "Derechos y Deberes GC",
        "nombre_completo": "Ley Orgánica 11/2007, reguladora de los derechos y deberes de los miembros de la Guardia Civil",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2007-18714"
    },
    "LO 12/2007": {
        "nombre_corto": "Régimen Disciplinario GC",
        "nombre_completo": "Ley Orgánica 12/2007, de 22 de octubre, del régimen disciplinario de la Guardia Civil",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2007-18487"
    },
    "Ley 29/2014": {
        "nombre_corto": "Régimen Personal GC",
        "nombre_completo": "Ley 29/2014, de 28 de noviembre, de Régimen del Personal de la Guardia Civil",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2014-12328"
    },
    "RD 179/2005": {
        "nombre_corto": "PRL en Guardia Civil",
        "nombre_completo": "Real Decreto 179/2005, sobre prevención de riesgos laborales en la Guardia Civil",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2005-3052"
    },
    "RD 470/2019": {
        "nombre_corto": "Reglamento Destinos GC",
        "nombre_completo": "Real Decreto 470/2019, Reglamento de destinos del personal de la Guardia Civil",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2019-11317"
    },
    "RD 176/2022": {
        "nombre_corto": "Código Conducta GC",
        "nombre_completo": "Real Decreto 176/2022, por el que se aprueba el Código de Conducta del personal de la Guardia Civil",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2022-4038"
    },
    "Ley 8/1997 PV": {
        "nombre_corto": "Ordenación Sanitaria Euskadi",
        "nombre_completo": "Ley 8/1997, de 26 de junio, de Ordenación sanitaria de Euskadi",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2012-2252"
    },
    "Ley 4/2005 PV": {
        "nombre_corto": "Ley Igualdad Euskadi",
        "nombre_completo": "Ley 4/2005, de 18 de febrero, para la Igualdad de Mujeres y Hombres del País Vasco",
        "url_boe": None
    },
}


def get_or_create_law(referencia):
    """Get existing law or create new one, return True if successful"""
    # Check if exists
    r = requests.get(f"{API}/legislacion/by-referencia/{referencia}")
    if r.status_code == 200:
        # Increment reference count
        requests.patch(f"{API}/legislacion/by-referencia/{referencia}/increment")
        return True
    
    # Create new if in NEW_LAWS
    if referencia in NEW_LAWS:
        info = NEW_LAWS[referencia]
        data = {
            'referencia': referencia,
            'nombre_corto': info.get('nombre_corto') or referencia,
            'nombre_completo': info.get('nombre_completo'),
            'url_boe': info.get('url_boe'),
            'veces_referenciada': 1
        }
        r = requests.post(f"{API}/legislacion/", json=data)
        if r.status_code == 201:
            print(f"  ✓ Created: {referencia}")
            return True
        else:
            print(f"  ✗ Failed to create: {referencia} - {r.text}")
            return False
    
    print(f"  ? Unknown law, skipping: {referencia}")
    return False


def update_tema_laws(tema_id, leyes_vinculadas):
    """Update a tema with its linked laws"""
    r = requests.patch(
        f"{API}/temario/{tema_id}",
        json={'leyes_vinculadas': leyes_vinculadas}
    )
    return r.status_code == 200


def process_letrados():
    """Process Letrados de la Seguridad Social"""
    opos_id = "baac8afe-8e06-443c-8465-b28052092bca"
    print("\n" + "="*60)
    print("Processing: Cuerpo Superior de Letrados de la Administración de la Seguridad Social")
    print("="*60)
    
    r = requests.get(f"{API}/temario/?oposicion_id={opos_id}&limit=200")
    temas = r.json()
    
    total_linked = 0
    all_laws = set()
    
    for tema in temas:
        bloque = tema['bloque']
        num = tema['num_tema']
        tema_id = tema['id']
        
        key = (bloque, num)
        if key in LETRADOS_SS_LAWS:
            laws = LETRADOS_SS_LAWS[key]
            if laws:
                # Ensure laws exist
                for law_ref in laws:
                    get_or_create_law(law_ref)
                    all_laws.add(law_ref)
                
                if update_tema_laws(tema_id, laws):
                    print(f"  {bloque} Tema {num}: {', '.join(laws)}")
                    total_linked += 1
    
    print(f"\nSummary: {total_linked} temas with laws, {len(all_laws)} unique laws")
    return total_linked, all_laws


def process_guardia_civil():
    """Process Guardia Civil - Escala de Suboficiales"""
    opos_id = "87d2e57a-3d6e-4122-9bc7-561a84729bf8"
    print("\n" + "="*60)
    print("Processing: Guardia Civil - Escala de Suboficiales")
    print("="*60)
    
    r = requests.get(f"{API}/temario/?oposicion_id={opos_id}&limit=200")
    temas = r.json()
    
    total_linked = 0
    all_laws = set()
    
    for tema in temas:
        num = tema['num_tema']
        tema_id = tema['id']
        
        if num in GUARDIA_CIVIL_LAWS:
            laws = GUARDIA_CIVIL_LAWS[num]
            if laws:
                # Ensure laws exist
                for law_ref in laws:
                    get_or_create_law(law_ref)
                    all_laws.add(law_ref)
                
                if update_tema_laws(tema_id, laws):
                    print(f"  Tema {num}: {', '.join(laws)}")
                    total_linked += 1
    
    print(f"\nSummary: {total_linked} temas with laws, {len(all_laws)} unique laws")
    return total_linked, all_laws


def process_medico_osakidetza():
    """Process Médico de Familia de Osakidetza"""
    opos_id = "5ea22047-36cb-4d42-b599-474b4dc0c943"
    print("\n" + "="*60)
    print("Processing: Médico de Familia de Osakidetza")
    print("="*60)
    
    r = requests.get(f"{API}/temario/?oposicion_id={opos_id}&limit=200")
    temas = r.json()
    
    total_linked = 0
    all_laws = set()
    
    for tema in temas:
        num = tema['num_tema']
        tema_id = tema['id']
        
        if num in MEDICO_OSAKIDETZA_LAWS:
            laws = MEDICO_OSAKIDETZA_LAWS[num]
            if laws:
                # Ensure laws exist
                for law_ref in laws:
                    get_or_create_law(law_ref)
                    all_laws.add(law_ref)
                
                if update_tema_laws(tema_id, laws):
                    print(f"  Tema {num}: {', '.join(laws)}")
                    total_linked += 1
    
    print(f"\nSummary: {total_linked} temas with laws, {len(all_laws)} unique laws")
    return total_linked, all_laws


def finalize_oposicion(opos_id, nombre):
    """Mark oposicion as leyes_ok"""
    r = requests.patch(
        f"{API}/oposiciones/{opos_id}",
        json={'pipeline_state': 'leyes_ok', 'agente_activo': None}
    )
    if r.status_code == 200:
        print(f"✓ Marked as leyes_ok: {nombre}")
        return True
    else:
        print(f"✗ Failed to finalize: {nombre}")
        return False


def main():
    results = []
    
    # Process all three
    temas1, laws1 = process_letrados()
    finalize_oposicion("baac8afe-8e06-443c-8465-b28052092bca", "Letrados Seguridad Social")
    results.append(("Letrados Seguridad Social", temas1, laws1))
    
    temas2, laws2 = process_guardia_civil()
    finalize_oposicion("87d2e57a-3d6e-4122-9bc7-561a84729bf8", "Guardia Civil Suboficiales")
    results.append(("Guardia Civil Suboficiales", temas2, laws2))
    
    temas3, laws3 = process_medico_osakidetza()
    finalize_oposicion("5ea22047-36cb-4d42-b599-474b4dc0c943", "Médico Familia Osakidetza")
    results.append(("Médico Familia Osakidetza", temas3, laws3))
    
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    for nombre, temas, laws in results:
        print(f"\n{nombre}:")
        print(f"  Temas with laws: {temas}")
        print(f"  Unique laws: {len(laws)}")
        if laws:
            print(f"  Laws: {', '.join(sorted(laws))}")


if __name__ == '__main__':
    main()
