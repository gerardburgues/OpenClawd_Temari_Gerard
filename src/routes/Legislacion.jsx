import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import legislacionData from '@/data/legislacion.json'
import temarioData from '@/data/temario.json'
import oposicionesData from '@/data/oposiciones.json'
import { GRUPOS } from '@/constants/pipeline'

export default function Legislacion() {
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('veces_referenciada') // or 'referencia'
  const [sortOrder, setSortOrder] = useState('desc')
  const [expandedLey, setExpandedLey] = useState(null)

  // Filter and sort legislation
  const filteredLeyes = useMemo(() => {
    let filtered = legislacionData.filter(ley =>
      ley.referencia.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ley.nombre_corto.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ley.nombre_completo.toLowerCase().includes(searchTerm.toLowerCase())
    )

    filtered.sort((a, b) => {
      const aValue = a[sortBy]
      const bValue = b[sortBy]
      const order = sortOrder === 'asc' ? 1 : -1

      if (typeof aValue === 'string') {
        return aValue.localeCompare(bValue) * order
      }
      return (aValue - bValue) * order
    })

    return filtered
  }, [searchTerm, sortBy, sortOrder])

  const toggleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(field)
      setSortOrder('desc')
    }
  }

  const getOposicionesForLey = (leyId) => {
    const temasWithLey = temarioData.filter(t => t.leyes_vinculadas.includes(leyId))
    const oposicionIds = [...new Set(temasWithLey.map(t => t.oposicion_id))]
    const oposiciones = oposicionesData.filter(o => oposicionIds.includes(o.id))
    return oposiciones.map(opo => ({
      ...opo,
      temasCount: temasWithLey.filter(t => t.oposicion_id === opo.id).length
    }))
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Catálogo de Legislación</h1>
        <p className="text-muted-foreground">
          {legislacionData.length} leyes catalogadas y verificadas
        </p>
      </div>

      <div className="flex items-center gap-4 mb-6">
        <Input
          placeholder="Buscar por referencia, nombre corto o nombre completo..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="max-w-md"
        />
        <div className="flex-1" />
        <span className="text-sm text-muted-foreground font-mono">
          {filteredLeyes.length} {filteredLeyes.length === 1 ? 'resultado' : 'resultados'}
        </span>
      </div>

      <Card>
        <div className="divide-y divide-border">
          {/* Table Header */}
          <div className="grid grid-cols-12 gap-4 p-4 text-xs font-medium text-muted-foreground bg-muted/50">
            <div
              className="col-span-2 cursor-pointer hover:text-foreground flex items-center gap-1"
              onClick={() => toggleSort('referencia')}
            >
              Referencia
              {sortBy === 'referencia' && (
                <span>{sortOrder === 'asc' ? '↑' : '↓'}</span>
              )}
            </div>
            <div className="col-span-2">Nombre Corto</div>
            <div className="col-span-4">Nombre Completo</div>
            <div
              className="col-span-2 cursor-pointer hover:text-foreground flex items-center gap-1"
              onClick={() => toggleSort('veces_referenciada')}
            >
              Referencias
              {sortBy === 'veces_referenciada' && (
                <span>{sortOrder === 'asc' ? '↑' : '↓'}</span>
              )}
            </div>
            <div className="col-span-2 text-right">Última Verificación</div>
          </div>

          {/* Table Rows */}
          {filteredLeyes.map(ley => {
            const isExpanded = expandedLey === ley.id
            const oposicionesWithLey = getOposicionesForLey(ley.id)

            return (
              <div key={ley.id}>
                <div
                  className="grid grid-cols-12 gap-4 p-4 hover:bg-accent/50 cursor-pointer transition-colors"
                  onClick={() => setExpandedLey(isExpanded ? null : ley.id)}
                >
                  <div className="col-span-2">
                    <span className="font-mono font-bold text-sm">{ley.referencia}</span>
                  </div>
                  <div className="col-span-2">
                    <Badge variant="outline">{ley.nombre_corto}</Badge>
                  </div>
                  <div className="col-span-4">
                    <div className="text-sm">{ley.nombre_completo}</div>
                  </div>
                  <div className="col-span-2">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-lg font-bold">{ley.veces_referenciada}</span>
                      <span className="text-xs text-muted-foreground">temas</span>
                    </div>
                  </div>
                  <div className="col-span-2 text-right">
                    <div className="text-xs text-muted-foreground font-mono">
                      {new Date(ley.fecha_verificacion).toLocaleDateString('es-ES')}
                    </div>
                    <a
                      href={ley.url_boe}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-blue-500 hover:underline"
                      onClick={(e) => e.stopPropagation()}
                    >
                      Ver en BOE →
                    </a>
                  </div>
                </div>

                {isExpanded && (
                  <div className="p-6 bg-muted/30 border-t border-border">
                    <div className="mb-4">
                      <h3 className="font-semibold mb-2">
                        Oposiciones que referencian esta ley ({oposicionesWithLey.length})
                      </h3>
                      {oposicionesWithLey.length === 0 ? (
                        <p className="text-sm text-muted-foreground">
                          Esta ley aún no está vinculada a ninguna oposición en el sistema.
                        </p>
                      ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                          {oposicionesWithLey
                            .sort((a, b) => b.temasCount - a.temasCount)
                            .map(opo => {
                              const grupo = GRUPOS[opo.grupo]
                              return (
                                <Link key={opo.id} to={`/oposicion/${opo.id}`}>
                                  <div className="p-3 rounded border border-border bg-card hover:bg-accent/50 transition-colors">
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
                                      <Badge variant="outline" className="text-xs">
                                        {opo.ambito}
                                      </Badge>
                                    </div>
                                    <div className="text-xs text-muted-foreground">
                                      Referenciada en {opo.temasCount} tema{opo.temasCount > 1 ? 's' : ''}
                                    </div>
                                  </div>
                                </Link>
                              )
                            })}
                        </div>
                      )}
                    </div>

                    <div className="mt-4 pt-4 border-t border-border">
                      <h4 className="text-sm font-semibold mb-2">Detalles de la ley</h4>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-muted-foreground">Referencia completa:</span>{' '}
                          <span className="font-medium">{ley.referencia}</span>
                        </div>
                        <div>
                          <span className="text-muted-foreground">Total de referencias:</span>{' '}
                          <span className="font-medium font-mono">{ley.veces_referenciada}</span>
                        </div>
                        <div className="col-span-2">
                          <span className="text-muted-foreground">Nombre oficial:</span>{' '}
                          <span className="font-medium">{ley.nombre_completo}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </Card>

      {filteredLeyes.length === 0 && (
        <div className="text-center py-12">
          <p className="text-muted-foreground">
            No se encontraron leyes que coincidan con tu búsqueda.
          </p>
        </div>
      )}
    </div>
  )
}
