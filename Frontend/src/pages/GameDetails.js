import React, { useState, useEffect } from 'react'; // Adicionado useEffect
import { useParams, Link } from 'react-router-dom';
import { FaStar, FaSave, FaArrowLeft } from 'react-icons/fa';
import { toast } from 'react-toastify';
import api from '../services/api'; // Importando a API

const GameDetails = () => {
  const { id } = useParams();

  const [gameData, setGameData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [userRating, setUserRating] = useState(0);
  const [status, setStatus] = useState('wishlist');
  const [notes, setNotes] = useState('');

  useEffect(() => {
    const fetchGameDetails = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/games/details/${id}`); 
        
        setGameData(response.data);

      } catch (error) {
        console.error("Erro ao buscar detalhes:", error);
        toast.error("Erro ao carregar informações do jogo.");
      } finally {
        setLoading(false);
      }
    };

    fetchGameDetails();
  }, [id]);

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      await api.post(`/games/${id}/interaction`, {
        status,
        rating: userRating,
        notes
      });
      toast.success('Informações salvas com sucesso!');
    } catch (error) {
      toast.error('Erro ao salvar alterações.');
    }
  };

  if (loading) return <div className="text-white text-center mt-5">Carregando...</div>;
  if (!gameData) return <div className="text-white text-center mt-5">Jogo não encontrado.</div>;

  return (
    <div className="container py-5">
      <Link to="/biblioteca" className="btn btn-outline-secondary mb-4">
        <FaArrowLeft className="me-2" /> Voltar
      </Link>

      <div className="row">
        {/* Coluna da Esquerda */}
        <div className="col-md-4 mb-4">
          <div className="card bg-dark border-0 shadow-lg rounded-4 overflow-hidden">
            <img 
               src={gameData.image || "https://via.placeholder.com/400x600"} 
               alt={gameData.title} 
               className="img-fluid" 
            />
            <div className="card-body">
              <h5 className="text-white fw-bold mb-3">Informações</h5>
              <p className="text-secondary mb-1">Desenvolvedora: <span className="text-white">{gameData.developer || "N/A"}</span></p>
              <p className="text-secondary mb-1">Lançamento: <span className="text-white">{gameData.releaseDate || "N/A"}</span></p>
              <p className="text-secondary mb-0">Gênero: <span className="text-white">{gameData.genre || "N/A"}</span></p>
            </div>
          </div>
        </div>

        {/* Coluna da Direita (Mantendo o layout do seu colega) */}
        <div className="col-md-8">
          <h1 className="display-4 fw-bold text-white mb-2">{gameData.title}</h1>
          <div className="d-flex align-items-center mb-4">
            <span className="badge bg-primary me-2">{gameData.genre}</span>
            <span className="text-warning fw-bold"><FaStar /> {gameData.globalRating || "S/N"} Global</span>
          </div>

          <p className="text-secondary lead mb-5">{gameData.description || "Sem descrição disponível."}</p>

          <hr className="border-secondary my-5" />

          {/* Área de Edição */}
          <div className="bg-dark p-4 rounded-4 border border-secondary border-opacity-25">
            <h4 className="text-white fw-bold mb-4">Sua Atividade</h4>
            
            <form onSubmit={handleSave}>
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="form-label text-secondary">Status</label>
                  <select 
                    className="form-select form-control-dark" 
                    value={status} 
                    onChange={(e) => setStatus(e.target.value)}
                  >
                    <option value="wishlist">Quero Jogar</option>
                    <option value="playing">Jogando</option>
                    <option value="completed">Zerado / Completado</option>
                    <option value="dropped">Abandonado</option>
                  </select>
                </div>

                <div className="col-md-6">
                  <label className="form-label text-secondary">Sua Nota (0 a 10)</label>
                  <input 
                    type="number" 
                    className="form-control form-control-dark" 
                    min="0" max="10" 
                    value={userRating}
                    onChange={(e) => setUserRating(e.target.value)}
                  />
                </div>

                <div className="col-12">
                  <label className="form-label text-secondary">Anotações Pessoais</label>
                  <textarea 
                    className="form-control form-control-dark" 
                    rows="3" 
                    placeholder="O que você está achando do jogo?"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                  ></textarea>
                </div>

                <div className="col-12">
                  <button type="submit" className="btn btn-brand-red px-4 d-flex align-items-center gap-2">
                    <FaSave /> Salvar Alterações
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GameDetails;