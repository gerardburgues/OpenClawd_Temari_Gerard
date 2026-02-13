import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { PIPELINE_STATES, AGENTS } from '@/constants/pipeline'
import { useOposicionesStats } from '@/hooks/useOposicionesStats'
import AgentCards from '@/components/dashboard/AgentCards'
import StatsCards from '@/components/dashboard/StatsCards'
import oposicionesData from '@/data/oposiciones.json'
import activityLogData from '@/data/activity-log.json'

export default function Dashboard() {
  const [showActivityLog, setShowActivityLog] = useState(true)
  const [activityFilter, setActivityFilter] = useState([])

  const stats = useOposicionesStats()

  // Calculate progress by state
  const progressByState = useMemo(() => {
    return PIPELINE_STATES.slice(0, 7).map(state => ({
      ...state,
      count: oposicionesData.filter(o => o.pipeline_state === state.id).length
    }))
  }, [])

  // Filter activity log
  const filteredActivityLog = useMemo(() => {
    if (activityFilter.length === 0) return activityLogData
    return activityLogData.filter(log => activityFilter.includes(log.agente_id))
  }, [activityFilter])

  const toggleActivityFilter = (agentId) => {
    setActivityFilter(prev =>
      prev.includes(agentId) ? prev.filter(id => id !== agentId) : [...prev, agentId]
    )
  }

  return (
    <div className="p-8 space-y-8">
      {/* Agent Cards */}
      <AgentCards />

      {/* Stats Cards */}
      <StatsCards stats={stats} />

      {/* Global Progress Bar */}
      <Card>
        <CardHeader>
          <CardTitle>Progreso Global del Pipeline</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex h-8 rounded overflow-hidden bg-background">
            {progressByState.map((state, index) => {
              const percentage = (state.count / oposicionesData.length) * 100
              return percentage > 0 ? (
                <div
                  key={state.id}
                  className="flex items-center justify-center text-xs font-mono font-semibold text-white transition-all hover:opacity-80"
                  style={{
                    width: `${percentage}%`,
                    backgroundColor: state.color
                  }}
                  title={`${state.label}: ${state.count}`}
                >
                  {percentage > 5 && state.count}
                </div>
              ) : null
            })}
          </div>
          <div className="grid grid-cols-7 gap-2 mt-4">
            {progressByState.map(state => (
              <div key={state.id} className="flex items-center gap-2">
                <div className="w-3 h-3 rounded" style={{ backgroundColor: state.color }} />
                <div className="flex-1 min-w-0">
                  <div className="text-xs font-medium truncate">{state.label}</div>
                  <div className="text-xs text-muted-foreground font-mono">{state.count}</div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Quick Navigation Cards */}
      <div className="grid grid-cols-3 gap-4">
        <Link to="/oposiciones">
          <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="text-2xl">📋</span>
                Ver todas las oposiciones
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Accede a la vista de tabla completa con todas las oposiciones, filtros y detalles expandibles.
              </p>
            </CardContent>
          </Card>
        </Link>
        <Link to="/pipeline">
          <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="text-2xl">🔄</span>
                Ver pipeline completo
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Visualiza las oposiciones organizadas por estado del pipeline en vista Kanban.
              </p>
            </CardContent>
          </Card>
        </Link>
        <Link to="/agentes">
          <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="text-2xl">🤖</span>
                Ver agentes en acción
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Observa qué oposiciones está procesando cada agente en tiempo real.
              </p>
            </CardContent>
          </Card>
        </Link>
      </div>

      {/* Activity Log */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Log de Actividad de Agentes</CardTitle>
            <div className="flex items-center gap-2">
              {AGENTS.map(agent => (
                <Button
                  key={agent.id}
                  size="sm"
                  variant={activityFilter.includes(agent.id) ? 'default' : 'outline'}
                  onClick={() => toggleActivityFilter(agent.id)}
                  className="text-xs"
                >
                  {agent.icon} {agent.name}
                </Button>
              ))}
              <Button
                size="sm"
                variant="ghost"
                onClick={() => setShowActivityLog(!showActivityLog)}
              >
                {showActivityLog ? '▼' : '▶'}
              </Button>
            </div>
          </div>
        </CardHeader>
        {showActivityLog && (
          <CardContent>
            <div className="bg-background rounded-md p-4 font-mono text-xs max-h-96 overflow-y-auto space-y-1">
              {filteredActivityLog.slice(0, 50).map(log => {
                const agent = AGENTS.find(a => a.id === log.agente_id)
                const typeColors = {
                  success: '#3fb950',
                  error: '#f85149',
                  warning: '#d29922',
                  info: '#8b949e'
                }
                return (
                  <div key={log.id} className="flex items-start gap-3 py-1">
                    <span className="text-muted-foreground">{new Date(log.timestamp).toLocaleTimeString('es-ES')}</span>
                    <span>{agent?.icon}</span>
                    <span className="text-muted-foreground">{agent?.name}</span>
                    <span>→</span>
                    <span style={{ color: typeColors[log.tipo] }}>{log.mensaje}</span>
                  </div>
                )
              })}
            </div>
          </CardContent>
        )}
      </Card>
    </div>
  )
}
