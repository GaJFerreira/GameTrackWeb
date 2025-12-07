import React, { useState, useEffect } from 'react';
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

  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return !!localStorage.getItem('token'); 
  });

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="App">
        <Navbar isLoggedIn={isAuthenticated} />
        
        <Routes>
          <Route path="/" element={<Home />} />
          
          {/* Se já estiver logado, redireciona login/cadastro para biblioteca */}
          <Route 
            path="/login" 
            element={!isAuthenticated ? <Login onLogin={handleLogin} /> : <Navigate to="/biblioteca" />} 
          />
          <Route 
            path="/cadastro" 
            element={!isAuthenticated ? <Cadastro /> : <Navigate to="/biblioteca" />} 
          />

          {/* ROTAS PROTEGIDAS (Protected Routes) */}
          {/* Se NÃO estiver logado, manda pro login */}
          <Route 
            path="/biblioteca" 
            element={isAuthenticated ? <Biblioteca /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/recomendacoes" 
            element={isAuthenticated ? <Recomendacoes /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/metas" 
            element={isAuthenticated ? <Metas /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/perfil" 
            element={isAuthenticated ? <Perfil onLogout={handleLogout} /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/jogo/:id" 
            element={isAuthenticated ? <GameDetails /> : <Navigate to="/login" />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;