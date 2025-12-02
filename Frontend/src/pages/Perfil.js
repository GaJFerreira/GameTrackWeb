import React from 'react';
import { FaSteam, FaEdit, FaGamepad, FaTrophy, FaClock, FaBan, FapauseCircle, FaPlayCircle } from 'react-icons/fa';

const Perfil = ({ onLogout }) => {
  // Dados do Usuário (Simulação)
  const user = {
    nickname: "GamerPro_99",
    realName: "João da Silva",
    email: "joao.gamer@email.com",
    steamId: "76561198000000000",
    steamProfileLink: "https://steamcommunity.com/id/gamerpro99",
    avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200",
  };

  // Simulação da Biblioteca para gerar estatísticas
  const libraryStats = {
    total: 142,
    byStatus: {
      notStarted: 45, // Não iniciado
      started: 12,    // Iniciado
      playing: 4,     // Jogando
      finished: 78,   // Finalizado
      abandoned: 3    // Abandonado
    }
  };

  return (
    <div className="container py-5">
      <div className="row">
        
        {/* COLUNA DA ESQUERDA: Informações Pessoais */}
        <div className="col-lg-4 mb-4">
          <div className="card bg-dark text-white border-secondary border-opacity-25 shadow-lg rounded-4 p-4 text-center h-100">
            <div className="position-relative d-inline-block mx-auto mb-3">
              <img 
                src={user.avatar} 
                alt="Avatar" 
                className="rounded-circle border border-4 border-danger"
                style={{ width: '150px', height: '150px', objectFit: 'cover' }}
              />
              <button className="btn btn-sm btn-primary position-absolute bottom-0 end-0 rounded-circle p-2" title="Editar Avatar">
                <FaEdit />
              </button>
            </div>
            
            <h3 className="fw-bold mb-0">{user.nickname}</h3>
            <p className="text-secondary mb-3">{user.realName}</p>
            
            <div className="text-start bg-black bg-opacity-25 p-3 rounded-3 mb-3">
              <p className="mb-1 small text-secondary">Email:</p>
              <p className="mb-3 text-white fw-bold">{user.email}</p>
              
              <p className="mb-1 small text-secondary">Steam ID:</p>
              <p className="mb-0 text-white font-monospace">{user.steamId}</p>
            </div>

            <a href={user.steamProfileLink} target="_blank" rel="noreferrer" className="btn btn-outline-secondary w-100 d-flex align-items-center justify-content-center gap-2 mb-3">
              <FaSteam size={20} /> Perfil Steam
            </a>

            <button onClick={onLogout} className="btn btn-outline-danger w-100 mt-auto">
              Sair da Conta
            </button>
          </div>
        </div>

        {/* COLUNA DA DIREITA: Estatísticas */}
        <div className="col-lg-8">
          <h2 className="text-white fw-bold mb-4">Estatísticas da Biblioteca</h2>

          {/* Card Total */}
          <div className="card bg-gradient-primary text-white border-0 shadow-sm rounded-4 p-4 mb-4" style={{ background: 'linear-gradient(45deg, #8a0000, #b91c1c)' }}>
             <div className="d-flex justify-content-between align-items-center">
                <div>
                   <h2 className="display-4 fw-bold mb-0">{libraryStats.total}</h2>
                   <p className="mb-0 opacity-75">Total de Jogos na Biblioteca</p>
                </div>
                <FaGamepad size={60} className="opacity-25" />
             </div>
          </div>

          {/* Grid de Status */}
          <div className="row g-3">
            {/* Jogando */}
            <div className="col-md-4">
               <div className="p-3 rounded-4 bg-dark border border-primary border-opacity-50 text-center h-100">
                  <FaPlayCircle className="text-primary h2 mb-2" />
                  <h3 className="fw-bold m-0 text-white">{libraryStats.byStatus.playing}</h3>
                  <small className="text-secondary text-uppercase fw-bold" style={{fontSize: '0.7rem'}}>Jogando Agora</small>
               </div>
            </div>

            {/* Finalizados */}
            <div className="col-md-4">
               <div className="p-3 rounded-4 bg-dark border border-success border-opacity-25 text-center h-100">
                  <FaTrophy className="text-success h2 mb-2" />
                  <h3 className="fw-bold m-0 text-white">{libraryStats.byStatus.finished}</h3>
                  <small className="text-secondary text-uppercase fw-bold" style={{fontSize: '0.7rem'}}>Finalizados</small>
               </div>
            </div>

            {/* Não Iniciados */}
            <div className="col-md-4">
               <div className="p-3 rounded-4 bg-dark border border-secondary border-opacity-25 text-center h-100">
                  <FaClock className="text-secondary h2 mb-2" />
                  <h3 className="fw-bold m-0 text-white">{libraryStats.byStatus.notStarted}</h3>
                  <small className="text-secondary text-uppercase fw-bold" style={{fontSize: '0.7rem'}}>Backlog (Não Iniciado)</small>
               </div>
            </div>

            {/* Iniciados (Mas pausados/sem jogar ativamente) */}
            <div className="col-md-6">
               <div className="p-3 rounded-4 bg-dark border border-warning border-opacity-25 d-flex align-items-center justify-content-between">
                  <div className="text-start">
                    <h4 className="fw-bold m-0 text-white">{libraryStats.byStatus.started}</h4>
                    <small className="text-secondary">Iniciados</small>
                  </div>
                  <FaPlayCircle className="text-warning h4 mb-0" />
               </div>
            </div>

            {/* Abandonados */}
            <div className="col-md-6">
               <div className="p-3 rounded-4 bg-dark border border-danger border-opacity-25 d-flex align-items-center justify-content-between">
                  <div className="text-start">
                    <h4 className="fw-bold m-0 text-white">{libraryStats.byStatus.abandoned}</h4>
                    <small className="text-secondary">Abandonados</small>
                  </div>
                  <FaBan className="text-danger h4 mb-0" />
               </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default Perfil;