import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.post('/auth/login', {
        email: email,
        password: password
      });

      const { id_token, refresh_token } = response.data;

      localStorage.setItem('token', id_token);
      localStorage.setItem('refreshToken', refresh_token);

      navigate('/biblioteca'); 
      
    } catch (err) {
      console.error(err);
      setError("Email ou senha inválidos.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
      <div className="card bg-dark text-white p-5 rounded-4 shadow-lg border border-secondary border-opacity-25" style={{ maxWidth: '450px', width: '100%' }}>
        <h2 className="fw-bold mb-2 text-center">Bem-vindo de volta</h2>
        <p className="text-secondary text-center mb-4">Acesse sua biblioteca de jogos</p>
        
        {error && <div className="alert alert-danger small py-2">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label text-secondary small">Email</label>
            <input 
              type="email" 
              className="form-control form-control-dark" 
              placeholder="seu@email.com" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label className="form-label text-secondary small">Senha</label>
            <input 
              type="password" 
              className="form-control form-control-dark" 
              placeholder="••••••••" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button 
            className="btn btn-brand-red w-100 py-2 fw-bold mb-3"
            disabled={loading}
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
        
        <p className="text-center text-secondary small">
          Não tem conta? <Link to="/cadastro" className="text-primary text-decoration-none">Cadastre-se</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;