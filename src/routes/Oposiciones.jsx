import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { PIPELINE_STATES, GRUPOS } from '@/constants/pipeline'
import { useOposicionesFilters } from '@/hooks/useOposicionesFilters'
import { useData } from '@/hooks/useData'
import FilterBar from '@/components/dashboard/FilterBar'

export default function Oposiciones() {
  const [expandedRow, setExpandedRow] = useState(null)
  const { temario: temarioData } = useData()

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

  const getProgressPercentage = (state) => {
    const stateIndex = PIPELINE_STATES.findIndex(s => s.id === state)
    return ((stateIndex + 1) / 7) * 100
  }

  return (
    <div className="p-8 space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Oposiciones</h1>
        <p className="text-muted-foreground">Vista completa de todas las oposiciones en el sistema</p>
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

      <Card>
        <div className="divide-y divide-border">
          {/* Table Header */}
          <div className="grid grid-cols-12 gap-4 p-4 text-xs font-medium text-muted-foreground bg-muted/50">
            <div className="col-span-3">Oposición</div>
            <div className="col-span-1">Grupo</div>
            <div className="col-span-2">Ámbito</div>
            <div className="col-span-2">Estado</div>
            <div className="col-span-1 text-center">Temas</div>
            <div className="col-span-1 text-center">Exámenes</div>
            <div className="col-span-2">Progreso</div>
          </div>
          {/* Table Rows */}
          {filteredOposiciones.map(opo => {
            const state = PIPELINE_STATES.find(s => s.id === opo.pipeline_state)
            const grupo = GRUPOS[opo.grupo]
            const temasCount = temarioData.filter(t => t.oposicion_id === opo.id).length
            const progress = getProgressPercentage(opo.pipeline_state)
            const isExpanded = expandedRow === opo.id

            return (
              <div key={opo.id}>
                <div
                  className="grid grid-cols-12 gap-4 p-4 hover:bg-accent/50 cursor-pointer transition-colors"
                  onClick={() => setExpandedRow(isExpanded ? null : opo.id)}
                >
                  <div className="col-span-3">
                    <div className="font-medium">{opo.nombre}</div>
                    <div className="text-xs text-muted-foreground">{opo.organismo}</div>
                  </div>
                  <div className="col-span-1">
                    <Badge
                      style={{
                        backgroundColor: grupo.bg,
                        color: grupo.color,
                        border: `1px solid ${grupo.color}40`
                      }}
                    >
                      {opo.grupo}
                    </Badge>
                  </div>
                  <div className="col-span-2 text-sm">{opo.ambito}</div>
                  <div className="col-span-2">
                    <Badge
                      style={{
                        backgroundColor: `${state.color}20`,
                        color: state.color,
                        border: `1px solid ${state.color}60`
                      }}
                    >
                      {state.icon} {state.label}
                    </Badge>
                  </div>
                  <div className="col-span-1 text-center">
                    <span className="font-mono text-sm" style={{ color: temasCount > 0 ? '#3b82f6' : '#6e7681' }}>
                      {temasCount}
                    </span>
                  </div>
                  <div className="col-span-1 text-center">
                    <span className="font-mono text-sm" style={{ color: '#a371f7' }}>0</span>
                  </div>
                  <div className="col-span-2">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-2 bg-background rounded-full overflow-hidden">
                        <div
                          className="h-full transition-all"
                          style={{
                            width: `${progress}%`,
                            backgroundColor: state.color
                          }}
                        />
                      </div>
                      <span className="text-xs font-mono">{progress.toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
                {isExpanded && (
                  <div className="p-6 bg-muted/30 border-t border-border">
                    <div className="grid grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <div className="text-sm">
                          <span className="text-muted-foreground">Cuerpo:</span>{' '}
                          <span className="font-medium">{opo.cuerpo}</span>
                        </div>
                        <div className="text-sm">
                          <span className="text-muted-foreground">Área:</span>{' '}
                          <span className="font-medium">{opo.area}</span>
                        </div>
                        {(opo.pipeline_started_at || opo.created_at) && (
                          <div className="text-sm">
                            <span className="text-muted-foreground">Pipeline iniciado:</span>{' '}
                            <span className="font-medium font-mono">
                              {new Date(opo.pipeline_started_at || opo.created_at).toLocaleString('es-ES')}
                            </span>
                          </div>
                        )}
                        {opo.error_msg && (
                          <div className="text-sm bg-destructive/10 border border-destructive/20 rounded p-2 mt-2">
                            <span className="text-destructive font-medium">⚠️ {opo.error_msg}</span>
                          </div>
                        )}
                      </div>
                      <div>
                        <div className="flex items-center gap-2 mb-4">
                          {PIPELINE_STATES.slice(0, 7).map((s, idx) => {
                            const isCompleted = PIPELINE_STATES.findIndex(st => st.id === opo.pipeline_state) > idx
                            const isCurrent = s.id === opo.pipeline_state
                            return (
                              <div key={s.id} className="flex items-center">
                                <div
                                  className={`w-8 h-8 rounded-full flex items-center justify-center text-xs transition-all ${
                                    isCurrent ? 'ring-2 ring-offset-2' : ''
                                  }`}
                                  style={{
                                    backgroundColor: isCompleted || isCurrent ? s.color : '#6e7681',
                                    ringColor: isCurrent ? s.color : 'transparent'
                                  }}
                                >
                                  {isCompleted ? '✓' : s.icon}
                                </div>
                                {idx < 6 && <div className="w-4 h-0.5 bg-border" />}
                              </div>
                            )
                          })}
                        </div>
                        <Link to={`/oposicion/${opo.id}`}>
                          <Button size="sm" variant="outline" className="mt-2">
                            Ver detalle completo →
                          </Button>
                        </Link>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </Card>
    </div>
  )
}
