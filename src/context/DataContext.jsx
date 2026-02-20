import { createContext, useState, useEffect, useCallback } from 'react'
import {
  getOposiciones,
  getTemario,
  getLegislacion,
  getConvocatorias,
  getExamenes,
} from '@/services/api'

export const DataContext = createContext(null)

const REFRESH_INTERVAL = 300_000

export function DataProvider({ children }) {
  const [oposiciones, setOposiciones] = useState([])
  const [temario, setTemario] = useState([])
  const [legislacion, setLegislacion] = useState([])
  const [convocatorias, setConvocatorias] = useState([])
  const [examenes, setExamenes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(null)

  const refresh = useCallback(async () => {
    try {
      // Sequential fetches to avoid overwhelming serverless backend
      const opoRes = await getOposiciones()
      setOposiciones(opoRes)
      const temRes = await getTemario()
      setTemario(temRes)
      const legRes = await getLegislacion()
      setLegislacion(legRes)
      const convRes = await getConvocatorias()
      setConvocatorias(convRes)
      const exRes = await getExamenes()
      setExamenes(exRes)
      setError(null)
      setLastUpdate(new Date())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    refresh()
    const id = setInterval(refresh, REFRESH_INTERVAL)
    return () => clearInterval(id)
  }, [refresh])

  return (
    <DataContext.Provider
      value={{
        oposiciones,
        temario,
        legislacion,
        convocatorias,
        examenes,
        activityLog: [],
        loading,
        error,
        lastUpdate,
        refresh,
      }}
    >
      {children}
    </DataContext.Provider>
  )
}
