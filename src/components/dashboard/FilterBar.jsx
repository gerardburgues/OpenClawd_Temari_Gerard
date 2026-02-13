import { Input } from '@/components/ui/input'
import { PIPELINE_STATES, GRUPOS } from '@/constants/pipeline'

export default function FilterBar({
  searchTerm,
  setSearchTerm,
  filterAmbito,
  setFilterAmbito,
  filterGrupo,
  setFilterGrupo,
  filterState,
  setFilterState,
  ambitos,
  resultCount
}) {
  return (
    <div className="flex items-center gap-4">
      <Input
        placeholder="Buscar por nombre u organismo..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="max-w-xs"
      />
      <select
        value={filterAmbito}
        onChange={(e) => setFilterAmbito(e.target.value)}
        className="h-9 rounded-md border border-input bg-background px-3 text-sm"
      >
        {ambitos.map(a => <option key={a} value={a}>{a}</option>)}
      </select>
      <select
        value={filterGrupo}
        onChange={(e) => setFilterGrupo(e.target.value)}
        className="h-9 rounded-md border border-input bg-background px-3 text-sm"
      >
        <option value="Todos">Todos los grupos</option>
        {Object.keys(GRUPOS).map(g => <option key={g} value={g}>{g}</option>)}
      </select>
      <select
        value={filterState}
        onChange={(e) => setFilterState(e.target.value)}
        className="h-9 rounded-md border border-input bg-background px-3 text-sm"
      >
        <option value="Todos">Todos los estados</option>
        {PIPELINE_STATES.map(s => <option key={s.id} value={s.id}>{s.label}</option>)}
      </select>
      <div className="flex-1" />
      {resultCount !== undefined && (
        <span className="text-sm text-muted-foreground font-mono">
          {resultCount} {resultCount === 1 ? 'resultado' : 'resultados'}
        </span>
      )}
    </div>
  )
}
