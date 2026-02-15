#!/bin/bash
API="http://localhost:8005/temario"

# Tema 1 - CE 1978, LO 3/1981 (Defensor del Pueblo)
curl -s -X PATCH "$API/e7676729-ad1c-46bc-885d-d235840b7a1f" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978","LO 3/1981"]}'

# Tema 2 - CE 1978
curl -s -X PATCH "$API/58029d47-b07e-4483-b4ff-35fb04f2885f" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978"]}'

# Tema 3 - CE 1978, Ley 50/1997, Ley 40/2015
curl -s -X PATCH "$API/6042cf6a-f717-4fd9-8a3f-0f45459bb46b" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978","Ley 50/1997","Ley 40/2015"]}'

# Tema 4 - CE 1978, Ley 7/1985 (LRBRL)
curl -s -X PATCH "$API/159ff443-ae9c-4a28-ab87-b7fdeaab03c7" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["CE 1978","Ley 7/1985"]}'

# Tema 5 - Ley 39/2015, Ley 40/2015
curl -s -X PATCH "$API/7a7219ca-dfc3-4e0b-8252-580e6fbb42fe" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 39/2015","Ley 40/2015"]}'

# Tema 6 - RDL 5/2015 TREBEP
curl -s -X PATCH "$API/0ba33740-5df3-4e37-8630-ca1918708db6" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["RDL 5/2015"]}'

# Tema 7 - Ley 47/2003 LGP
curl -s -X PATCH "$API/34b41a4f-db97-451e-813c-7cf0abe9fb6a" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 47/2003"]}'

# Tema 8 - Ley 12/1989
curl -s -X PATCH "$API/0af44525-2c48-48fb-a18e-d4a0fc8ecc18" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 12-1989"]}'

# Tema 9 - LO 3/2018, RGPD
curl -s -X PATCH "$API/6914ff1f-8b3f-40a2-b798-3ac80ab8fb6b" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["LO 3/2018","RGPD 2016/679"]}'

# Tema 10 - Reglamento 223/2009
curl -s -X PATCH "$API/4d8844a9-ee2d-49be-8831-dc537e2b6d96" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Reglamento 223/2009"]}'

# Tema 11 - LO 5/1985 LOREG
curl -s -X PATCH "$API/da362572-df8e-4eb0-bb43-77164c4251b7" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["LO 5/1985"]}'

# Tema 12 - LO 3/2007, LO 1/2004
curl -s -X PATCH "$API/cf35d806-0b0c-4fb7-94f4-4ef25dd38a0b" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["LO 3/2007","LO 1/2004"]}'

# Tema 13 - Ley 19/2013
curl -s -X PATCH "$API/c3cdf426-b445-408b-807f-d9d878db9110" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 19/2013"]}'

# Tema 14 - Ley 39/2015, Ley 40/2015
curl -s -X PATCH "$API/57772afc-f7ce-48fd-9b9b-e003a54504af" -H "Content-Type: application/json" -d '{"leyes_vinculadas":["Ley 39/2015","Ley 40/2015"]}'

echo "Done Estadisticos"
