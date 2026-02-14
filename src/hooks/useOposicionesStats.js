import { useMemo } from 'react'
import { useData } from '@/hooks/useData'

export function useOposicionesStats() {
  const { oposiciones, temario, legislacion, examenes } = useData()

  const stats = useMemo(() => {
    const total = oposiciones.length
    const completas = oposiciones.filter(o => o.pipeline_state === 'completa').length
    const enProceso = oposiciones.filter(o => o.agente_activo !== null).length
    const totalTemas = temario.length
    const totalLeyes = legislacion.length
    const totalExamenes = examenes.length
    const errores = oposiciones.filter(o => o.pipeline_state === 'error').length

    return {
      total,
      completas,
      enProceso,
      totalTemas,
      totalLeyes,
      totalExamenes,
      errores
    }
  }, [oposiciones, temario, legislacion, examenes])

  return stats
}
