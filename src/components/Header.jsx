import { useLocation, Link } from 'react-router-dom'
import { useData } from '@/hooks/useData'

export default function Header() {
  const location = useLocation()
  const { oposiciones: oposicionesData, lastUpdate } = useData()

  const getBreadcrumbs = () => {
    const path = location.pathname

    if (path === '/') {
      return [{ label: 'Dashboard', path: '/' }]
    }

    if (path === '/oposiciones') {
      return [
        { label: 'Dashboard', path: '/' },
        { label: 'Oposiciones', path: '/oposiciones' }
      ]
    }

    if (path === '/pipeline') {
      return [
        { label: 'Dashboard', path: '/' },
        { label: 'Pipeline', path: '/pipeline' }
      ]
    }

    if (path === '/agentes') {
      return [
        { label: 'Dashboard', path: '/' },
        { label: 'Agentes', path: '/agentes' }
      ]
    }

    if (path === '/legislacion') {
      return [
        { label: 'Dashboard', path: '/' },
        { label: 'Legislación', path: '/legislacion' }
      ]
    }

    if (path.startsWith('/oposicion/')) {
      const id = path.split('/')[2]
      const opo = oposicionesData.find(o => o.id === id)
      return [
        { label: 'Dashboard', path: '/' },
        { label: opo?.nombre || 'Oposición', path: path }
      ]
    }

    return [{ label: 'Dashboard', path: '/' }]
  }

  const breadcrumbs = getBreadcrumbs()
  const pipelineActive = oposicionesData.some(o => o.agente_activo !== null)

  return (
    <header className="h-14 border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-10">
      <div className="h-full px-6 flex items-center justify-between">
        <nav className="flex items-center gap-2 text-sm">
          {breadcrumbs.map((crumb, index) => (
            <div key={crumb.path} className="flex items-center gap-2">
              {index > 0 && <span className="text-muted-foreground">/</span>}
              {index === breadcrumbs.length - 1 ? (
                <span className="font-medium">{crumb.label}</span>
              ) : (
                <Link
                  to={crumb.path}
                  className="text-muted-foreground hover:text-foreground transition-colors"
                >
                  {crumb.label}
                </Link>
              )}
            </div>
          ))}
        </nav>

        <div className="flex items-center gap-4">
          {lastUpdate && (
            <span className="text-xs text-muted-foreground font-mono">
              {lastUpdate.toLocaleTimeString('es-ES')}
            </span>
          )}
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${pipelineActive ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
            <span className="text-xs font-medium font-mono">
              {pipelineActive ? 'Pipeline activo' : 'Pipeline en espera'}
            </span>
          </div>
        </div>
      </div>
    </header>
  )
}
