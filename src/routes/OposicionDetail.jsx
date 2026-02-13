import { useParams, Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { PIPELINE_STATES, AGENTS, GRUPOS } from '@/constants/pipeline'
import oposicionesData from '@/data/oposiciones.json'
import temarioData from '@/data/temario.json'
import legislacionData from '@/data/legislacion.json'
import convocatoriasData from '@/data/convocatorias.json'
import examenesData from '@/data/examenes.json'

export default function OposicionDetail() {
  const { id } = useParams()
  const oposicion = oposicionesData.find(o => o.id === id)

  if (!oposicion) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold">Oposición no encontrada</h1>
        <Link to="/">
          <Button className="mt-4">← Volver al dashboard</Button>
        </Link>
      </div>
    )
  }

  const state = PIPELINE_STATES.find(s => s.id === oposicion.pipeline_state)
  const grupo = GRUPOS[oposicion.grupo]
  const agent = oposicion.agente_activo ? AGENTS.find(a => a.id === oposicion.agente_activo) : null

  // Get related data
  const temas = temarioData.filter(t => t.oposicion_id === id)
  const convocatorias = convocatoriasData.filter(c => c.oposicion_id === id)
  const examenes = examenesData.filter(e => {
    const convIds = convocatorias.map(c => c.id)
    return convIds.includes(e.convocatoria_id)
  })

  // Get unique leyes from temas
  const leyesIds = [...new Set(temas.flatMap(t => t.leyes_vinculadas))]
  const leyes = legislacionData.filter(l => leyesIds.includes(l.id))

  // Group temas by bloque
  const temasPorBloque = temas.reduce((acc, tema) => {
    if (!acc[tema.bloque]) {
      acc[tema.bloque] = []
    }
    acc[tema.bloque].push(tema)
    return acc
  }, {})

  // Group examenes by convocatoria
  const examenesPorConvocatoria = convocatorias.map(conv => ({
    convocatoria: conv,
    examenes: examenes.filter(e => e.convocatoria_id === conv.id)
  }))

  return (
    <div className="p-8 max-w-7xl">
      {/* Header */}
      <div className="mb-8">
        <Link to="/">
          <Button variant="ghost" size="sm" className="mb-4">
            ← Volver al dashboard
          </Button>
        </Link>

        <div className="flex items-start justify-between mb-4">
          <div>
            <h1 className="text-4xl font-bold mb-4">{oposicion.nombre}</h1>
            <div className="flex items-center gap-2 flex-wrap">
              <Badge
                style={{
                  backgroundColor: grupo.bg,
                  color: grupo.color,
                  border: `1px solid ${grupo.color}40`,
                  fontSize: '14px',
                  padding: '4px 12px'
                }}
              >
                Grupo {oposicion.grupo}
              </Badge>
              <Badge variant="outline" className="text-sm">
                {oposicion.ambito}
              </Badge>
              <Badge variant="outline" className="text-sm">
                {oposicion.organismo}
              </Badge>
              <Badge variant="outline" className="text-sm">
                {oposicion.area}
              </Badge>
            </div>
          </div>
          <div className="text-right">
            <Badge
              style={{
                backgroundColor: `${state.color}20`,
                color: state.color,
                border: `1px solid ${state.color}60`,
                fontSize: '14px',
                padding: '6px 14px'
              }}
            >
              {state.icon} {state.label}
            </Badge>
            {agent && (
              <div className="flex items-center gap-2 mt-2 justify-end">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                <span className="text-sm text-muted-foreground">
                  {agent.icon} {agent.name} trabajando
                </span>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mt-6">
          <Card>
            <CardContent className="pt-4">
              <div className="text-sm text-muted-foreground">Tipo de personal</div>
              <div className="text-lg font-medium">{oposicion.tipo_personal}</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-4">
              <div className="text-sm text-muted-foreground">Titulación requerida</div>
              <div className="text-lg font-medium">{oposicion.titulacion_requerida}</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-4">
              <div className="text-sm text-muted-foreground">Frecuencia estimada</div>
              <div className="text-lg font-medium">{oposicion.frecuencia_estimada}</div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="temario">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="temario">
            Temario ({temas.length})
          </TabsTrigger>
          <TabsTrigger value="convocatorias">
            Convocatorias ({convocatorias.length})
          </TabsTrigger>
          <TabsTrigger value="examenes">
            Exámenes ({examenes.length})
          </TabsTrigger>
          <TabsTrigger value="legislacion">
            Legislación ({leyes.length})
          </TabsTrigger>
        </TabsList>

        {/* Tab 1: Temario */}
        <TabsContent value="temario" className="mt-6">
          {temas.length === 0 ? (
            <Card>
              <CardContent className="pt-6">
                <p className="text-muted-foreground text-center">
                  El temario aún no ha sido extraído por el agente Excavador.
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-6">
              {Object.entries(temasPorBloque).map(([bloque, temas]) => (
                <Card key={bloque}>
                  <CardHeader>
                    <CardTitle>{bloque}</CardTitle>
                    <div className="text-sm text-muted-foreground">{temas.length} temas</div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {temas.map(tema => (
                        <div key={tema.id} className="p-4 border border-border rounded-md">
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex-1">
                              <div className="flex items-center gap-3 mb-2">
                                <span className="font-mono font-bold text-sm text-muted-foreground">
                                  Tema {tema.num_tema}
                                </span>
                                <span className={`text-xs px-2 py-0.5 rounded ${
                                  tema.prioridad === 'Alta' ? 'bg-red-500/20 text-red-500' :
                                  tema.prioridad === 'Media' ? 'bg-yellow-500/20 text-yellow-500' :
                                  'bg-green-500/20 text-green-500'
                                }`}>
                                  {tema.prioridad}
                                </span>
                                {tema.peso_examen_pct && (
                                  <span className="text-xs text-muted-foreground font-mono">
                                    Peso: {tema.peso_examen_pct}%
                                  </span>
                                )}
                              </div>
                              <div className="text-sm mb-2">{tema.titulo}</div>
                              {tema.leyes_vinculadas && tema.leyes_vinculadas.length > 0 && (
                                <div className="flex items-center gap-2 flex-wrap mt-2">
                                  <span className="text-xs text-muted-foreground">Leyes:</span>
                                  {tema.leyes_vinculadas.map(leyId => {
                                    const ley = legislacionData.find(l => l.id === leyId)
                                    return ley ? (
                                      <Badge key={leyId} variant="outline" className="text-xs">
                                        {ley.nombre_corto}
                                      </Badge>
                                    ) : null
                                  })}
                                </div>
                              )}
                              {tema.material_inap && (
                                <a
                                  href={tema.material_inap}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-xs text-blue-500 hover:underline mt-2 inline-block"
                                >
                                  📄 Material INAP →
                                </a>
                              )}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        {/* Tab 2: Convocatorias */}
        <TabsContent value="convocatorias" className="mt-6">
          {convocatorias.length === 0 ? (
            <Card>
              <CardContent className="pt-6">
                <p className="text-muted-foreground text-center">
                  No hay convocatorias registradas para esta oposición.
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              {convocatorias.map(conv => (
                <Card key={conv.id}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle>Convocatoria {conv.anyo}</CardTitle>
                        <div className="text-sm text-muted-foreground mt-1">{conv.tipo}</div>
                      </div>
                      <Badge
                        variant={conv.estado === 'Convocada' ? 'default' : 'secondary'}
                      >
                        {conv.estado}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div>
                        <div className="text-sm text-muted-foreground">Plazas totales</div>
                        <div className="text-2xl font-bold font-mono">{conv.plazas_total}</div>
                        <div className="text-xs text-muted-foreground mt-1">
                          {conv.plazas_libre} libre + {conv.plazas_interna} interna
                        </div>
                      </div>
                      <div>
                        <div className="text-sm text-muted-foreground">Fecha examen</div>
                        <div className="text-lg font-medium">
                          {new Date(conv.fecha_examen).toLocaleDateString('es-ES', {
                            day: 'numeric',
                            month: 'long',
                            year: 'numeric'
                          })}
                        </div>
                      </div>
                      <div>
                        <div className="text-sm text-muted-foreground">Nota corte teórico</div>
                        <div className="text-2xl font-bold font-mono">{conv.nota_corte_teorico}</div>
                      </div>
                      <div>
                        <div className="text-sm text-muted-foreground">Ratio opos/plaza</div>
                        <div className="text-2xl font-bold font-mono">{conv.ratio_opositores_plaza}</div>
                      </div>
                    </div>
                    <div className="mt-4 flex items-center gap-4 text-sm">
                      <div>
                        <span className="text-muted-foreground">Publicación:</span>{' '}
                        {new Date(conv.fecha_publicacion).toLocaleDateString('es-ES')}
                      </div>
                      <div>
                        <span className="text-muted-foreground">Fin plazo:</span>{' '}
                        {new Date(conv.fecha_fin_plazo).toLocaleDateString('es-ES')}
                      </div>
                      <a
                        href={conv.url_boe}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-500 hover:underline ml-auto"
                      >
                        Ver en BOE →
                      </a>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        {/* Tab 3: Exámenes */}
        <TabsContent value="examenes" className="mt-6">
          {examenes.length === 0 ? (
            <Card>
              <CardContent className="pt-6">
                <p className="text-muted-foreground text-center">
                  No hay exámenes registrados aún. El agente Arqueólogo está buscando...
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-6">
              {examenesPorConvocatoria.filter(e => e.examenes.length > 0).map(({ convocatoria, examenes }) => (
                <Card key={convocatoria.id}>
                  <CardHeader>
                    <CardTitle>Exámenes {convocatoria.anyo}</CardTitle>
                    <div className="text-sm text-muted-foreground">{examenes.length} examen{examenes.length > 1 ? 'es' : ''}</div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {examenes.map(examen => (
                        <div key={examen.id} className="p-4 border border-border rounded-md">
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex-1">
                              <div className="flex items-center gap-3 mb-2">
                                <span className="font-medium">{examen.tipo_prueba}</span>
                                <Badge variant="outline">{examen.turno}</Badge>
                                {examen.modelo !== 'Único' && (
                                  <Badge variant="outline">Modelo {examen.modelo}</Badge>
                                )}
                                <Badge
                                  variant={examen.verificado ? 'default' : 'secondary'}
                                  className="text-xs"
                                >
                                  {examen.verificado ? '✓ Verificado' : 'Sin verificar'}
                                </Badge>
                              </div>
                              <div className="text-sm text-muted-foreground mb-2">
                                {examen.num_preguntas} preguntas · Fuente: {examen.fuente}
                              </div>
                              <div className="flex gap-2">
                                <a
                                  href={examen.pdf_examen_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-xs text-blue-500 hover:underline"
                                >
                                  📄 PDF Examen
                                </a>
                                <a
                                  href={examen.pdf_plantilla_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-xs text-blue-500 hover:underline"
                                >
                                  📄 PDF Plantilla
                                </a>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        {/* Tab 4: Legislación Vinculada */}
        <TabsContent value="legislacion" className="mt-6">
          {leyes.length === 0 ? (
            <Card>
              <CardContent className="pt-6">
                <p className="text-muted-foreground text-center">
                  No hay legislación vinculada disponible. El agente Decodificador está trabajando...
                </p>
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="pt-6">
                <div className="space-y-3">
                  {leyes
                    .map(ley => {
                      const countInThisOpo = temas.filter(t =>
                        t.leyes_vinculadas.includes(ley.id)
                      ).length
                      return { ...ley, countInThisOpo }
                    })
                    .sort((a, b) => b.countInThisOpo - a.countInThisOpo)
                    .map(ley => (
                      <div key={ley.id} className="p-4 border border-border rounded-md">
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              <span className="font-mono font-bold text-sm">{ley.referencia}</span>
                              <Badge variant="outline">{ley.nombre_corto}</Badge>
                              <span className="text-xs text-muted-foreground">
                                Referenciada en {ley.countInThisOpo} tema{ley.countInThisOpo > 1 ? 's' : ''}
                              </span>
                            </div>
                            <div className="text-sm mb-2">{ley.nombre_completo}</div>
                            <a
                              href={ley.url_boe}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-xs text-blue-500 hover:underline"
                            >
                              Ver en BOE →
                            </a>
                          </div>
                        </div>
                      </div>
                    ))}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
