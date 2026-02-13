import { Link, useLocation } from 'react-router-dom'
import { AGENTS } from '@/constants/pipeline'
import oposicionesData from '@/data/oposiciones.json'

export default function Sidebar() {
  const location = useLocation()

  const agentsActive = oposicionesData.filter(o => o.agente_activo !== null).length

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/oposiciones', label: 'Oposiciones', icon: '📋' },
    { path: '/pipeline', label: 'Pipeline', icon: '🔄' },
    { path: '/agentes', label: 'Agentes', icon: '🤖' },
    { path: '/legislacion', label: 'Legislación', icon: '⚖️' },
  ]

  return (
    <div className="w-60 bg-card border-r border-border flex flex-col h-screen sticky top-0">
      <div className="p-6 border-b border-border">
        <h1 className="text-2xl font-bold font-mono">Typed</h1>
        <p className="text-xs text-muted-foreground mt-1">Pipeline Dashboard</p>
      </div>

      <nav className="flex-1 p-4">
        <div className="space-y-1">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-3 py-2 rounded-md transition-colors ${
                location.pathname === item.path
                  ? 'bg-accent text-accent-foreground'
                  : 'text-muted-foreground hover:bg-accent/50 hover:text-foreground'
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span className="text-sm font-medium">{item.label}</span>
            </Link>
          ))}
        </div>
      </nav>

      <div className="p-4 border-t border-border">
        <div className="bg-background rounded-md p-3">
          <div className="flex items-center gap-2 mb-2">
            <div className={`w-2 h-2 rounded-full ${agentsActive > 0 ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
            <span className="text-xs font-medium font-mono">
              {agentsActive > 0 ? 'Agentes activos' : 'Sistema en espera'}
            </span>
          </div>
          {agentsActive > 0 && (
            <p className="text-xs text-muted-foreground font-mono">
              {agentsActive} {agentsActive === 1 ? 'tarea activa' : 'tareas activas'}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
