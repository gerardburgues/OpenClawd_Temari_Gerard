import { useMemo } from 'react'
import oposicionesData from '@/data/oposiciones.json'
import temarioData from '@/data/temario.json'
import legislacionData from '@/data/legislacion.json'
import examenesData from '@/data/examenes.json'

export function useOposicionesStats() {
  const stats = useMemo(() => {
    const total = oposicionesData.length
    const completas = oposicionesData.filter(o => o.pipeline_state === 'completa').length
    const enProceso = oposicionesData.filter(o => o.agente_activo !== null).length
    const totalTemas = temarioData.length
    const totalLeyes = legislacionData.length
    const totalExamenes = examenesData.length
    const errores = oposicionesData.filter(o => o.pipeline_state === 'error').length

    return {
      total,
      completas,
      enProceso,
      totalTemas,
      totalLeyes,
      totalExamenes,
      errores
    }
  }, [])

  return stats
}
