#!/bin/bash
API="http://localhost:8005/legislacion/"

# Ley 12/1989 - Función Estadística Pública
curl -s -X POST "$API" -H "Content-Type: application/json" -d '{"referencia":"Ley 12-1989","nombre_corto":"Ley Funcion Estadistica Publica","url_boe":"https://www.boe.es/buscar/act.php?id=BOE-A-1989-10767","veces_referenciada":1}'

# LO 3/2021 - Eutanasia (correcting reference)
curl -s -X POST "$API" -H "Content-Type: application/json" -d '{"referencia":"LO 3-2021","nombre_corto":"Ley Eutanasia","url_boe":"https://www.boe.es/buscar/act.php?id=BOE-A-2021-4628","veces_referenciada":1}'

# RDL 1/2015 - Medicamentos
curl -s -X POST "$API" -H "Content-Type: application/json" -d '{"referencia":"RDLeg 1-2015","nombre_corto":"Ley Garantias Medicamentos","url_boe":"https://www.boe.es/buscar/act.php?id=BOE-A-2015-8343","veces_referenciada":1}'

# RD 888/2022 - Discapacidad
curl -s -X POST "$API" -H "Content-Type: application/json" -d '{"referencia":"RD 888-2022","nombre_corto":"Baremo Discapacidad","url_boe":"https://www.boe.es/buscar/act.php?id=BOE-A-2022-17105","veces_referenciada":1}'

# RD 1299/2006 - Enfermedades profesionales
curl -s -X POST "$API" -H "Content-Type: application/json" -d '{"referencia":"RD 1299-2006","nombre_corto":"Cuadro Enfermedades Profesionales","url_boe":"https://www.boe.es/buscar/act.php?id=BOE-A-2006-22169","veces_referenciada":1}'

echo "Done"
