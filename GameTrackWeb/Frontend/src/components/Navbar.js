import React from 'react';
import { Link } from 'react-router-dom';
import { FaGamepad, FaSearch, FaUser } from 'react-icons/fa';

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark py-3" style={{ backgroundColor: '#050505', borderBottom: '1px solid #222' }}>
      <div className="container">
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
          </ul>

          <div className="d-flex align-items-center gap-3">
            <div className="d-none d-lg-flex input-group">
              <span className="input-group-text bg-dark border-secondary text-secondary"><FaSearch /></span>
              <input type="text" className="form-control bg-dark border-secondary text-white shadow-none" placeholder="Buscar..." />
            </div>
            <Link to="/login" className="btn btn-brand-red px-4 d-flex align-items-center gap-2">
              <FaUser size={14} /> Entrar
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;