import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function StatsCards({ stats }) {
  return (
    <div className="grid grid-cols-7 gap-4">
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-muted-foreground">Total</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold font-mono">{stats.total}</div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-muted-foreground">Completas</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold font-mono" style={{ color: '#3fb950' }}>{stats.completas}</div>
          <div className="text-xs text-muted-foreground mt-1">{((stats.completas / stats.total) * 100).toFixed(1)}%</div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-muted-foreground">En proceso</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold font-mono" style={{ color: '#d29922' }}>{stats.enProceso}</div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-muted-foreground">Temas</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold font-mono" style={{ color: '#3b82f6' }}>{stats.totalTemas}</div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-muted-foreground">Leyes</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold font-mono" style={{ color: '#06b6d4' }}>{stats.totalLeyes}</div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-muted-foreground">Exámenes</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold font-mono" style={{ color: '#a371f7' }}>{stats.totalExamenes}</div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-muted-foreground">Errores</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold font-mono" style={{ color: '#f85149' }}>{stats.errores}</div>
        </CardContent>
      </Card>
    </div>
  )
}
