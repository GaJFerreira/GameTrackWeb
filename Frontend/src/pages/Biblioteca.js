import React, { useState, useEffect } from 'react';
import { FaSync } from 'react-icons/fa';
import GameCard from '../components/GameCard';
import api from '../services/api';
import { toast } from 'react-toastify'

const Biblioteca = () => {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState(null);
  const [syncing, setSyncing] = useState(false);
  
  const getGameImage = (game) => {
    if (!game.appid) {
      return "https://via.placeholder.com/400x220?text=Sem+Imagem";
    }
    
    return `https://cdn.akamai.steamstatic.com/steam/apps/${game.appid}/capsule_616x353.jpg`;
  };

  const fetchData = async () => {
    try {
      const authResponse = await api.get('/auth/me');
      const firebaseUid = authResponse.data.user.uid;

      const userResponse = await api.get(`/users/${firebaseUid}`);
      setUserData(userResponse.data);

      const gamesResponse = await api.get(`/games/${firebaseUid}`);
      setGames(gamesResponse.data);

    } catch (error) {
      console.error("Erro ao carregar:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSync = async () => {
    if (!userData) return;
    setSyncing(true);

    try {
      await api.post(`/steam/sync/${userData.id}/${userData.steam_id}`);
      toast("Iniciando sincronização. Pode levar algum tempo atualizar sua biblioteca.");
      
      const gamesResponse = await api.get(`/games/${userData.id}`);
      setGames(gamesResponse.data);

    } catch (error) {
      console.error("Erro no sync:", error);
      toast.error("Erro ao sincronizar. Tente novamente.");
    } finally {
      setSyncing(false);
    }
  };

  if (loading) return <div className="text-white text-center mt-5">Carregando...</div>;

  return (
    <div className="container py-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="text-white fw-bold m-0">Minha Biblioteca</h2>
        <button 
          className="btn btn-outline-primary d-flex align-items-center gap-2"
          onClick={handleSync}
          disabled={syncing || !userData}
        >
          {syncing ? <span className="spinner-border spinner-border-sm"></span> : <FaSync />}
          {syncing ? ' Sincronizando...' : ' Sincronizar Steam'}
        </button>
      </div>

      {games.length === 0 ? (
        <div className="text-center text-secondary mt-5">
          <p>Nenhum jogo encontrado.</p>
          <p>Clique no botão acima para importar da Steam.</p>
        </div>
      ) : (
        <div className="row g-4">
          {games.map((game) => (
            <div key={game.appid} className="col-6 col-md-3">
              <GameCard 
                id={game.appid}
                title={game.name} 
                genre={game.genero || "Gênero não definido"} 
                rating={game.nota_pessoal || 0} 
                hours={game.horas_jogadas || 0} 
                image={getGameImage(game)}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Biblioteca;