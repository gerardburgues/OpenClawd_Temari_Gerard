#!/usr/bin/env python3
"""
Populate TAC (Técnicos de la Administración Civil) temario from the official BOE source.
Based on Orden TDF/1156/2024, de 30 de octubre (Anexo II).
"""

import json
import urllib.request

API_BASE = "http://localhost:8001"
OPOSICION_ID = "306f1357-c501-4168-8659-f2a283686055"

# ============================================================================
# A. GRUPO DE MATERIAS COMUNES (114 temas)
# ============================================================================

MATERIAS_COMUNES = [
    # I. Ciencia Política (temas 1-10)
    ("A.I", 1, "El Estado y sus elementos constitutivos. Estado y Nación. La organización territorial del Estado. El sistema político español: su configuración constitucional y su evolución democrática."),
    ("A.I", 2, "Tipología de los regímenes políticos: los regímenes no democráticos. Las democracias y sus tipos. Partidos políticos. Grupos de interés y movimientos sociales. La opinión pública."),
    ("A.I", 3, "El pensamiento político: La teoría política en la Antigüedad, la Edad Media y la Edad Moderna. El pensamiento político en la España de los siglos XIX y XX."),
    ("A.I", 4, "Teorías de la democracia: la democracia mayoritaria, de consenso, deliberativa y participativa. Gobernanza democrática y valores públicos. Lucha contra la corrupción: instrumentos y foros internacionales."),
    ("A.I", 5, "La Monarquía y la Jefatura de Estado en las formas políticas del constitucionalismo. La Monarquía parlamentaria."),
    ("A.I", 6, "El Gobierno. Formación y estructura. Funciones del Gobierno. La responsabilidad política del Gobierno. Composición, organización y funciones del Gobierno español."),
    ("A.I", 7, "El poder legislativo. El Parlamento: estructura, composición y funciones. El Parlamento en España: Congreso de los Diputados y Senado. El bicameralismo."),
    ("A.I", 8, "El Poder Judicial y la organización de los tribunales de justicia. Administración de Justicia y tutela judicial efectiva. La organización judicial en España. El Consejo General del Poder Judicial. El Ministerio Fiscal."),
    ("A.I", 9, "Las formas de Estado. Los Estados unitarios y los Estados compuestos: confederación, federación, Estado regional y Estado autonómico. Modelos comparados de federalismo."),
    ("A.I", 10, "El pensamiento político y la configuración de la ciudadanía. Definiciones de ciudadanía. Modelos de ciudadanía. Ciudadanía e igualdad."),

    # II. Estructura económica y social de España (temas 11-28)
    ("A.II", 11, "Crecimiento y desarrollo. Desarrollo y sostenibilidad. Objetivos de Desarrollo Sostenible de la Agenda 2030. La medición del desarrollo y la calidad de vida. El caso español."),
    ("A.II", 12, "Características del crecimiento económico español en el siglo XX: las grandes etapas. Análisis de los principales factores del crecimiento económico español. El modelo de crecimiento económico español en el periodo 2000-2023. Tendencias, fortalezas y debilidades de la economía española."),
    ("A.II", 13, "Transformaciones estructurales de la economía española: sector agrario, industria y sector servicios. Los sectores productivos en España."),
    ("A.II", 14, "El sector exterior: exportación, importación, cuenta corriente y financiera. Los flujos de inversiones directas. Estructura geográfica y por productos del comercio exterior español. Balanza de pagos. Competitividad exterior de la economía española."),
    ("A.II", 15, "Población y capital humano en España. Dinámica, estructura y características de la población. Crecimiento económico, empleo y mercado de trabajo. Política de empleo."),
    ("A.II", 16, "Infraestructuras: definición, tipos, fuentes de financiación. Planificación de infraestructuras. Red de infraestructuras de transporte en España. Red de infraestructuras digitales."),
    ("A.II", 17, "La energía: planificación energética en España. Estructura del sector energético y sus principales características. Política energética en la Unión Europea. Transición ecológica."),
    ("A.II", 18, "Investigación, desarrollo e innovación en España. Estrategia y marco institucional de la investigación científica. Evaluación de la investigación. Grandes instalaciones científicas. Fomento de la innovación y emprendimiento. Transformación digital. Inteligencia artificial."),
    ("A.II", 19, "Demografía empresarial. Estructura y dinámica del tejido empresarial en España. Análisis del emprendimiento."),
    ("A.II", 20, "La Seguridad Social: el sistema de la Seguridad Social en España. Contingencias, acción protectora y regímenes. La Seguridad Social como pilar del Estado de bienestar. El pacto de Toledo y reformas del sistema de pensiones. El Fondo de Reserva de las pensiones."),
    ("A.II", 21, "Pobreza y desigualdad: distribución personal y territorial de la renta. Inclusión social. Políticas de cohesión social. El ingreso mínimo vital."),
    ("A.II", 22, "Discapacidad e inclusión. Definiciones y tipología. La protección a las personas con discapacidad en la normativa española. Principales cifras. Políticas de discapacidad. Accesibilidad universal."),
    ("A.II", 23, "Igualdad de género en España. Instituciones para la igualdad. Instrumentos de las políticas de igualdad. Políticas para prevenir y erradicar la violencia de género."),
    ("A.II", 24, "La familia en España: Marco institucional. Estructura del hogar. Políticas de protección a la familia."),
    ("A.II", 25, "Diversidad en España. Movimientos migratorios. Llegada e integración de inmigrantes. Emigración exterior. Principales cifras. Retos demográficos."),
    ("A.II", 26, "El sistema de educación y formación profesional en España. Marco institucional. Principales cifras. Modelos de evaluación."),
    ("A.II", 27, "El sistema sanitario español. Organización. Principales cifras. Salud pública. Planificación sanitaria."),
    ("A.II", 28, "Sistema de prestaciones sociales. El papel del Tercer Sector en España: su relación con las Administraciones Públicas."),

    # III. Turismo (temas 29-33)
    ("A.III", 29, "El turismo y su importancia estratégica en la economía española. Evolución del sector turístico. Principales cifras del turismo español."),
    ("A.III", 30, "Organismos del Estado competentes en materia de turismo. Actuación de la Administración General del Estado y la Política turística: la nueva Estrategia de Turismo Sostenible de España 2030."),
    ("A.III", 31, "La inteligencia turística. Análisis de los mercados turísticos emisores."),
    ("A.III", 32, "Diversificación de productos turísticos: turismo cultural, turismo verde o sostenible, turismo de salud, turismo idiomático. Promoción del turismo en el exterior: líneas de promoción turística internacional de España."),
    ("A.III", 33, "TURESPAÑA. Instituto de Turismo de España. Oficinas Españolas de Turismo. La marca España. Gestión de los Paradores de Turismo."),

    # IV. Relaciones internacionales y Unión Europea (temas 34-53)
    ("A.IV", 34, "El Derecho internacional público: concepto y fuentes. Relaciones entre Derecho internacional público y Derecho interno."),
    ("A.IV", 35, "La sociedad internacional. Los sujetos en Derecho Internacional. La subjetividad de los Estados y de las Organizaciones internacionales."),
    ("A.IV", 36, "La solución pacífica de conflictos internacionales. El régimen de la seguridad colectiva y el uso de la fuerza. Referencia especial al problema del terrorismo internacional."),
    ("A.IV", 37, "Teorías de las relaciones internacionales."),
    ("A.IV", 38, "El proceso de globalización: riesgos y oportunidades. Conceptos básicos de geopolítica. Principales actores en la escena internacional."),
    ("A.IV", 39, "La acción exterior del Estado. Ejes e instrumentos de la política exterior de España. La Marca España. El Servicio Europeo de Acción Exterior."),
    ("A.IV", 40, "La cooperación al desarrollo: origen, evolución, definición, actores e instrumentos."),
    ("A.IV", 41, "La cooperación española: origen, evolución, marco normativo e institucional. La Agenda 2030 para el Desarrollo Sostenible y la renovación de la política de cooperación española."),
    ("A.IV", 42, "El comercio internacional de bienes y servicios. Proteccionismo y librecambio. La OMC. Política comercial de la Unión Europea."),
    ("A.IV", 43, "Las inversiones directas en las empresas multinacionales. Tendencias actuales y distribución geográfica. La inversión directa extranjera en España. La empresa española en el exterior."),
    ("A.IV", 44, "El sistema monetario internacional: evolución histórica. Problemas de coordinación monetaria y financiera. El euro y el papel del Banco Central Europeo."),
    ("A.IV", 45, "El proceso de integración europea. La Unión Europea: estructura y funcionamiento. El sistema institucional y decisorio de la Unión Europea."),
    ("A.IV", 46, "Los procedimientos de toma de decisiones en la Unión Europea: actos normativos. El control del Tribunal de Justicia de la Unión Europea. Efectos del Derecho de la Unión Europea en el ordenamiento jurídico de los Estados Miembros."),
    ("A.IV", 47, "El mercado interior de la Unión Europea. Las políticas de la Unión Europea: políticas internas."),
    ("A.IV", 48, "Las políticas económicas de la Unión Europea: la Política Económica y Monetaria, el Pacto de Estabilidad y Crecimiento. El Pacto Verde Europeo y su encaje con el resto de las políticas de la Unión."),
    ("A.IV", 49, "Los fondos europeos: especial referencia al Mecanismo de Recuperación y Resiliencia."),
    ("A.IV", 50, "Organización de las Naciones Unidas: génesis histórica, estructura y competencias. Los órganos principales de Naciones Unidas. Organismos especializados y agencias del Sistema de Naciones Unidas."),
    ("A.IV", 51, "Las organizaciones internacionales de carácter económico: El Fondo Monetario Internacional. El Banco Mundial. La Organización para la Cooperación y el Desarrollo Económico. La Organización Mundial del Comercio."),
    ("A.IV", 52, "La Organización del Tratado del Atlántico Norte. Organización para la Seguridad y la Cooperación en Europa. El sistema de seguridad del Consejo de Europa."),
    ("A.IV", 53, "Organizaciones de ámbito americano, africano y asiático. El papel de España en las organizaciones internacionales."),

    # V. Derecho público (temas 54-80)
    ("A.V", 54, "Las Constituciones españolas. Constitucionalismo histórico español."),
    ("A.V", 55, "La Constitución española de 1978. Génesis y características. Estructura. El procedimiento de reforma."),
    ("A.V", 56, "Los principios constitucionales. Los valores superiores. El Estado de Derecho. La soberanía nacional. El Estado social. El Estado autonómico."),
    ("A.V", 57, "Los derechos fundamentales (I). Génesis, evolución y garantías de los derechos fundamentales. Los derechos derivados de la dignidad de la persona. Los derechos derivados del principio de libertad."),
    ("A.V", 58, "Los derechos fundamentales (II). Derechos derivados del principio de igualdad. Los derechos de participación política. El recurso de amparo constitucional. La suspensión de los derechos fundamentales."),
    ("A.V", 59, "Los principios rectores de la política económica y social en la Constitución española. Políticas de protección a las personas en situación de vulnerabilidad."),
    ("A.V", 60, "La Corona en la Constitución española de 1978."),
    ("A.V", 61, "El Tribunal Constitucional. Composición, designación y organización. Funciones del Tribunal Constitucional: el recurso de inconstitucionalidad. La cuestión de inconstitucionalidad. Los conflictos constitucionales."),
    ("A.V", 62, "Las Cortes Generales en la Constitución española. Composición y funciones. El Defensor del Pueblo. El Tribunal de Cuentas."),
    ("A.V", 63, "La elaboración de las leyes. Leyes orgánicas. El Derecho de la Unión Europea y su transposición. El control parlamentario del Gobierno."),
    ("A.V", 64, "El Gobierno en la Constitución española."),
    ("A.V", 65, "El Poder Judicial en la Constitución. El Consejo General del Poder Judicial. El Tribunal Supremo. El Ministerio Fiscal."),
    ("A.V", 66, "La Administración en la Constitución. El modelo español de distribución de competencias. Las Administraciones públicas. Principios de actuación de la Administración pública. El ciudadano como centro de la actuación administrativa."),
    ("A.V", 67, "El Estado autonómico (I). Organización del Estado y distribución del poder. El proceso autonómico: la definición de los principios del Estado Autonómico en el Título Preliminar y en el Título VIII de la Constitución. El estatuto de autonomía: elaboración y reforma. La asunción de competencias."),
    ("A.V", 68, "El Estado autonómico (II). Las relaciones entre el Estado y las Comunidades Autónomas. El control estatal sobre la actividad de las Comunidades Autónomas. Las relaciones de las Comunidades Autónomas entre sí. La cooperación entre Administraciones Públicas. Conferencias Sectoriales. Órganos de Cooperación."),
    ("A.V", 69, "El régimen local: la Administración local en la Constitución. La Ley de Bases del Régimen Local y demás normativa básica. Competencias. Elementos del municipio: territorio, población, organización. Otras Entidades Locales."),
    ("A.V", 70, "La Administración General del Estado. Órganos superiores y directivos de la Administración. La organización ministerial. Los Ministros, Secretarios de Estado, Subsecretarios y Directores Generales. Secretarios Generales y Secretarios Generales Técnicos."),
    ("A.V", 71, "El sector público institucional. Los organismos públicos. Las entidades de Derecho público vinculadas o dependientes de la Administración General del Estado. Las autoridades administrativas independientes. Los consorcios. Las fundaciones del sector público. Los fondos carentes de personalidad jurídica. Las sociedades mercantiles estatales."),
    ("A.V", 72, "La Administración General del Estado en el exterior. El Servicio Exterior del Estado. Misiones diplomáticas, representaciones permanentes y oficinas consulares."),
    ("A.V", 73, "La Administración periférica del Estado. Los Delegados del Gobierno. Subdelegados del Gobierno y Directores Insulares."),
    ("A.V", 74, "El acto administrativo. Requisitos: competencia, procedimiento y forma. La motivación de los actos administrativos. La eficacia del acto administrativo: ejecutividad y condiciones."),
    ("A.V", 75, "La teoría de la invalidez del acto administrativo: actos nulos y anulables. Convalidación. Conversión. Conservación. Revisión de oficio."),
    ("A.V", 76, "El procedimiento administrativo común. Fases. Motivación y forma. El silencio administrativo. La eficacia de los actos administrativos. La revisión de los actos en vía administrativa."),
    ("A.V", 77, "Los contratos del sector público. Ámbito subjetivo. Tipología de contratos. Preparación, adjudicación, efectos, modificación y extinción de los contratos de las Administraciones públicas. Régimen del contrato menor."),
    ("A.V", 78, "Formas de la actuación administrativa: la actividad de policía, fomento y servicio público. Subvenciones. La potestad sancionadora de la Administración. La responsabilidad de las Administraciones Públicas."),
    ("A.V", 79, "Los recursos administrativos. El recurso contencioso administrativo."),
    ("A.V", 80, "La elaboración de normas por la Administración. Los principios de buena regulación. Calidad normativa. Evaluación ex ante y ex post. La adaptación normativa a la economía digital."),

    # VI. Gestión pública (temas 81-114)
    ("A.VI", 81, "La planificación de la gestión pública. Planes Estratégicos. Indicadores de gestión."),
    ("A.VI", 82, "La Ley del Procedimiento Administrativo Común de las Administraciones Públicas y la Ley de Régimen Jurídico del Sector Público. Antecedentes y contexto. Estructura y contenido."),
    ("A.VI", 83, "Las medidas de simplificación administrativa: reducción de cargas y tramitación. Silencio positivo. Buenas prácticas. Las conferencias sectoriales en materia de simplificación administrativa."),
    ("A.VI", 84, "Gobernanza pública, gobierno abierto y participación ciudadana. Acceso a la información pública. Reutilización de la información del sector público."),
    ("A.VI", 85, "Integridad y ética pública. Marcos de integridad. Los códigos éticos y de conducta."),
    ("A.VI", 86, "Evaluación de políticas públicas e institucionalización de la evaluación. La Agencia Estatal de Evaluación de Políticas Públicas. Metodologías de evaluación. Indicadores."),
    ("A.VI", 87, "Régimen jurídico del personal al servicio de las Administraciones Públicas: personal funcionario y personal laboral. Derechos y deberes de los empleados públicos. La provisión de puestos de trabajo. Situaciones administrativas. Incompatibilidades."),
    ("A.VI", 88, "Selección del personal al servicio de las Administraciones Públicas. La carrera profesional: horizontal, vertical y la promoción interna. La formación de los empleados públicos."),
    ("A.VI", 89, "Políticas de personal en materia de igualdad de género: fundamentos, medidas e instrumentos. Políticas de inclusión de personas con discapacidad."),
    ("A.VI", 90, "Administración electrónica: marco conceptual y normativo. Servicios electrónicos a los ciudadanos. La gobernanza de la administración digital en la Administración General del Estado."),
    ("A.VI", 91, "Identidad digital y firma electrónica. El procedimiento administrativo electrónico. Registro, archivo y notificaciones electrónicas. Sede electrónica asociada y Punto de Acceso General electrónico. Plataformas de intermediación."),
    ("A.VI", 92, "El Plan de Recuperación, Transformación y Resiliencia: estructura, principios, gobernanza y gestión."),
    ("A.VI", 93, "La protección de datos. Régimen aplicable. Responsable y encargado del tratamiento. La Agencia Española de Protección de Datos. Los delegados de protección de datos en las Administraciones Públicas."),
    ("A.VI", 94, "Ciberseguridad: amenazas y medidas de respuesta. El Centro Criptológico Nacional. CCN-CERT. Mecanismos de cooperación público-privada en materia de ciberseguridad."),
    ("A.VI", 95, "El sistema español de ciencia, tecnología e innovación. La Ley de la Ciencia, la Tecnología y la Innovación. Convocatoria de proyectos. La Agencia Estatal de Investigación. El Centro para el Desarrollo Tecnológico y la Innovación (CDTI)."),
    ("A.VI", 96, "Transformación digital e inteligencia artificial en el sector público. Estrategia de Inteligencia Artificial. Procesamiento del lenguaje natural y asistentes virtuales. Automatización de procesos."),
    ("A.VI", 97, "El patrimonio de las Administraciones Públicas. Bienes de dominio público y bienes patrimoniales. Régimen jurídico. Gestión de inmuebles del Estado."),
    ("A.VI", 98, "La gestión de los recursos humanos. Planificación y programación. Dimensionamiento de plantillas. Análisis y clasificación de puestos de trabajo. Evaluación del desempeño."),
    ("A.VI", 99, "Dirección y gestión de proyectos. Instrumentos y técnicas de gestión de proyectos. Gestión de riesgos. Contratación: pliego de cláusulas y pliego de prescripciones técnicas."),
    ("A.VI", 100, "La gestión de servicios públicos. Formas de gestión. Calidad de los servicios públicos. Cartas de Servicios. Atención a la ciudadanía. Gestión de quejas y sugerencias."),
    ("A.VI", 101, "Fundamentos y componentes de un sistema de gestión de la calidad y la excelencia en el ámbito público. Las normas ISO de calidad. El modelo EFQM. La mejora continua de los procesos."),
    ("A.VI", 102, "Las políticas públicas. Las fases del proceso de elaboración de políticas públicas. Evaluación y agenda. Formulación e implementación. Evaluación de resultados."),
    ("A.VI", 103, "La organización de la seguridad: Consejo de Seguridad Nacional. El Sistema de Seguridad Nacional. Los Departamentos de Seguridad Nacional."),
    ("A.VI", 104, "Riesgos y amenazas a la seguridad nacional. Principales agentes de riesgos y amenazas a la seguridad nacional. Las líneas de acción estratégica. Ámbitos de especial interés: seguridad económica, la protección de infraestructuras críticas."),
    ("A.VI", 105, "Comunicación institucional y corporativa. Gestión de la comunicación. La información administrativa: planes de comunicación. Marketing público. Tecnología e innovación en la comunicación institucional."),
    ("A.VI", 106, "Principales magnitudes del sector público. El gasto público. La composición del gasto público en España."),
    ("A.VI", 107, "El presupuesto como instrumento de gestión pública. Técnicas de presupuestación. La presupuestación con enfoque de género."),
    ("A.VI", 108, "El presupuesto del Estado en España: marco normativo. Estructura y contenido. Fases del ciclo presupuestario. Los Presupuestos Generales del Estado: elaboración, aprobación, ejecución y control."),
    ("A.VI", 109, "Los ingresos públicos: concepto, naturaleza y clasificación. El impuesto: concepto y tipos. Técnicas de medición de la progresividad. Efectos económicos de los impuestos."),
    ("A.VI", 110, "La estructura del sistema tributario español: imposición directa e indirecta. Principales figuras tributarias. Financiación de las Comunidades Autónomas y de los Entes Locales."),
    ("A.VI", 111, "Contabilidad pública: conceptos generales. La Ley General Presupuestaria. El Plan General de Contabilidad Pública. Cuentas anuales."),
    ("A.VI", 112, "La sostenibilidad de las finanzas públicas. Exigencias de la Unión Europea. La Ley Orgánica de Estabilidad Presupuestaria y Sostenibilidad Financiera."),
    ("A.VI", 113, "El control interno de la gestión económico-financiera del sector público estatal: La Intervención General de la Administración del Estado. Control externo: el Tribunal de Cuentas."),
    ("A.VI", 114, "Economía española de la pandemia Covid. La crisis sanitaria, económica y social. Los instrumentos de respuesta a la crisis: ERTE, ICO, IMV. El impulso a la digitalización y a la sostenibilidad."),
]

# ============================================================================
# B. GRUPO DE MATERIAS ESPECÍFICAS
# ============================================================================

# 1. Materias Jurídicas (52 temas)
MATERIAS_JURIDICAS = [
    # I. Fuentes del Derecho y jurisdicción constitucional (temas 1-16)
    ("B.1.I", 1, "Los orígenes históricos del Derecho constitucional. Las revoluciones liberales del siglo XVIII y XIX: América y Europa. El liberalismo y la garantía de los derechos individuales."),
    ("B.1.I", 2, "El concepto de Constitución. La Constitución del constitucionalismo. Principios estructurales de la Constitución. Constitución y otras fuentes del Derecho."),
    ("B.1.I", 3, "La posición de la Constitución en el sistema de fuentes. Límites a la Ley. Procedimiento de reforma de la Constitución. Garantía jurisdiccional de la Constitución."),
    ("B.1.I", 4, "Las leyes orgánicas. Las leyes ordinarias. El procedimiento legislativo y sus especialidades."),
    ("B.1.I", 5, "Las normas con rango de ley emanadas del Gobierno: el Decreto-Ley, el Decreto Legislativo."),
    ("B.1.I", 6, "Los Tratados Internacionales: posición en el sistema de fuentes del Derecho. La relación entre el Derecho internacional público y los ordenamientos estatales: teorías."),
    ("B.1.I", 7, "La doctrina de los derechos fundamentales. Teoría general y raíces filosóficas. Tipología. Doble dimensión de los derechos fundamentales. La protección supranacional: el Convenio Europeo de Derechos Humanos."),
    ("B.1.I", 8, "El recurso de inconstitucionalidad. Las cuestiones de inconstitucionalidad. La autocuestión de inconstitucionalidad. Los efectos de las sentencias de inconstitucionalidad."),
    ("B.1.I", 9, "Los conflictos de competencias entre el Estado y las Comunidades Autónomas. Conflictos positivos y negativos. Conflictos de atribuciones entre órganos constitucionales. Conflictos en defensa de la autonomía local. Impugnaciones del Título V LOTC."),
    ("B.1.I", 10, "El recurso de amparo. Legitimación y objeto. Tramitación del recurso de amparo. Efectos de la sentencia que resuelve el recurso de amparo."),
    ("B.1.I", 11, "La incorporación de España a la Unión Europea y las consecuencias para el sistema constitucional. El artículo 93 de la Constitución española. Los derechos fundamentales en la Unión Europea: la Carta de Derechos Fundamentales de la Unión Europea."),
    ("B.1.I", 12, "La potestad reglamentaria: titularidad. Clases de reglamentos. Límites de la potestad reglamentaria. El procedimiento de elaboración de disposiciones administrativas de carácter general."),
    ("B.1.I", 13, "Las formas de organización territorial en España: evolución y rasgos actuales. El Estado autonómico en la Constitución de 1978. Las competencias del Estado y de las Comunidades Autónomas."),
    ("B.1.I", 14, "La distribución de competencias entre el Estado y las Comunidades Autónomas. Competencias exclusivas y compartidas. Análisis de los principales títulos competenciales del Estado. La cláusula residual del artículo 149.3 CE."),
    ("B.1.I", 15, "La relación entre el ordenamiento estatal y los ordenamientos autonómicos. Leyes de armonización. Cláusula de prevalencia y de supletoriedad del Derecho estatal."),
    ("B.1.I", 16, "El proceso de elaboración normativa de la Unión Europea. La incorporación del Derecho de la Unión Europea en el ordenamiento español. Procedimientos de infracción de la normativa de la Unión Europea."),

    # II. Organización y actuación de las Administraciones Públicas (temas 17-36)
    ("B.1.II", 17, "El Derecho Administrativo: concepto y contenido. El modelo español de Derecho Administrativo: evolución y rasgos actuales. El ordenamiento administrativo: la Administración y las fuentes del Derecho."),
    ("B.1.II", 18, "Organización administrativa. Órganos administrativos: concepto, elementos y clases. Competencia: concepto y clases. Principios de coordinación, cooperación y colaboración. Delegación, avocación, desconcentración y encomienda de gestión. El conflicto de atribuciones."),
    ("B.1.II", 19, "La relación jurídico-administrativa: concepto y elementos. La posición jurídica de la Administración: potestades y prerrogativas."),
    ("B.1.II", 20, "Los ciudadanos en sus relaciones con la Administración: derechos y deberes. La relación de sujeción especial. Derechos de los ciudadanos y posición jurídica de los ciudadanos ante los procedimientos administrativos."),
    ("B.1.II", 21, "El servicio público. Modalidades de gestión de los servicios públicos. La externalización de los servicios públicos. Gestión directa e indirecta. Regulación económica: concepto. Regulación de industrias de red. Autoridades independientes de supervisión y control."),
    ("B.1.II", 22, "Principios de la potestad sancionadora. El procedimiento sancionador: especialidades."),
    ("B.1.II", 23, "La responsabilidad patrimonial de las Administraciones Públicas: evolución y régimen vigente. Características. Presupuestos. Daños indemnizables."),
    ("B.1.II", 24, "Los recursos administrativos: principios generales. Clases de recursos. Recurso de alzada. Recurso de reposición. Recurso extraordinario de revisión."),
    ("B.1.II", 25, "La jurisdicción contencioso-administrativa: origen, evolución y régimen vigente. Organización de la jurisdicción contencioso-administrativa. Distribución de la competencia."),
    ("B.1.II", 26, "El recurso contencioso-administrativo: los actos impugnables. Las partes. La pretensión contencioso-administrativa. El procedimiento de primera instancia. Las medidas cautelares."),
    ("B.1.II", 27, "Las sentencias: tipos y efectos. Los procesos especiales de la LJCA."),
    ("B.1.II", 28, "Los recursos en la jurisdicción contencioso-administrativa: el recurso de apelación. El recurso de casación: la reforma operada por la Ley Orgánica 7/2015, de 21 de julio. El recurso de revisión."),
    ("B.1.II", 29, "El contrato administrativo. El contrato de obras. El contrato de concesión de obras. El contrato de servicios. El contrato de concesión de servicios. El contrato de suministro. Otros contratos del sector público. Contrato mixto."),
    ("B.1.II", 30, "El régimen de adjudicación de los contratos públicos. Las formas de adjudicación de los contratos en las Directivas de contratación y en la legislación española: el procedimiento negociado sin publicidad y los procedimientos abiertos y restringidos. El diálogo competitivo y la asociación para la innovación. Protección jurídica del licitador."),
    ("B.1.II", 31, "Los efectos de los contratos administrativos. El ius variandi y el mantenimiento del equilibrio económico del contrato. El riesgo imprevisible y la cláusula de revisión de precios. Extinción de los contratos públicos."),
    ("B.1.II", 32, "El dominio público: concepto, naturaleza y elementos. Afectación y mutaciones demaniales. El régimen jurídico del dominio público: uso, aprovechamiento, protección y defensa. Las aguas terrestres. El demanio marítimo-terrestre."),
    ("B.1.II", 33, "Las propiedades especiales de las Administraciones Públicas. El régimen de los montes. Las vías pecuarias. El régimen de minas. El patrimonio histórico y cultural español."),
    ("B.1.II", 34, "Bienes patrimoniales del Estado: régimen de adquisición y disposición. El Patrimonio Nacional."),
    ("B.1.II", 35, "El Derecho urbanístico. Distribución constitucional de competencias entre Estado y Comunidades Autónomas: doctrina del Tribunal Constitucional. La clasificación del suelo: régimen jurídico. La valoración del suelo. El estatuto del propietario y la función social de la propiedad."),
    ("B.1.II", 36, "Los instrumentos de ordenación urbanística. La ejecución del planeamiento: los sistemas de actuación. Instrumentos de intervención en el mercado de suelo. La expropiación urbanística. Las licencias urbanísticas."),

    # III. Derecho de la Unión Europea y Derecho de la competencia (temas 37-52)
    ("B.1.III", 37, "Evolución del proceso de integración europea. Etapas. El Derecho originario de la Unión Europea: los Tratados fundacionales y su evolución. Especial referencia al Tratado de Lisboa."),
    ("B.1.III", 38, "Las instituciones de la Unión Europea (I): el Parlamento Europeo, el Consejo Europeo y el Consejo. Organización, competencias y funcionamiento."),
    ("B.1.III", 39, "Las instituciones de la Unión Europea (II): la Comisión Europea, el Tribunal de Justicia de la Unión Europea, el Banco Central Europeo y el Tribunal de Cuentas. Organización, competencias y funcionamiento."),
    ("B.1.III", 40, "Derecho derivado de la Unión Europea: los reglamentos, las directivas, las decisiones, las recomendaciones y los dictámenes. La elaboración del derecho de la Unión Europea."),
    ("B.1.III", 41, "Aplicación del derecho de la Unión Europea. Principios de primacía y de eficacia directa del derecho de la Unión Europea. Responsabilidad del Estado por incumplimiento del Derecho de la Unión."),
    ("B.1.III", 42, "Los procedimientos ante el Tribunal de Justicia. Cuestión prejudicial. Recurso de incumplimiento. Recurso de anulación. Recurso de omisión. Recurso por responsabilidad extracontractual. Los Tribunales especializados."),
    ("B.1.III", 43, "El mercado interior de la Unión Europea. Las cuatro libertades. Libre circulación de mercancías, personas, servicios y capitales."),
    ("B.1.III", 44, "Política de competencia de la Unión Europea: definición. La prohibición del abuso de la posición dominante. Las ayudas de Estado."),
    ("B.1.III", 45, "La defensa de la competencia en España: evolución, principios y objetivos. La Ley de defensa de la competencia. Las conductas colusorias y el abuso de posición de dominio. Análisis económico de la competencia. Otros ilícitos competitivos."),
    ("B.1.III", 46, "El control de las concentraciones económicas: régimen español y régimen de la Unión Europea. La Comisión Nacional de los Mercados y la Competencia: organización, funciones y competencias."),
    ("B.1.III", 47, "Las Directivas de la Unión Europea en materia de contratación pública. El recurso especial en materia de contratación pública: objeto y tribunal competente."),
    ("B.1.III", 48, "Instrumentos de colaboración público-privada: tipología. La colaboración público-privada: concepto, características, tipología y regulación en la Unión Europea."),
    ("B.1.III", 49, "El Derecho de la Unión Europea sobre servicios en el mercado interior: la Directiva de Servicios."),
    ("B.1.III", 50, "Los medios electrónicos en la Administración Pública: implicaciones jurídicas. El documento y el expediente electrónico. La firma electrónica. El Reglamento eIDAS."),
    ("B.1.III", 51, "Transparencia y gobierno abierto. La ley de transparencia y acceso a la información pública. Publicidad activa y derecho de acceso a la información. El Consejo de Transparencia."),
    ("B.1.III", 52, "Protección de datos de carácter personal. Régimen jurídico: El Reglamento General de Protección de Datos y la Ley Orgánica de Protección de Datos. Principios y derechos de protección de datos."),
]

# 2. Materias Sociales (52 temas)
MATERIAS_SOCIALES = [
    # I. Empleo público y protección social (temas 1-15)
    ("B.2.I", 1, "El personal al servicio de las Administraciones Públicas: clases. Adquisición y pérdida de la relación de servicio. Selección de los empleados públicos. La carrera profesional: horizontal, vertical y la promoción interna. La formación de los empleados públicos."),
    ("B.2.I", 2, "Planificación de los recursos humanos. Ordenación del empleo público. Instrumentos de planificación: planes de empleo, registros de personal, relaciones de puestos de trabajo y otras."),
    ("B.2.I", 3, "Los derechos de los funcionarios. Derechos económicos: retribuciones y pensiones. Las situaciones administrativas de los funcionarios."),
    ("B.2.I", 4, "La organización del trabajo y la jornada laboral. El teletrabajo. La conciliación de la vida personal, familiar y laboral. Medidas de corresponsabilidad. La ley del trabajo a distancia."),
    ("B.2.I", 5, "La evaluación del desempeño: concepto, marco normativo, fines e instrumentos. Modelos de evaluación del desempeño. Los principales sistemas de indicadores del desempeño."),
    ("B.2.I", 6, "La provisión de puestos de trabajo. Los deberes de los funcionarios. Las incompatibilidades. El régimen disciplinario. El código ético y de conducta. La protección de los trabajadores frente a riesgos laborales."),
    ("B.2.I", 7, "Personal laboral. La extinción de la relación de empleo público. Personal directivo. Órganos de representación. Negociación colectiva."),
    ("B.2.I", 8, "Protección social. Clases y características. El sistema de Seguridad Social en España. Su relación con el ámbito comunitario e internacional. La estructura del sistema de la Seguridad Social. El régimen general."),
    ("B.2.I", 9, "Incapacidad permanente: evolución histórica, concepto, protección, requisitos, prestaciones y procedimiento de gestión. La incapacidad temporal: concepto, protección, requisitos, prestaciones y procedimiento de gestión."),
    ("B.2.I", 10, "Protección por jubilación: concepto, modalidades, requisitos, prestación y procedimiento de gestión. Muerte y supervivencia: prestaciones y procedimiento de gestión."),
    ("B.2.I", 11, "Maternidad, paternidad, riesgo durante el embarazo y la lactancia natural: requisitos y procedimiento de gestión. Protección familiar. Cuidado de menores."),
    ("B.2.I", 12, "Protección por desempleo: régimen jurídico, campo de aplicación, requisitos, prestaciones y procedimiento de gestión."),
    ("B.2.I", 13, "Las pensiones no contributivas de invalidez y jubilación."),
    ("B.2.I", 14, "Las Mutualidades de funcionarios de la Administración General del Estado: mutualismo administrativo (MUFACE, ISFAS, MUGEJU). La acción protectora: régimen jurídico y procedimiento de gestión."),
    ("B.2.I", 15, "Las clases pasivas del Estado: régimen de clases pasivas y su extinción. Régimen jurídico y procedimiento de gestión."),

    # II. Trabajo, formación y relaciones laborales (temas 16-26)
    ("B.2.II", 16, "El trabajo por cuenta ajena: su regulación jurídica. El Estatuto de los Trabajadores. Contratos de trabajo: modalidades. El salario. La jornada de trabajo. Derechos y deberes laborales básicos."),
    ("B.2.II", 17, "La extinción del contrato de trabajo: supuestos, procedimiento y efectos. El despido: concepto, causas, efectos e impugnación. El Fondo de Garantía Salarial."),
    ("B.2.II", 18, "Libertad sindical. Los sindicatos: concepto, naturaleza, tipología y régimen jurídico. Representatividad sindical. Las asociaciones empresariales."),
    ("B.2.II", 19, "La negociación colectiva: concepto, clases. Los convenios colectivos: naturaleza, eficacia, contenido, negociación, ámbito de aplicación. La inaplicación de los convenios colectivos."),
    ("B.2.II", 20, "Conflictos colectivos de trabajo. Huelga: concepto, efectos, límites y procedimientos. Cierre patronal."),
    ("B.2.II", 21, "El mercado de trabajo en España. Actores y políticas. El Sistema Nacional de Empleo: organización y funciones."),
    ("B.2.II", 22, "Políticas activas de empleo. El Plan Anual de Políticas de Empleo. Programas para la empleabilidad. Políticas activas y prestaciones."),
    ("B.2.II", 23, "El marco institucional del empleo: la Organización Internacional del Trabajo. Competencias de la Unión Europea en materia de empleo. Estrategia Europea de Empleo: evolución. El Fondo Social Europeo."),
    ("B.2.II", 24, "Cualificaciones y formación profesional. El sistema de cualificaciones. El Catálogo Nacional de Cualificaciones Profesionales."),
    ("B.2.II", 25, "El Sistema de Formación Profesional para el empleo en el ámbito laboral. La Fundación Estatal para la Formación en el Empleo (Fundae). Formación de oferta y demanda. Financiación."),
    ("B.2.II", 26, "La Inspección de Trabajo y Seguridad Social: naturaleza, organización, funciones y competencias. Procedimientos de actuación. El Organismo Estatal de Inspección de Trabajo y Seguridad Social."),

    # III. Educación, cultura y deporte (temas 27-39)
    ("B.2.III", 27, "Educación: marco constitucional. Distribución de competencias. El derecho a la educación y la libertad de enseñanza. El sistema educativo español. La Alta Inspección de Educación."),
    ("B.2.III", 28, "Educación infantil, primaria y secundaria. La formación profesional: clases, estructura y diseño curricular."),
    ("B.2.III", 29, "Los programas europeos de educación. Becas y ayudas al estudio: legislación y regímenes."),
    ("B.2.III", 30, "La educación universitaria. Acceso y admisión. Espacio Europeo de Educación Superior. Autonomía universitaria. Verificación y acreditación de títulos. Agencias de calidad."),
    ("B.2.III", 31, "Cultura: marco constitucional. Distribución de competencias. Protección del patrimonio histórico español. Patrimonio cultural de la Humanidad."),
    ("B.2.III", 32, "Archivos de la Administración General del Estado. Patrimonio bibliográfico y bibliotecas. Patrimonio documental y museos. Museos de titularidad y gestión estatal. Propiedad intelectual."),
    ("B.2.III", 33, "Promoción y difusión de la cultura. Los organismos públicos estatales en materia de cultura. El mecenazgo y el patrocinio. La Acción cultural exterior del Estado."),
    ("B.2.III", 34, "La industria cinematográfica y audiovisual. Medidas de fomento a la cinematografía y el sector audiovisual. El Instituto de la Cinematografía y de las Artes Audiovisuales."),
    ("B.2.III", 35, "Deporte: marco constitucional. Distribución de competencias. Legislación deportiva estatal. La estructura del deporte: entidades deportivas. El Consejo Superior de Deportes."),
    ("B.2.III", 36, "El deporte profesional y de alto nivel. La Agencia Española de Protección de la Salud en el Deporte. La lucha contra el dopaje. Las competiciones deportivas. El deporte y la Unión Europea."),
    ("B.2.III", 37, "Comunicación audiovisual: concepto. La comunicación audiovisual: marco constitucional y distribución de competencias."),
    ("B.2.III", 38, "Regulación y autorización de los servicios de comunicación audiovisual. La Comisión Nacional de los Mercados y la Competencia. Los medios de comunicación de titularidad estatal."),
    ("B.2.III", 39, "El servicio postal universal. La regulación del sector postal. Sociedad Estatal Correos y Telégrafos."),

    # IV. Políticas de igualdad y servicios sociales (temas 40-52)
    ("B.2.IV", 40, "Igualdad de género: marco constitucional. Distribución de competencias. Políticas de igualdad: instituciones, planes e instrumentos."),
    ("B.2.IV", 41, "Violencia de género: concepto y tipos. Legislación estatal. Instrumentos y recursos para la prevención, detección y atención de la violencia de género. El Pacto de Estado contra la Violencia de Género."),
    ("B.2.IV", 42, "Infancia y adolescencia: protección jurídica. Políticas de apoyo a la familia e infancia. Estrategia de Erradicación de la Violencia contra la Infancia. Menores extranjeros no acompañados."),
    ("B.2.IV", 43, "Juventud: legislación estatal. Organismos competentes en materia de juventud. El Instituto de la Juventud. Políticas de juventud."),
    ("B.2.IV", 44, "Discapacidad: concepto, tipos y prevalencia. Marco constitucional. Distribución de competencias. Las personas con discapacidad: derechos, protección y políticas públicas."),
    ("B.2.IV", 45, "Los servicios sociales y su marco normativo. Distribución de competencias. Estructura del sistema de servicios sociales. El Tercer Sector de Acción Social."),
    ("B.2.IV", 46, "El Sistema para la Autonomía y Atención a la Dependencia: regulación, organización, recursos y gestión."),
    ("B.2.IV", 47, "Pobreza y exclusión social: indicadores y principales datos en España. Políticas de lucha contra la pobreza y la exclusión social. El ingreso mínimo vital."),
    ("B.2.IV", 48, "Inmigración y extranjería: marco constitucional. Distribución de competencias. Legislación de extranjería: entrada, permanencia, trabajo, infracciones y sanciones."),
    ("B.2.IV", 49, "Protección internacional: regulación. El sistema común europeo de asilo. Apatridia. Desplazados temporales."),
    ("B.2.IV", 50, "Personas mayores: demografía, situación socioeconómica y principales datos en España. Envejecimiento activo. Políticas de atención a las personas mayores."),
    ("B.2.IV", 51, "Voluntariado: concepto, evolución y marco normativo. El voluntariado en la Administración General del Estado. Promoción del voluntariado."),
    ("B.2.IV", 52, "Drogodependencias: evolución del consumo y efectos. Planes, estrategias e instrumentos de intervención. Delegación del Gobierno para el Plan Nacional sobre Drogas."),
]

# 3. Materias Económicas (52 temas)
MATERIAS_ECONOMICAS = [
    # I. Sistema tributario y financiación pública (temas 1-21)
    ("B.3.I", 1, "El tributo: concepto, fines y clases. Los elementos del tributo. Hecho imponible. Base imponible y base liquidable. Cuota tributaria. La deuda tributaria."),
    ("B.3.I", 2, "Los obligados tributarios: el sujeto pasivo. Responsables. La capacidad de obrar en el orden tributario."),
    ("B.3.I", 3, "La aplicación de los tributos. Información y asistencia a los obligados tributarios. Comprobación e investigación. La gestión tributaria. Las declaraciones y autoliquidaciones."),
    ("B.3.I", 4, "La inspección de los tributos. El procedimiento de inspección: iniciación, desarrollo y terminación."),
    ("B.3.I", 5, "La recaudación tributaria. Período voluntario y ejecutivo. Medidas cautelares. El procedimiento de apremio. Aplazamiento y fraccionamiento del pago. Compensación. Condonación. Prescripción."),
    ("B.3.I", 6, "Infracciones y sanciones tributarias: concepto y clases. Procedimiento sancionador. Delitos contra la Hacienda Pública."),
    ("B.3.I", 7, "Revisión de actos tributarios en vía administrativa. Procedimientos especiales de revisión. El recurso de reposición. Las reclamaciones económico-administrativas."),
    ("B.3.I", 8, "La Agencia Estatal de Administración Tributaria: creación, naturaleza, organización y funciones."),
    ("B.3.I", 9, "El impuesto sobre la renta de las personas físicas: naturaleza. Hecho imponible. Sujeto pasivo. Base imponible y liquidable. Cuota. Deducciones."),
    ("B.3.I", 10, "El impuesto sobre sociedades: naturaleza. Hecho imponible. Sujeto pasivo. Base imponible. Tipos de gravamen. Deducciones y bonificaciones."),
    ("B.3.I", 11, "El impuesto sobre el valor añadido: naturaleza. Operaciones gravadas. Base imponible. Sujeto pasivo. El tipo de gravamen. Liquidación del impuesto. Regímenes especiales."),
    ("B.3.I", 12, "Los impuestos especiales: naturaleza. Clases. Hecho imponible. Sujeto pasivo. Base imponible. Tipos de gravamen. Impuestos especiales de fabricación."),
    ("B.3.I", 13, "La Hacienda de las Comunidades Autónomas: principios constitucionales. El sistema de financiación de las Comunidades Autónomas: evolución. Los tributos propios de las Comunidades Autónomas. Los tributos cedidos."),
    ("B.3.I", 14, "La Hacienda de las Entidades Locales: principios constitucionales. El sistema de financiación local: evolución. Tributos propios. Participación en tributos del Estado y de las Comunidades Autónomas."),
    ("B.3.I", 15, "La deuda pública: concepto, clases y régimen jurídico. Procedimientos de emisión de deuda pública. El Tesoro Público: organización y funciones."),
    ("B.3.I", 16, "El presupuesto de la Unión Europea: principios, estructura, procedimiento de elaboración y ejecución. Los recursos propios de la Unión Europea. Los principales capítulos de gasto del presupuesto europeo."),
    ("B.3.I", 17, "Análisis del sector público: el gasto público: concepto y clasificación. El crecimiento del gasto público. Teorías explicativas."),
    ("B.3.I", 18, "La hacienda pública y la asignación de recursos. El análisis coste-beneficio y otras técnicas de evaluación de decisiones públicas."),
    ("B.3.I", 19, "La hacienda pública y la redistribución de la renta. Instrumentos redistributivos. El debate sobre la eficiencia y la equidad."),
    ("B.3.I", 20, "La hacienda pública y la estabilización económica. La política fiscal. El déficit público: concepto, tipos y financiación. Efectos económicos del déficit público."),
    ("B.3.I", 21, "Los principios constitucionales de la política presupuestaria. La estabilidad presupuestaria. Sostenibilidad financiera. Regla de gasto. Fondo de contingencia."),

    # II. Gestión presupuestaria y control del gasto (temas 22-37)
    ("B.3.II", 22, "El presupuesto del Estado en España (I). Evolución y marco normativo. Ámbito institucional. Principios presupuestarios. Las reglas de contenido del presupuesto."),
    ("B.3.II", 23, "El presupuesto del Estado en España (II). Estructura: los estados de gastos e ingresos. Clasificación de los créditos presupuestarios."),
    ("B.3.II", 24, "Procedimiento de elaboración y aprobación de los Presupuestos Generales del Estado. Las técnicas de presupuestación: evolución y tendencias actuales."),
    ("B.3.II", 25, "Ejecución del presupuesto de gastos (I). Gestión de los créditos presupuestarios. Principio de especialidad. Modificaciones presupuestarias."),
    ("B.3.II", 26, "Ejecución del presupuesto de gastos (II). Ordenación del gasto y del pago. Gastos de personal. Gastos de contratación."),
    ("B.3.II", 27, "Ejecución del presupuesto de gastos (III). Subvenciones públicas: concepto, tipos, procedimiento de concesión y gestión. La Ley General de Subvenciones."),
    ("B.3.II", 28, "Ejecución del presupuesto de gastos (IV). Los pagos: concepto y requisitos. La cuenta de pagos librados. Pagos del Tesoro. Anticipos de caja fija. Pagos a justificar."),
    ("B.3.II", 29, "Ingresos públicos: concepto y clasificación. Gestión presupuestaria de los ingresos. Devoluciones de ingresos. Derechos de cobro. Ingresos no tributarios."),
    ("B.3.II", 30, "Cierre del ejercicio presupuestario. Remanentes de crédito. Obligaciones de ejercicios cerrados. Derechos de cobro de ejercicios cerrados."),
    ("B.3.II", 31, "Contabilidad pública: conceptos generales. La Ley General Presupuestaria. El Plan General de Contabilidad Pública: principios y estructura."),
    ("B.3.II", 32, "Cuentas anuales del sector público estatal: contenido y formación. La Cuenta General del Estado: contenido, elaboración y rendición."),
    ("B.3.II", 33, "El control de la actividad financiera del sector público: concepto y clases. El control interno: ámbito subjetivo. Control de legalidad. Control financiero permanente. Auditoría pública."),
    ("B.3.II", 34, "El Tribunal de Cuentas: organización y funciones. Procedimiento de fiscalización. Enjuiciamiento contable. Relación con las instituciones de control externo de las Comunidades Autónomas y de la Unión Europea."),
    ("B.3.II", 35, "Los presupuestos de los organismos autónomos y entidades públicas empresariales: régimen presupuestario y de control. Los presupuestos de las sociedades mercantiles estatales."),
    ("B.3.II", 36, "El régimen económico-financiero de las Comunidades Autónomas. Presupuesto. Tesorería. Endeudamiento. Contabilidad. Control interno y externo."),
    ("B.3.II", 37, "El régimen económico-financiero de las Entidades Locales. Presupuesto. Tesorería. Endeudamiento. Contabilidad. Control interno y externo."),

    # III. Análisis económico y estadística (temas 38-52)
    ("B.3.III", 38, "Análisis macroeconómico: oferta y demanda agregadas. Renta nacional: conceptos, componentes y distribución. Determinación de la renta de equilibrio."),
    ("B.3.III", 39, "Dinero y sistema financiero. Oferta y demanda de dinero. El sistema bancario y la creación de dinero. Instrumentos de política monetaria. El Banco Central Europeo."),
    ("B.3.III", 40, "Inflación: concepto y medición. Teorías explicativas. Efectos económicos. Políticas anti-inflacionistas."),
    ("B.3.III", 41, "Paro: concepto y medición. Teorías explicativas. Efectos económicos. Políticas de empleo."),
    ("B.3.III", 42, "El mercado de trabajo: oferta y demanda de trabajo. El salario. Teorías del mercado de trabajo."),
    ("B.3.III", 43, "La economía abierta: balanza de pagos. Tipo de cambio: concepto y regímenes. Mercado de divisas."),
    ("B.3.III", 44, "Análisis microeconómico: teoría de la demanda. Utilidad y preferencias. Restricción presupuestaria. Elección del consumidor. Curvas de indiferencia."),
    ("B.3.III", 45, "Teoría de la oferta: la producción. Los costes de producción. La maximización del beneficio. Tipos de mercado: competencia perfecta, monopolio y oligopolio."),
    ("B.3.III", 46, "Fallos de mercado: bienes públicos, externalidades, información asimétrica. Intervención del sector público: justificación y límites."),
    ("B.3.III", 47, "Estadística descriptiva: conceptos básicos. Medidas de posición y dispersión. Análisis de distribuciones de frecuencias."),
    ("B.3.III", 48, "Estadística inferencial: muestreo. Estimación e intervalos de confianza. Contraste de hipótesis."),
    ("B.3.III", 49, "Análisis de regresión: regresión lineal simple y múltiple. Interpretación y evaluación del modelo."),
    ("B.3.III", 50, "Indicadores económicos: concepto y tipos. Principales indicadores coyunturales de la economía española."),
    ("B.3.III", 51, "Las cuentas nacionales: concepto y estructura. El Sistema Europeo de Cuentas Nacionales (SEC). Principales agregados macroeconómicos."),
    ("B.3.III", 52, "Estadísticas demográficas: fuentes. Principales indicadores demográficos. La medición de los fenómenos migratorios."),
]

# 4. Materias Técnicas (52 temas)
MATERIAS_TECNICAS = [
    # I. Tecnologías de la información y las comunicaciones (temas 1-14)
    ("B.4.I", 1, "Las tecnologías de la información y la comunicación: evolución y tendencias. La transformación digital del sector público. Marco estratégico e institucional."),
    ("B.4.I", 2, "El hardware: conceptos básicos. Componentes y arquitectura de un sistema informático. Periféricos. Sistemas de almacenamiento."),
    ("B.4.I", 3, "El software: concepto, tipología, evolución. Sistemas operativos. Software de aplicación. Software libre y propietario."),
    ("B.4.I", 4, "Bases de datos: conceptos básicos. Modelos de datos. El modelo relacional. Sistemas de gestión de bases de datos. El lenguaje SQL."),
    ("B.4.I", 5, "Redes de comunicaciones: conceptos básicos. Arquitectura de redes. Protocolos. Internet: arquitectura, servicios. La red SARA."),
    ("B.4.I", 6, "Desarrollo de sistemas de información. El ciclo de vida del software. Metodologías de desarrollo. Metodologías ágiles."),
    ("B.4.I", 7, "La World Wide Web. Tecnologías web. Servicios web. Arquitectura orientada a servicios."),
    ("B.4.I", 8, "Seguridad informática: conceptos básicos. Amenazas y vulnerabilidades. Medidas de protección. Criptografía. Firma electrónica."),
    ("B.4.I", 9, "Cloud computing: concepto, modelos de servicio, modelos de despliegue. Ventajas e inconvenientes. Cloud en el sector público."),
    ("B.4.I", 10, "Big Data: concepto y características. Tecnologías asociadas. Aplicaciones en el sector público."),
    ("B.4.I", 11, "Inteligencia artificial: concepto y tipos. Machine learning. Redes neuronales. Aplicaciones en el sector público. Implicaciones éticas."),
    ("B.4.I", 12, "Automatización de procesos (RPA): concepto, tecnologías, aplicaciones. Chatbots y asistentes virtuales."),
    ("B.4.I", 13, "Blockchain: concepto, características y funcionamiento. Aplicaciones en el sector público. Identidad digital."),
    ("B.4.I", 14, "Internet de las cosas (IoT): concepto, arquitectura, aplicaciones. Smart cities. 5G e infraestructuras digitales."),

    # II. Gestión de la información y administración electrónica (temas 15-28)
    ("B.4.II", 15, "Administración electrónica: concepto, evolución, marco normativo. Derechos y deberes de los ciudadanos en relación con la administración electrónica."),
    ("B.4.II", 16, "Sede electrónica: concepto, contenido y requisitos. Punto de Acceso General electrónico. Portal de la transparencia."),
    ("B.4.II", 17, "Registro electrónico: concepto, requisitos. Sistema de Interconexión de Registros. Compulsa electrónica."),
    ("B.4.II", 18, "Expediente electrónico: concepto, formación, características. Documento electrónico: concepto, validez, copias. Archivo electrónico."),
    ("B.4.II", 19, "Notificaciones electrónicas: concepto, requisitos, práctica. Dirección Electrónica Habilitada única. Carpeta ciudadana."),
    ("B.4.II", 20, "Identificación y firma electrónica: normativa. Certificado electrónico. DNI electrónico. Cl@ve. Sistemas de identificación y firma en el sector público."),
    ("B.4.II", 21, "Interoperabilidad en el sector público: concepto, dimensiones. El Esquema Nacional de Interoperabilidad. Normas técnicas de interoperabilidad."),
    ("B.4.II", 22, "Reutilización de información del sector público. Datos abiertos. El Portal de datos abiertos. Licencias."),
    ("B.4.II", 23, "El Esquema Nacional de Seguridad: principios básicos, requisitos, medidas de seguridad. Centro Criptológico Nacional."),
    ("B.4.II", 24, "Protección de datos: principios. Derechos del interesado. Obligaciones del responsable y del encargado del tratamiento. El delegado de protección de datos."),
    ("B.4.II", 25, "Ciberseguridad: amenazas, vulnerabilidades, ataques. Gestión de incidentes. Continuidad de negocio. CERT."),
    ("B.4.II", 26, "Accesibilidad electrónica: concepto, normativa. Criterios de accesibilidad. Evaluación de la accesibilidad."),
    ("B.4.II", 27, "Servicios electrónicos a ciudadanos y empresas: catálogo de servicios. Carpeta ciudadana. Ventanilla única empresarial."),
    ("B.4.II", 28, "Factura electrónica: concepto, requisitos. FACe. Punto General de Entrada de Facturas Electrónicas. Registro Contable de Facturas."),

    # III. Planificación, gestión y evaluación de proyectos (temas 29-40)
    ("B.4.III", 29, "Dirección y gestión de proyectos: concepto y etapas. Metodologías de gestión de proyectos. PMBOK. PRINCE2. Metodologías ágiles."),
    ("B.4.III", 30, "Planificación de proyectos: objetivos, alcance, recursos, tiempo, costes. Diagramas de red: PERT, CPM. Diagrama de Gantt."),
    ("B.4.III", 31, "Gestión de riesgos en proyectos: identificación, análisis, respuesta, seguimiento."),
    ("B.4.III", 32, "Gestión de la calidad en proyectos: concepto, planificación, aseguramiento, control."),
    ("B.4.III", 33, "Gestión del cambio organizativo. Gestión del conocimiento. Comunidades de práctica."),
    ("B.4.III", 34, "Oficina de proyectos (PMO): concepto, funciones, modelos. Gobernanza de proyectos."),
    ("B.4.III", 35, "Contratación de proyectos TIC: pliegos. Criterios de adjudicación. Ejecución y seguimiento."),
    ("B.4.III", 36, "Evaluación de proyectos: conceptos básicos. Indicadores de evaluación. Cuadro de mando integral."),
    ("B.4.III", 37, "Análisis de viabilidad de proyectos: técnica, económica, operativa. Caso de negocio."),
    ("B.4.III", 38, "Técnicas de análisis organizativo: análisis funcional, análisis de procesos, análisis de datos. Modelado de procesos: BPMN."),
    ("B.4.III", 39, "Reingeniería de procesos: concepto, metodología, fases. Simplificación administrativa."),
    ("B.4.III", 40, "Gestión por procesos: concepto, principios. Mapa de procesos. Indicadores de proceso. Mejora continua."),

    # IV. Medio ambiente y sostenibilidad (temas 41-48)
    ("B.4.IV", 41, "Medio ambiente: marco constitucional y distribución de competencias. Política ambiental de la Unión Europea. El Pacto Verde Europeo."),
    ("B.4.IV", 42, "Evaluación ambiental: evaluación ambiental estratégica y evaluación de impacto ambiental. Procedimiento. Participación pública."),
    ("B.4.IV", 43, "Cambio climático: causas, efectos, escenarios. Acuerdos internacionales. Políticas de mitigación y adaptación."),
    ("B.4.IV", 44, "Transición ecológica: concepto. Economía circular. Descarbonización. Transición energética justa."),
    ("B.4.IV", 45, "Espacios naturales protegidos: tipología, régimen jurídico. Red Natura 2000. Biodiversidad."),
    ("B.4.IV", 46, "Contaminación atmosférica: tipos, efectos, medición, control. Calidad del aire. Prevención y control integrados."),
    ("B.4.IV", 47, "Gestión de residuos: concepto, tipología, jerarquía. Residuos urbanos. Residuos peligrosos. Responsabilidad ampliada del productor."),
    ("B.4.IV", 48, "Agua: dominio público hidráulico. Planificación hidrológica. Calidad del agua. Reutilización."),

    # V. Consumo y seguridad alimentaria (temas 49-52)
    ("B.4.V", 49, "Protección de los consumidores: marco constitucional y distribución de competencias. Política de consumo de la Unión Europea. El Texto Refundido de la Ley General para la Defensa de Consumidores y Usuarios."),
    ("B.4.V", 50, "Derechos de los consumidores: información, seguridad, calidad. Contratos de consumo. Cláusulas abusivas. Resolución alternativa de litigios."),
    ("B.4.V", 51, "Seguridad alimentaria: concepto, principios. Autoridades competentes. Sistema de Alerta Rápida. Trazabilidad. Crisis alimentarias."),
    ("B.4.V", 52, "Sanidad animal y vegetal. Higiene de los alimentos. Etiquetado. Control oficial de alimentos y piensos."),
]


def build_tema(bloque: str, num: int, titulo: str) -> dict:
    return {
        "oposicion_id": OPOSICION_ID,
        "bloque": bloque,
        "num_tema": num,
        "titulo": titulo,
        "leyes_vinculadas": [],
        "peso_examen_pct": None,
        "prioridad": None,
    }


def main():
    # Combine all temas
    all_temas = []
    
    # Materias Comunes
    for bloque, num, titulo in MATERIAS_COMUNES:
        all_temas.append(build_tema(bloque, num, titulo))
    
    # Materias Jurídicas
    for bloque, num, titulo in MATERIAS_JURIDICAS:
        all_temas.append(build_tema(bloque, num, titulo))
    
    # Materias Sociales
    for bloque, num, titulo in MATERIAS_SOCIALES:
        all_temas.append(build_tema(bloque, num, titulo))
    
    # Materias Económicas
    for bloque, num, titulo in MATERIAS_ECONOMICAS:
        all_temas.append(build_tema(bloque, num, titulo))
    
    # Materias Técnicas
    for bloque, num, titulo in MATERIAS_TECNICAS:
        all_temas.append(build_tema(bloque, num, titulo))
    
    print(f"Total temas: {len(all_temas)}")
    print(f"  - Materias Comunes: {len(MATERIAS_COMUNES)}")
    print(f"  - Materias Jurídicas: {len(MATERIAS_JURIDICAS)}")
    print(f"  - Materias Sociales: {len(MATERIAS_SOCIALES)}")
    print(f"  - Materias Económicas: {len(MATERIAS_ECONOMICAS)}")
    print(f"  - Materias Técnicas: {len(MATERIAS_TECNICAS)}")
    
    # Send to API in chunks (API might have limits)
    CHUNK_SIZE = 50
    total_inserted = 0
    
    for i in range(0, len(all_temas), CHUNK_SIZE):
        chunk = all_temas[i:i+CHUNK_SIZE]
        data = json.dumps(chunk).encode('utf-8')
        req = urllib.request.Request(
            f"{API_BASE}/temario/bulk",
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        try:
            with urllib.request.urlopen(req, timeout=60.0) as response:
                if response.status == 201:
                    total_inserted += len(chunk)
                    print(f"Inserted chunk {i//CHUNK_SIZE + 1}: {len(chunk)} temas (total: {total_inserted})")
                else:
                    print(f"Error inserting chunk {i//CHUNK_SIZE + 1}: {response.status}")
                    break
        except Exception as e:
            print(f"Error inserting chunk {i//CHUNK_SIZE + 1}: {e}")
            break
    
    print(f"\nDone! Total temas inserted: {total_inserted}")


if __name__ == "__main__":
    main()
