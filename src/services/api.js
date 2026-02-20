const BASE_URL = import.meta.env.VITE_API_URL || '/api'

async function fetchJSON(endpoint) {
  const res = await fetch(`${BASE_URL}${endpoint}`)
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${endpoint}`)
  }
  return res.json()
}

async function fetchAll(endpoint, maxLimit) {
  const separator = endpoint.includes('?') ? '&' : '?'
  let all = []
  let skip = 0
  while (true) {
    const page = await fetchJSON(`${endpoint}${separator}limit=${maxLimit}&skip=${skip}`)
    if (!Array.isArray(page) || page.length === 0) break
    all = all.concat(page)
    if (page.length < maxLimit) break
    skip += maxLimit
  }
  return all
}

export async function getOposiciones() {
  return fetchAll('/oposiciones/', 1000)
}

export async function getTemario() {
  return fetchAll('/temario/', 5000)
}

export async function getLegislacion() {
  return fetchAll('/legislacion/', 1000)
}

export async function getConvocatorias() {
  return fetchAll('/convocatorias/', 1000)
}

export async function getExamenes() {
  return fetchAll('/examenes/', 1000)
}
