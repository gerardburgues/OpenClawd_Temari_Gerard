// Estados del pipeline (en orden)
export const PIPELINE_STATES = [
  { id: "descubierta", label: "Descubierta", icon: "🔍", color: "#8b949e" },
  { id: "extrayendo_temario", label: "Extrayendo temario", icon: "⚙️", color: "#d29922" },
  { id: "temario_ok", label: "Temario OK", icon: "📚", color: "#3b82f6" },
  { id: "decodificando_leyes", label: "Decodificando leyes", icon: "🔍", color: "#8b5cf6" },
  { id: "leyes_ok", label: "Leyes OK", icon: "⚖️", color: "#06b6d4" },
  { id: "buscando_examenes", label: "Buscando exámenes", icon: "🔎", color: "#a371f7" },
  { id: "completa", label: "Completa", icon: "✅", color: "#3fb950" },
  { id: "error", label: "Error", icon: "❌", color: "#f85149" },
];

// Agentes
export const AGENTS = [
  { id: "censador", name: "Censador", icon: "🗺️", color: "#d29922", cron: "*/2 min", description: "Descubre oposiciones" },
  { id: "excavador", name: "Excavador", icon: "⛏️", color: "#3b82f6", cron: "*/3 min", description: "Extrae temarios" },
  { id: "decodificador", name: "Decodificador", icon: "🔍", color: "#8b5cf6", cron: "*/4 min", description: "Mapea temas → leyes" },
  { id: "arqueologo", name: "Arqueólogo", icon: "🏺", color: "#a371f7", cron: "*/5 min", description: "Busca exámenes" },
];

// Grupos y sus colores
export const GRUPOS = {
  A1: { color: "#e94560", bg: "rgba(233,69,96,0.12)" },
  A2: { color: "#457b9d", bg: "rgba(69,123,157,0.12)" },
  C1: { color: "#2a9d8f", bg: "rgba(42,157,143,0.12)" },
  C2: { color: "#e9c46a", bg: "rgba(233,196,106,0.12)" },
  AP: { color: "#f4a261", bg: "rgba(244,162,97,0.12)" },
};
