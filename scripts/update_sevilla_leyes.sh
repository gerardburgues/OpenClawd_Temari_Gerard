#!/bin/bash
# Update Auxiliar Administrativo Diputación Sevilla with leyes_vinculadas
API="http://localhost:8001"

# Tema 1: Constitución
curl -s -X PATCH "$API/temario/73cef66b-a9cd-4a97-aa6e-0804b5e23630" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["CE 1978"]}' > /dev/null

# Tema 2: Corona, Cortes, Gobierno (CE 1978)
curl -s -X PATCH "$API/temario/dcca65cb-c928-417a-b426-a0331a9cd58d" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["CE 1978"]}' > /dev/null

# Tema 3: Organización territorial, Estatuto Andalucía (CE 1978, LO 2/2007)
curl -s -X PATCH "$API/temario/7f936333-b11a-4ee3-88bd-39e9d635ff4d" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["CE 1978", "LO 2/2007"]}' > /dev/null

# Tema 4: UE
curl -s -X PATCH "$API/temario/147d77ac-1617-40c7-a500-3022adf47c7c" -H "Content-Type: application/json" -d '{"leyes_vinculadas": []}' > /dev/null

# Tema 5: Ley 39/2015 LPAC
curl -s -X PATCH "$API/temario/0f765815-d90e-4361-8d84-9de525a81bae" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 39/2015"]}' > /dev/null

# Tema 6-7: Acto y procedimiento administrativo (Ley 39/2015)
curl -s -X PATCH "$API/temario/fb4d4146-df4d-44bc-a680-d12b78c38776" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 39/2015"]}' > /dev/null
curl -s -X PATCH "$API/temario/072faeac-56b7-4dd6-8565-8e89f95a44fb" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 39/2015"]}' > /dev/null

# Tema 8: TREBEP
curl -s -X PATCH "$API/temario/85a22cb2-5b19-42f3-94d7-a8d926eebe86" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["RDL 5/2015"]}' > /dev/null

# Tema 9: LRBRL
curl -s -X PATCH "$API/temario/6d051919-a132-4a39-ae2f-4598b437e487" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 7/1985"]}' > /dev/null

# Tema 10: Diputación Provincial (Ley 7/1985)
curl -s -X PATCH "$API/temario/2107000b-210b-4639-bc6a-4862e87463c0" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 7/1985"]}' > /dev/null

# Tema 11: Órganos colegiados (Ley 40/2015)
curl -s -X PATCH "$API/temario/eb90020f-95fa-4e16-8508-0b195ea8ef77" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 40/2015"]}' > /dev/null

# Tema 12: Haciendas locales (RDL 2/2004)
curl -s -X PATCH "$API/temario/e1602be3-1dce-48ab-815b-22012d2dc5a4" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["RDL 2/2004"]}' > /dev/null

# Tema 13: Transparencia (Ley 19/2013, Ley 39/2015)
curl -s -X PATCH "$API/temario/16a2fe37-bd5e-4344-919f-bae216abfe3c" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 19/2013", "Ley 39/2015"]}' > /dev/null

# Tema 14: Administración electrónica (Ley 39/2015)
curl -s -X PATCH "$API/temario/977d885e-ddae-4093-b0b5-6db866538777" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 39/2015"]}' > /dev/null

# Tema 15: Protección de datos (LO 3/2018)
curl -s -X PATCH "$API/temario/93f06f0b-e5c9-4352-adba-fff5f0cfe0f4" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["LO 3/2018"]}' > /dev/null

# Tema 16: Contratos (Ley 9/2017)
curl -s -X PATCH "$API/temario/55c883eb-3493-47bf-9a4d-a49f43cc9848" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 9/2017"]}' > /dev/null

# Tema 17: Igualdad (LO 3/2007, Ley 12/2007 And)
curl -s -X PATCH "$API/temario/3cf314a4-e0f7-4a30-a1ee-a51ec8f09daa" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["LO 3/2007", "Ley 12/2007 And"]}' > /dev/null

# Tema 18: Ofimática (no laws)
curl -s -X PATCH "$API/temario/d8d6262f-0ab0-4b81-951b-68f9fe87d8e6" -H "Content-Type: application/json" -d '{"leyes_vinculadas": []}' > /dev/null

echo "Sevilla temario updated"
