import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { toast } from 'react-toastify';

const Cadastro = () => {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    steamId: '',
    email: '',
    password: ''
  });
  
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { value, type } = e.target;

    if (type === "email") {
      setFormData(prev => ({ ...prev, email: value }));
    } else if (type === "password") {
      setFormData(prev => ({ ...prev, password: value }));
    } else {
      setFormData(prev => ({ ...prev, steamId: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await api.post("/auth/register", {
        email: formData.email,
        password: formData.password,
        steam_id: formData.steamId
      });
      toast("Conta criada com sucesso!.");

      const loginResponse = await api.post("/auth/login", {
        email: formData.email,
        password: formData.password
      });

      const { id_token, refresh_token } = loginResponse.data;
      localStorage.setItem("token", id_token);
      localStorage.setItem("refreshToken", refresh_token);
      
      toast("Conta criada! Bem-vindo.");

      navigate("/biblioteca");

    } catch (err) {
        console.error(err);
        const msg = err.response?.data?.detail || "Erro ao realizar cadastro.";
        setError(msg);

    } finally {
        setLoading(false);
    }
    
      };

  return (
    <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
      <div className="card bg-dark text-white p-5 rounded-4 shadow-lg border border-secondary border-opacity-25" style={{ maxWidth: '450px', width: '100%' }}>
        <h2 className="fw-bold mb-2 text-center">Crie sua Conta</h2>
        <p className="text-secondary text-center mb-4">Sincronize sua biblioteca Steam</p>

        {error && <div className="alert alert-danger small py-2">{error}</div>}

        <form onSubmit={handleSubmit}>
          
          {/* STEAM ID */}
          <div className="mb-3">
            <div className="d-flex justify-content-between">
              <label className="form-label text-secondary small">Steam ID (64-bit)</label>
              <a
                href="https://store.steampowered.com/account/"
                target="_blank"
                rel="noreferrer"
                className="small text-primary text-decoration-none"
                style={{ fontSize: '0.75rem' }}
              >
                Onde encontrar?
              </a>
            </div>

            <input
              type="text"
              className="form-control form-control-dark"
              placeholder="Ex: 76561198000000000"
              value={formData.steamId}
              onChange={handleInputChange}
              required
              minLength={17}
            />
          </div>

          {/* EMAIL */}
          <div className="mb-3">
            <label className="form-label text-secondary small">Email</label>
            <input
              type="email"
              className="form-control form-control-dark"
              placeholder="seu@email.com"
              value={formData.email}
              onChange={handleInputChange}
              required
            />
          </div>

          {/* SENHA */}
          <div className="mb-4">
            <label className="form-label text-secondary small">Senha</label>
            <input
              type="password"
              className="form-control form-control-dark"
              placeholder="••••••••"
              value={formData.password}
              onChange={handleInputChange}
              required
              minLength={6}
            />
          </div>

          {/* BOTÃO */}
          <button
            className="btn btn-brand-red w-100 py-2 fw-bold mb-3"
            disabled={loading}
          >
            {loading ? 'Criando...' : 'Cadastrar'}
          </button>
        </form>

        <p className="text-center text-secondary small">
          Já tem conta? <Link to="/login" className="text-primary text-decoration-none">Faça Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Cadastro;
