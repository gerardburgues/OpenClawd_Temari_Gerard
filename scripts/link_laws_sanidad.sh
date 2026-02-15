#!/bin/bash
API="http://localhost:8005/temario"

# Parte Primera - Admin General (temas 1-20)
curl -s -X PATCH "$API/aede16e4-f847-422d-bc7d-a54b1c2ead7d" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978"]}'
curl -s -X PATCH "$API/78c8b842-c2ce-4cc8-a9fe-14b21d36e018" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978","LO 6/1985","LO 2/1979","LO 3/1981"]}'
curl -s -X PATCH "$API/f84ca52e-b4a9-45c6-aa5c-3f79b06ab943" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978"]}'
curl -s -X PATCH "$API/9e37eafa-5148-4b04-87cb-0df8b0963ef2" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978"]}'
curl -s -X PATCH "$API/946e54aa-8a2e-44ff-bea3-cdce1c9d733d" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978","Ley 50/1997","Ley 47/2003"]}'
curl -s -X PATCH "$API/dd49339a-4d3f-4a82-b571-ef79dc58bc4d" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978","Ley 40/2015","Ley 7/1985"]}'
curl -s -X PATCH "$API/34f08bd5-66df-48a4-8ea0-8fcf03118c83" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978"]}'
curl -s -X PATCH "$API/3a63a080-ca19-4e5f-879c-c9cb2ef89c46" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 39/2015"]}'
curl -s -X PATCH "$API/9c3b25d3-72d8-4bdc-93ea-247332a44d40" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 39/2015"]}'
curl -s -X PATCH "$API/bb9e05d2-76ca-4393-8783-b2e08420b828" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 40/2015"]}'
curl -s -X PATCH "$API/3c79d448-047c-4274-9963-41e2efbc69d2" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 40/2015"]}'
curl -s -X PATCH "$API/36e32550-4928-4b63-9020-17714530e5e6" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 40/2015"]}'
curl -s -X PATCH "$API/963a8f73-a4bb-4e52-9bd8-5694adff06b6" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 40/2015"]}'
curl -s -X PATCH "$API/a7e83f6c-8983-4baf-9e56-c9364714c6e5" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 19/2013"]}'
curl -s -X PATCH "$API/087a8118-521b-401c-bd4d-f520e77ea7dd" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 9/2017"]}'
curl -s -X PATCH "$API/8193e6d6-2205-46e6-a537-6219a31aa8d1" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 5/2015"]}'
curl -s -X PATCH "$API/186ae9a7-a577-4486-a3f4-f19bddb9016c" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["LO 3/2007","LO 1/2004"]}'
curl -s -X PATCH "$API/cecf53d6-eb23-452e-830b-7d2a43a8c76d" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 2/2015"]}'

# Parte Primera - Sanidad (temas 21-26, 38, 41)
curl -s -X PATCH "$API/d2ef03d3-1cff-44b3-bc84-2a718887de00" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978","Ley 14/1986"]}'
curl -s -X PATCH "$API/34cbaa08-ba01-4e1c-a1a5-c41809cbf233" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 44/2003"]}'
curl -s -X PATCH "$API/6a2c9ed1-dbed-46ca-9f03-210ed8d90cfb" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["LO 3/2018","RGPD 2016/679"]}'
curl -s -X PATCH "$API/acb52d68-103d-474a-8661-15bb5c533d38" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDLeg 1-2015"]}'
curl -s -X PATCH "$API/4b5bb793-763a-436c-92a7-6c7d1d0dad1c" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 41/2002"]}'

# Parte Primera - Organización Asistencial
curl -s -X PATCH "$API/64b51c94-5686-414b-b776-6a12d365d230" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 55/2003"]}'

# Parte Segunda - Seguridad Social (temas 57-73)
curl -s -X PATCH "$API/9663f490-59e5-4dab-908f-817aceba19c7" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978","RDL 8/2015"]}'
curl -s -X PATCH "$API/44bdf210-b5bc-450c-a621-5902e0ff4f43" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 8/2015"]}'
curl -s -X PATCH "$API/aa232493-94db-4936-9938-a84889bf78f1" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 8/2015"]}'
curl -s -X PATCH "$API/1d50176c-f3aa-4f16-8931-c10774d8d0e8" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 8/2015"]}'
curl -s -X PATCH "$API/98659447-929a-4b56-b365-0ff51b91f709" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 8/2015"]}'
curl -s -X PATCH "$API/a01b8923-2eb8-4db8-8bfd-b70eca796a07" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 8/2015"]}'
curl -s -X PATCH "$API/20f20c73-0d2c-408f-8dd0-918447ee558d" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 8/2015"]}'
curl -s -X PATCH "$API/31cb9da4-a766-439c-ba9c-add719a9b4b0" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 8/2015"]}'
curl -s -X PATCH "$API/62cdbecf-f12d-4610-826c-b77ef78c919b" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 8/2015"]}'
curl -s -X PATCH "$API/4d056515-0dbb-4a03-9c6e-bc94b3a576b1" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 8/2015"]}'
curl -s -X PATCH "$API/61748f12-a921-4531-9f36-c34f0a315ee1" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 8/2015"]}'

# PRL
curl -s -X PATCH "$API/52944ade-f357-40f3-a973-6e1810bd94e6" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 31/1995"]}'

# Discapacidad y Dependencia
curl -s -X PATCH "$API/9bd3ba5d-2ca0-4ddf-9357-6ffe6e82e962" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RD 888-2022"]}'
curl -s -X PATCH "$API/f54d776e-28a6-4f14-9925-5540521fd391" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 39/2006"]}'

# Enfermedad profesional
curl -s -X PATCH "$API/1e6b45f5-6406-4fb8-826d-c7f4229d6732" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RD 1299-2006"]}'

echo "Done Sanidad"
