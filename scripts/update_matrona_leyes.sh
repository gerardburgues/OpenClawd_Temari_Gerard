#!/bin/bash
# Update Matrona SAS with leyes_vinculadas
API="http://localhost:8001"

# Tema 1: CE 1978
curl -s -X PATCH "$API/temario/443b209f-34cc-400c-b3da-a310aed42483" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["CE 1978"]}' > /dev/null

# Tema 2: Estatuto Andalucía (LO 2/2007)
curl -s -X PATCH "$API/temario/bbbda221-be8e-4af3-839a-50fda0266437" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["LO 2/2007"]}' > /dev/null

# Tema 3: LGS (Ley 14/1986)
curl -s -X PATCH "$API/temario/6b9378d3-7f0a-45d7-b37a-9401c601f96e" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 14/1986"]}' > /dev/null

# Tema 4: Ley Salud Andalucía (Ley 2/1998)
curl -s -X PATCH "$API/temario/ba42be89-970b-497e-9153-80a4322676b9" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 2/1998"]}' > /dev/null

# Tema 5: SAS (Ley 2/1998)
curl -s -X PATCH "$API/temario/3c0b2fad-974b-4d3e-bac2-1433c5d49f0b" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 2/1998"]}' > /dev/null

# Tema 6: Protección de datos (LO 3/2018)
curl -s -X PATCH "$API/temario/59b23fa3-e887-40ae-9c38-8160858912d5" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["LO 3/2018"]}' > /dev/null

# Tema 7: PRL (Ley 31/1995)
curl -s -X PATCH "$API/temario/d679f696-6b9c-4e83-a2c7-92447969c070" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 31/1995"]}' > /dev/null

# Tema 8: Igualdad y VG Andalucía (Ley 12/2007 And, Ley 13/2007)
curl -s -X PATCH "$API/temario/81b5757b-fdb7-4046-adff-e3bb1c4a97df" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 12/2007 And", "Ley 13/2007"]}' > /dev/null

# Tema 9: Estatuto Marco (Ley 55/2003)
curl -s -X PATCH "$API/temario/808825d7-225e-41ce-87bd-b8bb8d93b162" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 55/2003"]}' > /dev/null

# Temas 10-30: Materia clínica específica (sin leyes específicas salvo excepciones)
for id in 78627205-d55a-4454-99ba-3bcd1cc2ab4e d13d5f9e-a32c-4620-be74-e8f4718f0d9e ce47801a-a3ea-4514-8e52-e4703021a851 fe650903-bb38-4e95-8556-8f92ff656849 2ce5daf7-fdc9-4c54-a404-de07615f3420 dc9d6e58-df0e-4518-91ab-75676f29e053 7c948682-d7f2-457d-a2ca-5b477a3335a7 f63ff4f1-a34f-42ae-9878-34748dee9f13 dc9ed6e6-4ae0-4c3d-9182-2d34b602904b 18c15151-e2c2-4e6c-a9ee-7810ced79d22 d556cf5c-3170-481b-a229-ce81027904ef 57b7c6cc-c036-4bd2-a9c1-91617e746618 e98ffe71-c6bb-47c1-a7f9-576683113b1f 26e18a14-b95a-495b-8087-01cad173e90c d654b43e-7804-4226-886b-b4082ea1dfbe c8a5c5bc-84cd-4412-adcd-24c47b2ade58 6e98873e-abba-4575-939f-9886d9354721; do
  curl -s -X PATCH "$API/temario/$id" -H "Content-Type: application/json" -d '{"leyes_vinculadas": []}' > /dev/null
done

# Tema 11: Responsabilidad (Ley 41/2002)
curl -s -X PATCH "$API/temario/71120ba4-3b84-48d0-945f-663f32e08f17" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 41/2002"]}' > /dev/null

# Tema 12: Educación maternal
curl -s -X PATCH "$API/temario/8980431a-a212-4939-b14a-e16a85834ae6" -H "Content-Type: application/json" -d '{"leyes_vinculadas": []}' > /dev/null

# Tema 23: Salud reproductiva, IVE (LO 2/2010)
curl -s -X PATCH "$API/temario/b37cbcce-1f04-43ee-b291-f5e0f1382bf8" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["LO 2/2010"]}' > /dev/null

# Tema 26: Violencia de género (Ley 13/2007, LO 1/2004)
curl -s -X PATCH "$API/temario/2a48dc90-ae7b-4350-aabf-02bdf0beac47" -H "Content-Type: application/json" -d '{"leyes_vinculadas": ["Ley 13/2007", "LO 1/2004"]}' > /dev/null

echo "Matrona SAS temario updated"
