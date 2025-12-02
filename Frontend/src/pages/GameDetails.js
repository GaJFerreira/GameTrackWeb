import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { FaStar, FaSave, FaArrowLeft } from 'react-icons/fa';
import { Link } from 'react-router-dom';

const GameDetails = () => {
  const { id } = useParams(); // Pega o ID da URL (ex: /jogo/1)

  // Simulação de dados do jogo (viria do Backend)
  const gameData = {
    id: id,
    title: 'Cyberpunk 2077',
    description: 'Cyberpunk 2077 é uma história de ação e aventura de mundo aberto ambientada em Night City, uma megalópole obcecada por poder, glamour e modificação corporal. Você joga como V, um mercenário fora da lei atrás de um implante único que carrega a chave para a imortalidade.',
    genre: 'RPG / Ação',
    releaseDate: '2020',
    developer: 'CD Projekt Red',
    image: 'https://images.unsplash.com/photo-1533230408703-912440333d64?auto=format&fit=crop&w=800',
    globalRating: 4.5
  };

  // Estado para as informações do usuário (Editáveis)
  const [userRating, setUserRating] = useState(0);
  const [status, setStatus] = useState('wishlist');
  const [notes, setNotes] = useState('');

  const handleSave = (e) => {
    e.preventDefault();
    alert('Informações salvas com sucesso! (Simulação)');
  };

  return (
    <div className="container py-5">
      <Link to="/" className="btn btn-outline-secondary mb-4">
        <FaArrowLeft className="me-2" /> Voltar
      </Link>

      <div className="row">
        {/* Coluna da Esquerda: Capa e Informações Fixas */}
        <div className="col-md-4 mb-4">
          <div className="card bg-dark border-0 shadow-lg rounded-4 overflow-hidden">
            <img src={gameData.image} alt={gameData.title} className="img-fluid" />
            <div className="card-body">
              <h5 className="text-white fw-bold mb-3">Informações</h5>
              <p className="text-secondary mb-1">Desenvolvedora: <span className="text-white">{gameData.developer}</span></p>
              <p className="text-secondary mb-1">Lançamento: <span className="text-white">{gameData.releaseDate}</span></p>
              <p className="text-secondary mb-0">Gênero: <span className="text-white">{gameData.genre}</span></p>
            </div>
          </div>
        </div>

        {/* Coluna da Direita: Detalhes e Edição do Usuário */}
        <div className="col-md-8">
          <h1 className="display-4 fw-bold text-white mb-2">{gameData.title}</h1>
          <div className="d-flex align-items-center mb-4">
            <span className="badge bg-primary me-2">{gameData.genre}</span>
            <span className="text-warning fw-bold"><FaStar /> {gameData.globalRating} Global</span>
          </div>

          <p className="text-secondary lead mb-5">{gameData.description}</p>

          <hr className="border-secondary my-5" />

          {/* Área de Edição do Usuário */}
          <div className="bg-dark p-4 rounded-4 border border-secondary border-opacity-25">
            <h4 className="text-white fw-bold mb-4">Sua Atividade</h4>
            
            <form onSubmit={handleSave}>
              <div className="row g-3">
                {/* Status */}
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

                {/* Nota Pessoal */}
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

                {/* Notas/Review */}
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