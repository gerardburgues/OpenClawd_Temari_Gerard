#!/bin/bash
API="http://localhost:8005/temario"

# Temario Común (temas 1-10)
curl -s -X PATCH "$API/3d4e9cc7-25e6-4484-97b8-8730471f8a2a" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978"]}'
curl -s -X PATCH "$API/650c7a80-974b-4a2e-b57c-83b24423a767" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["LO 2/2007"]}'
curl -s -X PATCH "$API/74f69cb7-4fa4-48f4-9ce8-bf67ae5bb84c" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 14/1986","Ley 2/1998 And"]}'
curl -s -X PATCH "$API/c6dd954d-af43-410a-a48a-57391fb8c2c9" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 2/1998 And"]}'
curl -s -X PATCH "$API/e2875627-3f69-43a9-9fee-8cea347956db" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["LO 3/2018","Ley 1/2014 Andalucia"]}'
curl -s -X PATCH "$API/1c90e56f-520c-47f3-ac9e-89dc30969fbd" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 31/1995"]}'
curl -s -X PATCH "$API/1d7ab4bc-9e27-480e-8edc-60e05e168a24" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 12/2007 And","Ley 13/2007 And"]}'
curl -s -X PATCH "$API/083020ff-66a1-4d41-a20b-c9a5952f4eaa" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 55/2003"]}'
curl -s -X PATCH "$API/893218e9-70f4-478d-818b-b230a3ca7900" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 41/2002"]}'

# Temario Específico (selected legal temas)
curl -s -X PATCH "$API/c559b458-da2c-4416-8a26-1e88f26851b6" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 16/2003"]}'
curl -s -X PATCH "$API/6a5e8466-8f33-4ea6-a784-5a0b130cf036" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 16/2011 And"]}'
curl -s -X PATCH "$API/fe2c2e44-765a-4a5f-95a1-ceda62b3676d" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 41/2002","LO 3-2021","Ley 4/2023"]}'
curl -s -X PATCH "$API/03410b0c-89ea-4489-b1e0-aa20e29fcf11" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 40/2015"]}'
curl -s -X PATCH "$API/2b6a5dc4-a7cc-4c5b-82a3-91629b023282" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 44/2003"]}'
curl -s -X PATCH "$API/a1a88023-0bcd-4fbe-b8b0-451777c5c8b6" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 14/2007"]}'
curl -s -X PATCH "$API/9bf32b42-dde7-412f-b587-2b5a8edd18b1" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 39/2006"]}'

echo "Done Terapeuta Ocupacional"
