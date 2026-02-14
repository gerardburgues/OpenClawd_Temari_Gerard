#!/usr/bin/env python3
"""Process Maestro Educación Primaria Canarias - map laws to temas"""
import requests

API = "http://localhost:8001"
OPOS_ID = "fb1bce62-5c1e-49e6-bc01-917f3fc0faeb"

# Manual mapping based on analysis
TEMA_LAWS = {
    1: ['LO 2/2006', 'LO 3/2020'],  # LOMLOE (modificación de LOE)
    2: ['LO 2/2006', 'LO 3/2020'],  # LOMLOE
    3: [],  # Pedagogía, no ley específica
    4: ['LO 2/2006', 'LO 3/2020'],  # Atención diversidad en LOMLOE
    5: ['LO 2/2006', 'LO 3/2020'],  # Evaluación LOMLOE
    6: ['LO 2/2006', 'LO 3/2020'],  # Competencias clave
    7: ['LO 2/2006', 'LO 3/2020'],  # Currículo
    8: [],  # Principios didácticos, sin ley
    9: ['LO 2/2006', 'LO 3/2020'],  # Área curricular
    10: ['LO 2/2006', 'LO 3/2020'],  # Área curricular
    11: ['LO 2/2006', 'LO 3/2020'],  # Área curricular
    12: ['LO 2/2006', 'LO 3/2020'],  # Área curricular
    13: ['LO 2/2006', 'LO 3/2020'],  # Área curricular
    14: ['LO 2/2006', 'LO 3/2020'],  # Área curricular + MCER
    15: [],  # Desarrollo evolutivo
    16: [],  # Salud - varios reglamentos menores
    17: [],  # Desarrollo lenguaje
    18: [],  # Escritura
    19: ['LO 2/2006', 'LO 3/2020'],  # Proyecto educativo centro
    20: ['LO 2/2006', 'LO 3/2020'],  # Formación profesorado
    21: [],  # Familia como agente socializador
    22: ['LO 3/2007', 'LO 2/2006'],  # Educación ciudadanía, igualdad
    23: ['LO 2/2006', 'LO 3/2020'],  # DUA - accesibilidad
    24: ['LO 3/2018'],  # Competencia digital - LOPDGDD
    25: ['LO 2/2006', 'LO 3/2020'],  # Área Valores Cívicos
}

def ensure_law_exists(ref):
    """Ensure law exists"""
    r = requests.get(f"{API}/legislacion/by-referencia/{ref}")
    if r.status_code == 200:
        requests.patch(f"{API}/legislacion/by-referencia/{ref}/increment")
        return True
    return False

def update_tema(tema_id, laws):
    """Update tema"""
    r = requests.patch(
        f"{API}/temario/{tema_id}",
        json={'leyes_vinculadas': laws}
    )
    return r.status_code == 200

def main():
    r = requests.get(f"{API}/temario/?oposicion_id={OPOS_ID}&limit=100")
    temas = r.json()
    
    print("=" * 60)
    print("MAESTRO PRIMARIA CANARIAS - Mapping Laws")
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
            # Clear any existing laws
            update_tema(tema_id, [])
    
    print(f"\nTotal: {updated} temas with laws")
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
