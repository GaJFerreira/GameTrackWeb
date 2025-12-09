import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

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
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = () => setIsAuthenticated(true);
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="App">
        <ToastContainer 
          position="bottom-right"
          autoClose={3000}
          theme="dark"
        />

        <Navbar isLoggedIn={isAuthenticated} />
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/cadastro" element={<Cadastro />} />
          <Route path="/biblioteca" element={<Biblioteca />} />
          <Route path="/recomendacoes" element={<Recomendacoes />} />
          <Route path="/jogo/:id" element={<GameDetails />} />
          <Route path="/metas" element={<Metas />} />
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