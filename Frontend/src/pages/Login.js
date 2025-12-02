import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

// Recebemos a função onLogin vinda do App.js
const Login = ({ onLogin }) => {
  const navigate = useNavigate(); // Hook para redirecionar o usuário

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // AQUI VALIDARIA NO BACKEND (Futuro)
    // Por enquanto, apenas simulamos o sucesso:
    
    onLogin(); // 1. Avisa o App que logou
    navigate('/perfil'); // 2. Redireciona para o Perfil
  };

  return (
    <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
      <div className="card bg-dark text-white p-5 rounded-4 shadow-lg border border-secondary border-opacity-25" style={{ maxWidth: '450px', width: '100%' }}>
        <h2 className="fw-bold mb-2 text-center">Bem-vindo de volta</h2>
        <p className="text-secondary text-center mb-4">Acesse sua biblioteca de jogos</p>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label text-secondary small">Email</label>
            <input type="email" required className="form-control form-control-dark" placeholder="seu@email.com" />
          </div>
          <div className="mb-4">
            <label className="form-label text-secondary small">Senha</label>
            <input type="password" required className="form-control form-control-dark" placeholder="••••••••" />
          </div>
          <button type="submit" className="btn btn-brand-red w-100 py-2 fw-bold mb-3">Entrar</button>
        </form>
        
        <p className="text-center text-secondary small">
          Não tem conta? <Link to="/cadastro" className="text-primary text-decoration-none">Cadastre-se</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;