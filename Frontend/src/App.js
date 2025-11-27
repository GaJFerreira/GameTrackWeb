import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// Importando componentes
import Navbar from './components/Navbar';

// Importando páginas
import Home from './pages/Home';
import Login from './pages/Login';
import Cadastro from './pages/Cadastro';
import Biblioteca from './pages/Biblioteca';
import Recomendacoes from './pages/Recomendacoes';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navbar aparece em todas as telas */}
        <Navbar />
        
        {/* As Rotas mudam o conteúdo abaixo da Navbar */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />
          <Route path="/biblioteca" element={<Biblioteca />} />
          <Route path="/recomendacoes" element={<Recomendacoes />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;