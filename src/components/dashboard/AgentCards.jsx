import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { AGENTS } from '@/constants/pipeline'
import { useData } from '@/hooks/useData'

export default function AgentCards() {
  const { oposiciones: oposicionesData } = useData()
  return (
    <div className="grid grid-cols-4 gap-4">
      {AGENTS.map(agent => {
        const activeCount = oposicionesData.filter(o => o.agente_activo === agent.id).length
        const isActive = activeCount > 0
        return (
          <Card key={agent.id} className={`transition-all ${isActive ? 'ring-2' : ''}`} style={{ ringColor: isActive ? agent.color : 'transparent' }}>
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <span className="text-2xl">{agent.icon}</span>
                {isActive && (
                  <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: agent.color }} />
                )}
              </div>
              <CardTitle className="text-lg">{agent.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground mb-2">{agent.description}</p>
              <div className="flex items-center justify-between text-xs">
                <span className="text-muted-foreground font-mono">{agent.cron}</span>
                <span className="font-mono font-medium" style={{ color: isActive ? agent.color : '#6e7681' }}>
                  {isActive ? `${activeCount} activa${activeCount > 1 ? 's' : ''}` : 'En espera'}
                </span>
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
