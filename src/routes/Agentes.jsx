import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AGENTS, GRUPOS } from '@/constants/pipeline'
import { useData } from '@/hooks/useData'

export default function Agentes() {
  const { oposiciones: oposicionesData } = useData()
  return (
    <div className="p-8 space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Agentes en Acción</h1>
        <p className="text-muted-foreground">Vista Kanban de oposiciones organizadas por agente activo</p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        {AGENTS.map(agent => {
          const activeOpos = oposicionesData.filter(o => o.agente_activo === agent.id)
          return (
            <Card key={agent.id}>
              <CardHeader style={{ borderBottom: `2px solid ${agent.color}` }}>
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{agent.icon}</span>
                  <div className="flex-1">
                    <CardTitle>{agent.name}</CardTitle>
                    <div className="text-xs text-muted-foreground mt-1">{agent.description}</div>
                  </div>
                  {activeOpos.length > 0 && (
                    <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: agent.color }} />
                  )}
                </div>
                <div className="text-xs text-muted-foreground font-mono mt-2">{agent.cron}</div>
              </CardHeader>
              <CardContent className="pt-4">
                {activeOpos.length > 0 && (
                  <div className="mb-4">
                    <div className="text-xs font-medium text-muted-foreground mb-2">Procesando ahora</div>
                    <div className="space-y-2">
                      {activeOpos.map(opo => (
                        <Link key={opo.id} to={`/oposicion/${opo.id}`}>
                          <div className="p-2 rounded border border-border bg-card hover:bg-accent/50 transition-colors">
                            <div className="text-sm font-medium">{opo.nombre}</div>
                            <div className="flex items-center gap-2 mt-1">
                              <Badge style={{ backgroundColor: GRUPOS[opo.grupo].bg, color: GRUPOS[opo.grupo].color, fontSize: '10px' }}>
                                {opo.grupo}
                              </Badge>
                              <span className="text-xs text-muted-foreground">{opo.ambito}</span>
                            </div>
                          </div>
                        </Link>
                      ))}
                    </div>
                  </div>
                )}
                <div className="text-xs text-muted-foreground">
                  {activeOpos.length === 0 ? 'Sin tareas activas' : `${activeOpos.length} tarea${activeOpos.length > 1 ? 's' : ''} activa${activeOpos.length > 1 ? 's' : ''}`}
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
