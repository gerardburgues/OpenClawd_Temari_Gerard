import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { PIPELINE_STATES, AGENTS, GRUPOS } from '@/constants/pipeline'
import { useOposicionesFilters } from '@/hooks/useOposicionesFilters'
import FilterBar from '@/components/dashboard/FilterBar'
import oposicionesData from '@/data/oposiciones.json'

export default function Pipeline() {
  const {
    searchTerm,
    setSearchTerm,
    filterAmbito,
    setFilterAmbito,
    filterGrupo,
    setFilterGrupo,
    filterState,
    setFilterState,
    ambitos,
    filteredOposiciones,
  } = useOposicionesFilters()

  const progressByState = useMemo(() => {
    return PIPELINE_STATES.slice(0, 7).map(state => ({
      ...state,
      count: oposicionesData.filter(o => o.pipeline_state === state.id).length
    }))
  }, [])

  return (
    <div className="p-8 space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Pipeline de Oposiciones</h1>
        <p className="text-muted-foreground">Vista Kanban organizada por estado del pipeline</p>
      </div>

      <FilterBar
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        filterAmbito={filterAmbito}
        setFilterAmbito={setFilterAmbito}
        filterGrupo={filterGrupo}
        setFilterGrupo={setFilterGrupo}
        filterState={filterState}
        setFilterState={setFilterState}
        ambitos={ambitos}
        resultCount={filteredOposiciones.length}
      />

      <div className="grid grid-cols-7 gap-4">
        {progressByState.map(state => {
          const opos = filteredOposiciones.filter(o => o.pipeline_state === state.id)
          return (
            <Card key={state.id}>
              <CardHeader className="pb-3" style={{ borderBottom: `2px solid ${state.color}` }}>
                <div className="flex items-center gap-2">
                  <span className="text-lg">{state.icon}</span>
                  <CardTitle className="text-sm">{state.label}</CardTitle>
                </div>
                <div className="text-xs text-muted-foreground font-mono">{opos.length}</div>
              </CardHeader>
              <CardContent className="pt-4 space-y-2">
                {opos.map(opo => {
                  const grupo = GRUPOS[opo.grupo]
                  return (
                    <Link key={opo.id} to={`/oposicion/${opo.id}`}>
                      <div className="p-3 rounded border border-border bg-card hover:bg-accent/50 transition-colors cursor-pointer">
                        <div className="text-sm font-medium mb-2">{opo.nombre}</div>
                        <div className="flex items-center gap-2 mb-2">
                          <Badge
                            style={{
                              backgroundColor: grupo.bg,
                              color: grupo.color,
                              fontSize: '10px'
                            }}
                          >
                            {opo.grupo}
                          </Badge>
                          <span className="text-xs text-muted-foreground">{opo.ambito}</span>
                        </div>
                        {opo.agente_activo && (
                          <div className="flex items-center gap-1 text-xs">
                            <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                            <span className="text-muted-foreground">
                              {AGENTS.find(a => a.id === opo.agente_activo)?.name}
                            </span>
                          </div>
                        )}
                      </div>
                    </Link>
                  )
                })}
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
