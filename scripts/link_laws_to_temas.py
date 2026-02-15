#!/usr/bin/env python3
"""Link legislation to temario topics based on content analysis."""

import httpx
import json

API = "http://localhost:8005"

# Law IDs by category
LAWS = {
    # Constitutional
    "ce": "123c077a-5268-4712-b298-981edc3b63fc",  # CE 1978
    "lotc": "df8c9707-bb66-4ed9-952f-c928ba0f5040",  # LO 2/1979
    "lopj": "85cdea6e-3289-4980-8158-9efea945f3de",  # LO 6/1985
    "loaes": "b420efb0-e283-4499-b635-800db3a51f09",  # LO 4/1981 estados alarma
    "loreg": "c336d08c-4731-4fe2-8749-d0ff720b1ed2",  # LO 5/1985
    "lopp": "9c03dc83-6d5c-4350-936b-18d8fd94f57f",  # LO 6/2002 partidos
    "lols": "d3062f33-69e0-4d1c-8fc9-fdf4432fce1c",  # LO 11/1985 libertad sindical
    
    # Administrative
    "lpac": "6a536d86-c78f-4d8c-a4a1-bacaa627c568",  # Ley 39/2015
    "lrjsp": "9ac7a58f-0f1c-4420-b179-6eaab284abac",  # Ley 40/2015
    "gobierno": "0c71eaf8-774b-428a-b77d-3503a6b09968",  # Ley 50/1997
    "lrbrl": "88ac5439-322c-4325-81f1-5cc7e77c3fbc",  # Ley 7/1985
    "ljca": "f0bed5e8-d966-4f0d-8964-659a13e626c6",  # Ley 29/1998
    
    # Financial/Economic
    "lgp": "4cfb6804-f1a6-46fc-b914-7ee994f17765",  # Ley 47/2003
    "lcsp": "4431e9c7-e5d0-497c-86b7-db8d654ed5a0",  # Ley 9/2017
    "lgs": "03ccfe67-7313-454b-bea2-a2d185c593b9",  # Ley 38/2003 subvenciones
    "loep": "e3b3baa9-aaa7-42a1-a29b-3e072d808957",  # LO 2/2012 estabilidad
    
    # Employment/HR
    "trebep": "a519ac4b-1726-47bc-b2ef-781a6e7a3f3f",  # TREBEP
    "et": "3ea1f37d-5028-48b7-9d1d-47c637a3ee2f",  # ET
    "incomp": "73b44ca3-07f1-433b-8eef-39c75119d051",  # Ley 53/1984
    
    # EU
    "tue": "5adbc4d7-5108-4731-bd97-d2d0eb854fe6",  # TUE
    "tfue": "eeed712a-eca3-4743-9b3c-dcae9b649e8d",  # TFUE
}

# Topic mapping rules based on title keywords
RULES = [
    # Materias Comunes
    (["Constitución", "constituyente", "transición"], ["ce"]),
    (["derechos fundamentales", "garantías"], ["ce"]),
    (["monarquía", "Corona"], ["ce"]),
    (["Gobierno", "Administración pública"], ["gobierno", "lrjsp"]),
    (["Administración General del Estado", "AGE"], ["lrjsp"]),
    (["organización territorial", "Comunidades Autónomas"], ["ce", "lrbrl"]),
    (["competencias", "interadministrativ"], ["lrjsp"]),
    (["régimen jurídico", "procedimiento administrativo"], ["lpac", "lrjsp"]),
    (["personal", "empleado", "funcionario"], ["trebep"]),
    (["contratos", "contratación"], ["lcsp"]),
    (["presupuestos"], ["lgp"]),
    (["control jurisdiccional"], ["ljca"]),
    (["Unión Europea", "Comunidades Europeas", "Tratado"], ["tue", "tfue"]),
    (["derecho comunitario", "derecho de la Unión"], ["tue", "tfue"]),
    (["libre circulación", "mercado interior"], ["tfue"]),
    (["política agrícola", "política pesquera"], ["tfue"]),
    (["política exterior", "seguridad común"], ["tue"]),
    (["cohesión", "fondos europeos"], ["tfue"]),
    
    # Bloque I - Derecho Constitucional y Administrativo
    (["poder constituyente", "reforma"], ["ce"]),
    (["derechos económicos", "derechos sociales"], ["ce"]),
    (["protección jurisdiccional"], ["ce", "lotc"]),
    (["estados de alarma", "excepción", "sitio"], ["ce", "loaes"]),
    (["partidos políticos", "sindicatos"], ["lopp", "lols"]),
    (["Gobierno: composición", "nombramiento", "cese"], ["ce", "gobierno"]),
    (["funciones del Gobierno"], ["gobierno"]),
    (["Cortes Generales", "parlamentari"], ["ce"]),
    (["procedimiento legislativo"], ["ce"]),
    (["control parlamentario"], ["ce"]),
    (["Tribunal de Cuentas"], ["ce"]),
    (["Consejo de Estado"], ["lrjsp"]),
    (["Poder Judicial", "organización judicial"], ["lopj"]),
    (["Consejo General del Poder Judicial", "Ministerio Fiscal"], ["lopj"]),
    (["Tribunal Constitucional"], ["lotc"]),
    (["control de constitucionalidad"], ["lotc"]),
    (["conflictos", "competenciales"], ["lotc"]),
    (["sector público institucional"], ["lrjsp"]),
    (["Estatutos de Autonomía"], ["ce"]),
    (["derecho administrativo", "Administración pública"], ["lpac", "lrjsp"]),
    (["fuentes del derecho", "ley"], ["ce"]),
    (["decretos legislativos", "decretos-leyes"], ["ce"]),
    (["reglamento", "potestad reglamentaria"], ["lpac", "lrjsp"]),
    (["potestades administrativas", "discrecional"], ["lpac"]),
    (["administrado"], ["lpac"]),
    
    # Bloque II - Economía y Administración Financiera
    (["política económica", "modelo"], []),  # Theoretical, no specific law
    (["internacionalización", "comercio exterior"], []),
    (["política monetaria", "euro", "SEBC"], []),
    (["sector primario", "sector industrial", "sector servicios", "turismo"], []),
    (["sector público económico", "empresas públicas"], []),
    (["Seguridad Social"], ["trebep"]),  # For funcionarios context
    (["Sistema Nacional de Salud"], []),
    (["sistema educativo"], []),
    (["mercado de trabajo", "empleo"], []),
    (["políticas de empleo", "desempleo"], []),
    (["I+D+i", "medioambiental"], []),
    (["Hacienda pública", "sector público"], ["lgp"]),
    (["Déficit público", "estabilidad"], ["loep"]),
    (["tasas", "contribuciones especiales"], ["lgp"]),
    (["Ley General Presupuestaria", "leyes anuales"], ["lgp"]),
    (["presupuestos generales", "clasificaciones presupuestarias"], ["lgp"]),
    (["modificaciones presupuestarias"], ["lgp"]),
    (["gasto público", "ejecución del gasto"], ["lgp"]),
    (["gastos de personal", "retribuciones"], ["lgp", "trebep"]),
    (["gastos contractuales", "obligaciones contractuales"], ["lcsp"]),
    (["subvenciones"], ["lgs"]),
    (["tesorería", "anticipos de caja"], ["lgp"]),
    
    # Bloque III - Recursos Humanos
    (["empleo público", "normativa"], ["trebep"]),
    (["régimen jurídico del personal", "clases de personal"], ["trebep"]),
    (["gestión del sistema de empleo"], ["trebep"]),
    (["planificación de recursos humanos", "Oferta de Empleo"], ["trebep"]),
    (["selección del personal", "procedimiento selectivo"], ["trebep"]),
    (["carrera profesional", "relaciones de puestos"], ["trebep"]),
    (["provisión de puestos", "concurso", "libre designación"], ["trebep"]),
    (["promoción interna", "pérdida de la condición"], ["trebep"]),
    (["formación", "aprendizaje"], ["trebep"]),
    (["situaciones administrativas"], ["trebep"]),
    (["derechos de los funcionarios", "jornada", "permisos"], ["trebep"]),
    (["régimen disciplinario"], ["trebep"]),
    (["sistema retributivo", "evaluación del desempeño"], ["trebep"]),
    (["nóminas"], ["trebep"]),
    (["incompatibilidades", "códigos de conducta"], ["trebep", "incomp"]),
    (["Seguridad Social de los funcionarios", "clases pasivas"], ["trebep"]),
    (["jubilación"], ["trebep"]),
    (["MUFACE", "mutualismo"], ["trebep"]),
    (["derechos colectivos", "representación", "negociación"], ["trebep", "lols"]),
    (["derecho del trabajo"], ["et"]),
    (["fuentes del ordenamiento laboral"], ["et"]),
    (["contrato de trabajo"], ["et"]),
    (["modalidades del contrato"], ["et"]),
    (["negociación colectiva", "convenios colectivos"], ["et", "lols"]),
]


def match_laws(titulo: str, bloque: str) -> list[str]:
    """Find matching law IDs for a tema based on title and bloque."""
    titulo_lower = titulo.lower()
    matched = set()
    
    for keywords, law_keys in RULES:
        for kw in keywords:
            if kw.lower() in titulo_lower:
                matched.update(law_keys)
                break
    
    # Always include CE for constitutional topics
    if "Constitución" in titulo or "constitucional" in titulo.lower():
        matched.add("ce")
    
    # Map keys to UUIDs
    return [LAWS[k] for k in matched if k in LAWS]


def main():
    client = httpx.Client(base_url=API, timeout=30)
    
    # Get all temas for oposicion
    opo_id = "37d75919-ccd4-41ff-b95f-001de0ca694b"
    temas = client.get(f"/temario/?oposicion_id={opo_id}").json()
    
    print(f"Processing {len(temas)} temas...")
    
    updated = 0
    for tema in temas:
        leyes = match_laws(tema["titulo"], tema.get("bloque", ""))
        
        if leyes:
            # Update tema with linked laws
            r = client.patch(
                f"/temario/{tema['id']}",
                json={"leyes_vinculadas": leyes}
            )
            if r.status_code == 200:
                updated += 1
                print(f"  ✓ Tema {tema['num_tema']} ({tema['bloque']}): {len(leyes)} leyes")
            else:
                print(f"  ✗ Tema {tema['num_tema']}: {r.status_code}")
        else:
            print(f"  - Tema {tema['num_tema']}: no laws matched")
    
    print(f"\nUpdated {updated}/{len(temas)} temas")
    
    # Mark oposicion as completed
    r = client.patch(
        f"/oposiciones/{opo_id}",
        json={"pipeline_state": "leyes_ok", "agente_activo": None}
    )
    if r.status_code == 200:
        print("✓ Oposición marked as leyes_ok")
    else:
        print(f"✗ Failed to update oposición: {r.status_code}")


if __name__ == "__main__":
    main()
