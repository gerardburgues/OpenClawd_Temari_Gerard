import { useState, useMemo } from 'react'
import { useData } from '@/hooks/useData'

export function useOposicionesFilters() {
  const { oposiciones: oposicionesData } = useData()
  const [searchTerm, setSearchTerm] = useState('')
  const [filterAmbito, setFilterAmbito] = useState('Todos')
  const [filterGrupo, setFilterGrupo] = useState('Todos')
  const [filterState, setFilterState] = useState('Todos')

  // Get unique ambitos
  const ambitos = useMemo(() =>
    ['Todos', ...new Set(oposicionesData.map(o => o.ambito))],
    [oposicionesData]
  )

  // Filter oposiciones
  const filteredOposiciones = useMemo(() => {
    return oposicionesData.filter(opo => {
      const matchesSearch = opo.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           opo.organismo.toLowerCase().includes(searchTerm.toLowerCase())
      const matchesAmbito = filterAmbito === 'Todos' || opo.ambito === filterAmbito
      const matchesGrupo = filterGrupo === 'Todos' || opo.grupo === filterGrupo
      const matchesState = filterState === 'Todos' || opo.pipeline_state === filterState
      return matchesSearch && matchesAmbito && matchesGrupo && matchesState
    })
  }, [oposicionesData, searchTerm, filterAmbito, filterGrupo, filterState])

  return {
    // Filter values
    searchTerm,
    filterAmbito,
    filterGrupo,
    filterState,

    // Filter setters
    setSearchTerm,
    setFilterAmbito,
    setFilterGrupo,
    setFilterState,

    // Derived data
    ambitos,
    filteredOposiciones,
  }
}
