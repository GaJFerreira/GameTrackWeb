import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api'; // Importamos nossa configuração do Axios

const Login = ({ onLogin }) => {
  const navigate = useNavigate();
  
  // 1. Estados para armazenar os inputs e feedback visual
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');       // Limpa erros anteriores
    setLoading(true);   // Ativa o spinner

    try {
      // 2. Chamada real ao Backend
      const response = await api.post('/auth/login', {
        email: email,
        password: password
      });

      // 3. Sucesso: Pegamos os tokens
      const { id_token, refresh_token } = response.data;

      // 4. Salvamos no armazenamento do navegador (para persistir o login)
      localStorage.setItem('token', id_token);
      localStorage.setItem('refreshToken', refresh_token);

      // 5. Atualiza o estado global do App e redireciona
      onLogin(); 
      navigate('/biblioteca'); // Redirecionar para biblioteca faz mais sentido após login

    } catch (err) {
      console.error(err);
      // Tratamento de erro robusto
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail); // Mensagem exata do backend (ex: "INVALID_PASSWORD")
      } else {
        setError("Falha ao fazer login. Verifique suas credenciais.");
      }
    } finally {
      setLoading(false); // Desativa o spinner independente do resultado
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
      <div className="card bg-dark text-white p-5 rounded-4 shadow-lg border border-secondary border-opacity-25" style={{ maxWidth: '450px', width: '100%' }}>
        <h2 className="fw-bold mb-2 text-center">Bem-vindo de volta</h2>
        <p className="text-secondary text-center mb-4">Acesse sua biblioteca de jogos</p>
        
        {/* Exibe mensagem de erro se houver */}
        {error && <div className="alert alert-danger py-2 small text-center">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label text-secondary small">Email</label>
            <input 
              type="email" 
              required 
              className="form-control form-control-dark" 
              placeholder="seu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="mb-4">
            <label className="form-label text-secondary small">Senha</label>
            <input 
              type="password" 
              required 
              className="form-control form-control-dark" 
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          
          <button 
            type="submit" 
            className="btn btn-brand-red w-100 py-2 fw-bold mb-3"
            disabled={loading} // Desabilita botão durante o carregamento
          >
            {loading ? (
              <span><span className="spinner-border spinner-border-sm me-2"></span>Entrando...</span>
            ) : (
              'Entrar'
            )}
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