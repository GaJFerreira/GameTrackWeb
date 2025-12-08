import React from 'react';
import { Link } from 'react-router-dom';
import { FaGamepad, FaUser } from 'react-icons/fa'; // Removi FaSearch da importação

const Navbar = ({ isLoggedIn }) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark py-3" style={{ backgroundColor: '#050505', borderBottom: '1px solid #222' }}>
      <div className="container">
        {/* 1. MUDANÇA DE NOME AQUI */}
        <Link className="navbar-brand d-flex align-items-center fw-bold fs-4" to="/">
          <FaGamepad className="text-danger me-2" size={28} />
          GameTrack
        </Link>

        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav mx-auto">
            <li className="nav-item"><Link className="nav-link text-white mx-2" to="/">Explorar</Link></li>
            <li className="nav-item"><Link className="nav-link text-secondary mx-2" to="/recomendacoes">Recomendações</Link></li>
            <li className="nav-item"><Link className="nav-link text-secondary mx-2" to="/biblioteca">Biblioteca</Link></li>
            <li className="nav-item"><Link className="nav-link text-secondary mx-2" to="/metas">Metas</Link></li>
          </ul>

          <div className="d-flex align-items-center gap-3">
            
            {/* 2. BARRA DE PESQUISA REMOVIDA DAQUI */}
            
            {/* LÓGICA DO BOTÃO DE LOGIN/PERFIL */}
            {isLoggedIn ? (
              <Link 
                to="/perfil" 
                className="btn btn-outline-secondary d-flex align-items-center gap-2 border-opacity-25 text-white px-3 py-2"
                style={{ borderColor: '#444' }}
              >
                <div 
                  className="bg-danger rounded-circle d-flex align-items-center justify-content-center text-white" 
                  style={{width: '24px', height: '24px', fontSize: '10px'}}
                >
                  <FaUser />
                </div>
                <span className="d-none d-md-block small fw-bold text-nowrap">Minha Conta</span>
              </Link>
            ) : (
              <Link to="/login" className="btn btn-brand-red px-4 d-flex align-items-center gap-2">
                <FaUser size={14} /> Entrar
              </Link>
            )}

          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;