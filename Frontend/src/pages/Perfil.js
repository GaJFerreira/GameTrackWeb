import React, { useState, useEffect } from 'react';
import { FaSteam, FaEdit, FaGamepad, FaTrophy, FaClock, FaBan, FaPlayCircle, FaPauseCircle } from 'react-icons/fa';
import api from '../services/api';

const Perfil = ({ onLogout }) => {
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  
  // Estado inicial das estatísticas zerado
  const [stats, setStats] = useState({
    total: 0,
    playing: 0,
    finished: 0,
    notStarted: 0,
    started: 0, // Iniciados + Pausados
    abandoned: 0
  });

  useEffect(() => {
    const loadProfileData = async () => {
      try {
        setLoading(true);
        
        // 1. Pega o ID do usuário logado
        const authResponse = await api.get('/auth/me');
        const firebaseUid = authResponse.data.user.uid;

        // 2. Busca dados cadastrais (Avatar, SteamID, etc.)
        const userResponse = await api.get(`/users/${firebaseUid}`);
        setProfile(userResponse.data);

        // 3. Busca a biblioteca para calcular estatísticas
        const gamesResponse = await api.get(`/games/${firebaseUid}`);
        calculateStats(gamesResponse.data);

      } catch (error) {
        console.error("Erro ao carregar perfil:", error);
      } finally {
        setLoading(false);
      }
    };

    loadProfileData();
  }, []);

  // Lógica para processar os jogos e gerar os números do dashboard
  const calculateStats = (games) => {
    const newStats = {
      total: games.length,
      playing: 0,
      finished: 0,
      notStarted: 0,
      started: 0,
      abandoned: 0
    };

    games.forEach(game => {
      const status = game.status; // Vem do Backend: "Jogando", "Finalizado", etc.

      if (status === "Jogando") newStats.playing++;
      else if (status === "Finalizado") newStats.finished++;
      else if (status === "Não Iniciado") newStats.notStarted++;
      else if (status === "Abandonado") newStats.abandoned++;
      else if (status === "Iniciado" || status === "Pausado") newStats.started++;
    });

    setStats(newStats);
  };

  if (loading) return <div className="text-white text-center mt-5">Carregando perfil...</div>;
  if (!profile) return <div className="text-white text-center mt-5">Erro ao carregar perfil.</div>;

  return (
    <div className="container py-5">
      <div className="row">
        
        {/* COLUNA DA ESQUERDA: Informações Pessoais */}
        <div className="col-lg-4 mb-4">
          <div className="card bg-dark text-white border-secondary border-opacity-25 shadow-lg rounded-4 p-4 text-center h-100">
            <div className="position-relative d-inline-block mx-auto mb-3">
              <img 
                src={profile.avatar || "https://via.placeholder.com/150"} 
                alt="Avatar" 
                className="rounded-circle border border-4 border-danger"
                style={{ width: '150px', height: '150px', objectFit: 'cover' }}
              />
              {/* Botão decorativo por enquanto */}
              <button className="btn btn-sm btn-primary position-absolute bottom-0 end-0 rounded-circle p-2" title="Editar Avatar">
                <FaEdit />
              </button>
            </div>
            
            {/* Usa o personaname (Nick da Steam) ou o nome real se disponível */}
            <h3 className="fw-bold mb-0">{profile.personaname || "Usuário"}</h3>
            <p className="text-secondary mb-3">{profile.realname || "Gamer"}</p>
            
            <div className="text-start bg-black bg-opacity-25 p-3 rounded-3 mb-3">
              <p className="mb-1 small text-secondary">Email:</p>
              <p className="mb-3 text-white fw-bold text-truncate" title={profile.email}>{profile.email}</p>
              
              <p className="mb-1 small text-secondary">Steam ID:</p>
              <p className="mb-0 text-white font-monospace small">{profile.steam_id}</p>
            </div>

            {profile.profileurl && (
              <a href={profile.profileurl} target="_blank" rel="noreferrer" className="btn btn-outline-secondary w-100 d-flex align-items-center justify-content-center gap-2 mb-3">
                <FaSteam size={20} /> Perfil Steam
              </a>
            )}

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
                   <h2 className="display-4 fw-bold mb-0">{stats.total}</h2>
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
                  <h3 className="fw-bold m-0 text-white">{stats.playing}</h3>
                  <small className="text-secondary text-uppercase fw-bold" style={{fontSize: '0.7rem'}}>Jogando Agora</small>
               </div>
            </div>

            {/* Finalizados */}
            <div className="col-md-4">
               <div className="p-3 rounded-4 bg-dark border border-success border-opacity-25 text-center h-100">
                  <FaTrophy className="text-success h2 mb-2" />
                  <h3 className="fw-bold m-0 text-white">{stats.finished}</h3>
                  <small className="text-secondary text-uppercase fw-bold" style={{fontSize: '0.7rem'}}>Finalizados</small>
               </div>
            </div>

            {/* Não Iniciados */}
            <div className="col-md-4">
               <div className="p-3 rounded-4 bg-dark border border-secondary border-opacity-25 text-center h-100">
                  <FaClock className="text-secondary h2 mb-2" />
                  <h3 className="fw-bold m-0 text-white">{stats.notStarted}</h3>
                  <small className="text-secondary text-uppercase fw-bold" style={{fontSize: '0.7rem'}}>Backlog (Não Iniciado)</small>
               </div>
            </div>

            {/* Iniciados (Agrupa Iniciado + Pausado) */}
            <div className="col-md-6">
               <div className="p-3 rounded-4 bg-dark border border-warning border-opacity-25 d-flex align-items-center justify-content-between">
                  <div className="text-start">
                    <h4 className="fw-bold m-0 text-white">{stats.started}</h4>
                    <small className="text-secondary">Iniciados / Pausados</small>
                  </div>
                  <FaPauseCircle className="text-warning h4 mb-0" />
               </div>
            </div>

            {/* Abandonados */}
            <div className="col-md-6">
               <div className="p-3 rounded-4 bg-dark border border-danger border-opacity-25 d-flex align-items-center justify-content-between">
                  <div className="text-start">
                    <h4 className="fw-bold m-0 text-white">{stats.abandoned}</h4>
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