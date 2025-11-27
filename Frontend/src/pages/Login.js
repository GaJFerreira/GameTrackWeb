import React from 'react';
import { Link } from 'react-router-dom';

const Login = () => {
  return (
    <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
      <div className="card bg-dark text-white p-5 rounded-4 shadow-lg border border-secondary border-opacity-25" style={{ maxWidth: '450px', width: '100%' }}>
        <h2 className="fw-bold mb-2 text-center">Bem-vindo de volta</h2>
        <p className="text-secondary text-center mb-4">Acesse sua biblioteca de jogos</p>
        
        <form>
          <div className="mb-3">
            <label className="form-label text-secondary small">Email</label>
            <input type="email" className="form-control form-control-dark" placeholder="seu@email.com" />
          </div>
          <div className="mb-4">
            <label className="form-label text-secondary small">Senha</label>
            <input type="password" className="form-control form-control-dark" placeholder="••••••••" />
          </div>
          <button className="btn btn-brand-red w-100 py-2 fw-bold mb-3">Entrar</button>
        </form>
        
        <p className="text-center text-secondary small">
          Não tem conta? <Link to="/cadastro" className="text-primary text-decoration-none">Cadastre-se</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;