import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import { useData } from '@/hooks/useData'

export default function Layout() {
  const { loading, error } = useData()

  if (loading) {
    return (
      <div className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-8 h-8 border-4 border-muted-foreground border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm text-muted-foreground font-mono">Conectando con la API...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <div className="text-center space-y-4 max-w-md">
          <p className="text-lg font-bold text-destructive">Error de conexion</p>
          <p className="text-sm text-muted-foreground">{error}</p>
          <p className="text-xs text-muted-foreground font-mono">Asegurate de que la API esta corriendo en localhost:8005</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
