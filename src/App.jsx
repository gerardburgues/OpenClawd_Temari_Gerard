import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './routes/Dashboard'
import Oposiciones from './routes/Oposiciones'
import Pipeline from './routes/Pipeline'
import Agentes from './routes/Agentes'
import OposicionDetail from './routes/OposicionDetail'
import Legislacion from './routes/Legislacion'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="oposiciones" element={<Oposiciones />} />
          <Route path="pipeline" element={<Pipeline />} />
          <Route path="agentes" element={<Agentes />} />
          <Route path="oposicion/:id" element={<OposicionDetail />} />
          <Route path="legislacion" element={<Legislacion />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
