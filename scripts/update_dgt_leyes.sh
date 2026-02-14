#!/bin/bash
# Update Técnicos de Tráfico DGT temas with leyes_vinculadas
API="http://localhost:8001"
OPO_ID="69e35dad-b6d9-4dd2-a307-562b71f97454"

# Temas 1-7: Constitución (CE 1978)
for id in 9e3cac76-b6ac-46f7-b103-4124faa3617f 44d78f4c-6ac0-42c6-abbc-7c21fd585cbb 54ad858a-8068-43f2-88db-adb21c206e9d 3f9d807a-d6c0-4818-9def-2314f71cddf6 4fc9c580-d559-4d68-9989-08fceed09404 eae57142-a49f-49fd-9dd3-13e2421a8e0c 52377356-963b-4c6f-a48a-ede230de8114; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["CE 1978"]}' > /dev/null
done

# Temas 8-14: Administración General del Estado (CE 1978, Ley 40/2015)
for id in 4bdf3d8f-d476-42fd-aa9f-e103def6a682 8a195781-c062-4a7e-8b76-1615660f81f5 98e3bd48-8e0c-4550-9c8e-f214b13e83cb 2aab355a-6b10-4271-98bf-05bc0fef5fb3 ad6082b8-089c-4881-9c02-b4e3fefb166b 1ead90cb-d9b0-4176-b0c1-b97aab8341c5 eccb39e1-d008-4583-97fc-8b6b096d7145; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["CE 1978", "Ley 40/2015"]}' > /dev/null
done

# Temas 15-16: Fuentes del ordenamiento (CE 1978)
for id in 7a516491-104b-42ba-865e-975f9d1af036 a1485b50-a37d-439e-a0d6-aa9c2df64f46; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["CE 1978"]}' > /dev/null
done

# Temas 17-22: Procedimiento administrativo (Ley 39/2015, Ley 40/2015, Ley 29/1998)
for id in 426d951b-1eea-4904-b7e6-96adf9dc6823 7a2ba04e-a7c0-41c8-9687-635c441ad428 06d71857-a0ce-477a-93a0-701d9ff3d4b5 838b2d3e-4383-4dbb-a122-a4e73d82fc17 e5512a07-9175-44f8-9732-5318f02105ad c4ddebc1-de26-4f73-8007-6c6bb2fe8b50; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 39/2015", "Ley 40/2015", "Ley 29/1998"]}' > /dev/null
done

# Temas 23-26: Contratos (Ley 9/2017)
for id in 64cf62fa-21dc-493d-95f8-48cec0d4e8da 68e6b00d-3f67-4ca1-8b84-779b3450bd77 f87aba9d-48ca-404d-acd2-5c8beef89cd4 948a8a69-cb7b-46c8-852d-44a0283a7fa4; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 9/2017"]}' > /dev/null
done

# Temas 27-32: UE y derecho internacional
for id in d2bcc4f6-755a-42de-9879-4cad89ced1f7 ec69548c-0314-40ae-8f4c-e0eac9aad601 d3ac961a-d9a9-414d-bdb6-4dcf0dd69952 a8f3e196-7455-4718-a0c9-6643d76aa1bf ec3d0113-a5fa-454d-8785-630c7ada84c2 8cf9a0f4-3685-4339-9655-f4f59d41b535; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": []}' > /dev/null
done

# Temas 33-34: Gestión pública y gobierno abierto (Ley 19/2013)
for id in 75da297e-13d0-49dd-824c-a6e221bbd404 04eb5eaa-08b8-4d38-9c63-ecbb4f4cfaf9; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 19/2013"]}' > /dev/null
done

# Tema 35: Protección de datos (RGPD 2016/679, LO 3/2018)
curl -s -X PATCH "$API/temario/16272c7a-4574-43b2-bd72-cf54bc21e0af" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["RGPD 2016/679", "LO 3/2018"]}' > /dev/null

# Temas 36-43: Gestión de RRHH y función pública
for id in 15611ef6-6d61-4fce-b3b3-d85f0c5bcfc6 73dd76b4-97e1-4b82-a79d-b0639e51f279 c6ae024a-8918-48bb-b2b8-3f502f4590ee 8dfe9f91-c7ab-464d-8b2e-80afb5f34363 7c248148-aa4e-48ef-8bdc-b01e6562147c 2d41c87b-3a06-4d23-b984-26969f86755f 32388841-64f5-4aa5-8a95-fca7cc26c6d5 b62b517c-ae47-46cb-b1a2-0f9fee419351; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": []}' > /dev/null
done

# Temas 44-47: Empleo público (RDL 5/2015)
for id in e9f923f9-115d-4b74-94f4-40a1f66dd890 24b0ab28-9a16-4b4c-9ae0-424da7029c24 6f93aad4-5e82-4bdb-86ff-9cbbfdae241b 9d604c52-5723-4a45-8c60-ccdcb640ee13; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["RDL 5/2015"]}' > /dev/null
done

# Tema 48: Igualdad y dependencia (LO 3/2007, Ley 39/2006)
curl -s -X PATCH "$API/temario/76d0c2f1-bab4-47ef-bfab-298f5a21d922" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["LO 3/2007", "Ley 39/2006"]}' > /dev/null

# Temas 49-50: Seguridad Social (RDL 8/2015)
for id in 43dfa728-fa55-4fae-a854-df759810c3cd 20ccfc5e-b225-479d-99f8-425ea9d5422a; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["RDL 8/2015"]}' > /dev/null
done

# Tema 51: PRL (Ley 31/1995)
curl -s -X PATCH "$API/temario/b693f014-cfa8-47a8-864d-07d12c763498" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 31/1995"]}' > /dev/null

# Temas 52-60: Presupuestos (Ley 47/2003)
for id in bff5fdc7-625c-4208-a44d-70016fd15479 7127417c-04df-4cad-b8c5-a41f5d5336ad 8746fde3-8712-43e3-a7ae-47951c9d7360 b67ff648-14f4-4f38-917a-4c1a9233471c 566cf4e0-40d9-4533-a747-f005c713d09c bb12c674-3d40-435e-b043-020f04c084f8 827a3c31-c3f3-40dc-8f6c-14b927be0c48 650b221c-9e95-4f02-a4cf-02ebc0ceea07 586e6dad-e688-4736-9e27-2ae82685d047; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 47/2003"]}' > /dev/null
done

# Temas 61-90: Movilidad Segura (RDL 6/2015, RGC, RGCond, RGV)
for id in 0d5e604d-382a-4af7-bb29-7139ae38c4da 4ae08cdc-40e0-4ac4-89f1-df0da658b4c2 00054490-d51c-482b-8d1b-d3db5abbc8da 3c8e128f-df37-4ece-aa13-707727a7b2ef c1c929df-b1db-48e5-8498-3feda3dc0a82 8a4343cf-64f9-4fcf-88ef-e1fdda140788 98979cc2-cfc1-4de4-9f3b-787ddcd87d3d 69f7e617-08ac-4546-987f-43d91f49f626 cf22834d-cf75-4324-a760-4d5598b5f30b 6ca384b7-f151-4143-8056-fdf59625100d 300807d0-440b-418b-9223-d4432df29aac cc5aadde-5031-45a4-b384-00da890554c8 4981fe7e-5817-4b64-83a7-8fede0312dbe 4d331646-be26-4c17-8cf4-2ac085e29231 2f82d255-fe39-45a7-83fe-2ab8d6defe3e 71908d00-489d-4ecb-8d84-57f8565d87e5 1a45f9e6-7435-46f7-94c4-8c0ed3c24c7c 6eb50728-d596-443c-99ac-6f3c12b734e6 02a4d223-8aed-4b18-abfe-5b1b131827cb 93b71e8c-4bcc-4357-a377-f245c65f9cde 089b6174-9091-4a4a-be72-182232a7ccf8 da68e55f-e329-4142-9b4b-f113f600c9fd ceb637cd-0661-48d8-ae88-f95ee4ab1d51 60b4b824-c65f-470c-a074-96a0ccc2a801 85f5b0a5-a7f3-4619-9b80-2bb3501b2623 1179359c-3468-433a-89d0-ecd69b2103e6 691c2631-c712-43e3-a84d-d783a09e1e4d f27b7fde-0952-416d-94ba-ecc7a2414ade e5bd57da-2c74-4560-b6d0-72db2ed1b77e 8bee1010-cc3f-44bd-8b80-b7a4554c9219; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["RDL 6/2015"]}' > /dev/null
done

# Temas 91-100: Trafico específico (RDL 6/2015, RGC, RGCond, RGV, RD 836/2012)
for id in 4a7e0ce5-226f-41f2-9359-ede0485ff106 d87a57fd-8e58-43c3-84dc-64d0087f8fe1 aa7b054b-2291-4774-b450-7ab1e9ce6cfc e078846c-69a0-46ff-b387-9003ee496955 bacf8163-6cf5-422a-b836-29680de7085d aef367a7-519f-4c00-a81f-c56566dfd921 f63a6937-e805-4b34-a17e-8c801f08ff45 bae5098b-8830-4dba-a3e6-a429693b39bf 665b2081-1825-4769-8a1e-919942d2655e d90f1f6c-f3ec-4f97-8d30-f5082475a8e4; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["RDL 6/2015", "RGC", "RGCond", "RGV", "RD 836/2012"]}' > /dev/null
done

echo "DGT temario updated"
