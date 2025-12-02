import React, { useState } from 'react'; // Adicione useState
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Cadastro from './pages/Cadastro';
import Biblioteca from './pages/Biblioteca';
import Recomendacoes from './pages/Recomendacoes';
import GameDetails from './pages/GameDetails';
import Perfil from './pages/Perfil';
import Metas from './pages/Metas';

function App() {
  // Estado que controla se o usuário está logado (começa falso)
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Função chamada pela tela de Login para liberar o acesso
  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  // Função para deslogar (opcional, pode ser usada no Perfil)
  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="App">
        {/* Passamos o estado para a Navbar saber o que mostrar */}
        <Navbar isLoggedIn={isAuthenticated} />
        
        <Routes>
          <Route path="/" element={<Home />} />
          
          {/* Passamos a função handleLogin para a tela de Login */}
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          
          <Route path="/cadastro" element={<Cadastro />} />
          <Route path="/biblioteca" element={<Biblioteca />} />
          <Route path="/recomendacoes" element={<Recomendacoes />} />
          <Route path="/jogo/:id" element={<GameDetails />} />
          <Route path="/metas" element={<Metas />} />
          
          {/* Protegemos a rota de Perfil (se não tiver logado, volta pro Login) */}
          <Route 
            path="/perfil" 
            element={isAuthenticated ? <Perfil onLogout={handleLogout} /> : <Navigate to="/login" />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;