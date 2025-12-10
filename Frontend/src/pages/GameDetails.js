import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { FaStar, FaSave, FaArrowLeft, FaClock, FaTrophy, FaWindows, FaGlobe, FaTag, FaInfoCircle } from 'react-icons/fa';
import api from '../services/api';
import { toast } from 'react-toastify'; // Recomendo usar o toast para feedback visual

const GameDetails = () => {
  const { id } = useParams(); // 'id' aqui é o AppID da Steam (ex: 730)
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [gameData, setGameData] = useState(null);
  const [userData, setUserData] = useState(null);

  // Estados para edição
  const [status, setStatus] = useState('');
  const [userRating, setUserRating] = useState(0);
  const [interest, setInterest] = useState('');

  useEffect(() => {
    const fetchGameDetails = async () => {
      try {
        setLoading(true);
        const authResponse = await api.get('/auth/me');
        const user = authResponse.data.user;
        setUserData(user);

        // --- OTIMIZAÇÃO AQUI ---
        // Em vez de baixar tudo, buscamos apenas ESTE jogo específico
        // Rota: /games/{user_id}/{game_id}
        const response = await api.get(`/games/${user.uid}/${id}`);
        const foundGame = response.data;

        if (foundGame) {
          setGameData(foundGame);
          
          // Preenche os campos com o que veio do banco
          setStatus(foundGame.status || 'Não Iniciado');
          setUserRating(foundGame.nota_pessoal || 0);
          setInterest(foundGame.interesse || 'N/A');
        }

      } catch (error) {
        console.error("Erro ao carregar detalhes:", error);
        
        // Se der erro 404, significa que o jogo não está na biblioteca
        if (error.response && error.response.status === 404) {
             toast.error("Jogo não encontrado na sua biblioteca!");
             navigate('/biblioteca');
        } else {
             toast.error("Erro de conexão ao buscar jogo.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchGameDetails();
  }, [id, navigate]);

  const getGameImage = (game) => {
    if (!game?.appid) return "https://via.placeholder.com/800x450?text=Carregando...";
    return `https://cdn.akamai.steamstatic.com/steam/apps/${game.appid}/header.jpg`;
  };

  const formatPrice = (priceObj) => {
    if (!priceObj || !priceObj.preco_final) return "Grátis / Não disponível";
    // O preço geralmente vem em centavos da Steam (ex: 19990 = R$ 199,90)
    return (priceObj.preco_final / 100).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  };

  const handleSave = async (e) => {
    e.preventDefault();
    if (!userData || !gameData) return;

    const payload = {
      status: status,
      nota_pessoal: parseInt(userRating),
      interesse: interest
    };

    try {
      // Rota PUT: /games/{user_id}/{game_id}
      await api.put(`/games/${userData.uid}/${gameData.appid}`, payload);
      
      toast.success('Informações atualizadas com sucesso!');
      
      // Atualiza o estado local para refletir na hora sem recarregar
      setGameData({ ...gameData, ...payload });
      
    } catch (error) {
      console.error("Erro ao salvar:", error);
      toast.error("Falha ao salvar alterações.");
    }
  };

  if (loading) return <div className="text-white text-center mt-5">Carregando detalhes...</div>;
  if (!gameData) return <div className="text-white text-center mt-5">Jogo não encontrado.</div>;

  return (
    <div className="container py-5">
      <Link to="/biblioteca" className="btn btn-outline-light mb-4 border-opacity-25 text-white-50">
        <FaArrowLeft className="me-2" /> Voltar para Biblioteca
      </Link>

      <div className="row g-5">
        
        {/* === COLUNA DA ESQUERDA (Lateral) === */}
        <div className="col-lg-4">
          
          {/* 1. Capa e Stats */}
          <div className="card bg-dark border-0 shadow-lg rounded-4 overflow-hidden mb-4">
            <img 
              src={getGameImage(gameData)} 
              alt={gameData.name} 
              className="img-fluid"
              style={{ objectFit: 'cover' }}
            />
            <div className="card-footer bg-black bg-opacity-50 border-top border-secondary border-opacity-25 py-3">
              <div className="d-flex justify-content-around text-white">
                <div className="text-center">
                  <FaClock className="text-primary mb-1 h5" />
                  <div className="small fw-bold">{gameData.horas_jogadas ? Math.round(gameData.horas_jogadas / 60) : 0}h</div>
                  <div className="text-white-50" style={{fontSize: '0.7rem'}}>JOGADAS</div>
                </div>
                <div className="text-center">
                  <FaTrophy className="text-warning mb-1 h5" />
                  <div className="small fw-bold">{gameData.conquistas_obtidas || 0} / {gameData.conquistas_totais || '?'}</div>
                  <div className="text-white-50" style={{fontSize: '0.7rem'}}>CONQUISTAS</div>
                </div>
              </div>
            </div>
          </div>

          {/* 2. Card de Preço (Se existir) */}
          <div className="card bg-dark border border-secondary border-opacity-25 rounded-4 p-3 mb-4">
              <div className="d-flex align-items-center justify-content-between">
                <span className="text-white-50 small"><FaTag className="me-2"/>Preço Atual:</span>
                <div>
                  {gameData.preco && gameData.preco.desconto_percentual > 0 && (
                    <span className="badge bg-success me-2">-{gameData.preco.desconto_percentual}%</span>
                  )}
                  <span className="fw-bold text-white">{formatPrice(gameData.preco)}</span>
                </div>
              </div>
          </div>

          {/* 3. Card de Informações */}
          <div className="card bg-dark border border-secondary border-opacity-25 rounded-4 p-4 mb-4">
            <h5 className="text-white fw-bold mb-3 d-flex align-items-center">
              <FaInfoCircle className="text-primary me-2" size={18} /> Detalhes
            </h5>
            <ul className="list-unstyled mb-0">
              <li className="mb-3">
                <span className="d-block text-white-50 small mb-1">Desenvolvedor</span>
                <span className="text-white fw-medium">{gameData.desenvolvedor || 'N/A'}</span>
              </li>
              <li className="mb-3">
                <span className="d-block text-white-50 small mb-1">Publisher</span>
                <span className="text-white fw-medium">{gameData.publisher || 'N/A'}</span>
              </li>
              <li className="mb-3">
                <span className="d-block text-white-50 small mb-1">Lançamento</span>
                <span className="text-white fw-medium">{gameData.data_lancamento || 'N/A'}</span>
              </li>
              <li>
                <span className="d-block text-white-50 small mb-1">Gênero Principal</span>
                <span className="text-white fw-medium">{gameData.genero ? gameData.genero.split(',')[0] : 'N/A'}</span>
              </li>
            </ul>
          </div>

          {/* 4. Card Gerenciar Progresso */}
          <div className="card bg-black bg-opacity-50 border border-primary border-opacity-50 rounded-4 p-4 shadow">
            <h5 className="text-white fw-bold mb-4 d-flex align-items-center">
              <FaSave className="text-primary me-2" /> Meu Progresso
            </h5>
            
            <form onSubmit={handleSave}>
              <div className="row g-3">
                {/* Status */}
                <div className="col-12">
                  <label className="form-label text-white-50 small text-uppercase fw-bold">Status</label>
                  <select 
                    className="form-select form-control-dark text-white bg-dark border-secondary" 
                    value={status} 
                    onChange={(e) => setStatus(e.target.value)}
                  >
                    <option value="wishlist">Quero Jogar</option>
                    <option value="Jogando">Jogando</option>
                    <option value="Finalizado">Finalizado</option>
                    <option value="Abandonado">Abandonado</option>
                    <option value="Pausado">Pausado</option>
                  </select>
                </div>

                {/* Nota */}
                <div className="col-12">
                  <label className="form-label text-white-50 small text-uppercase fw-bold">Nota Pessoal</label>
                  <div className="input-group">
                    <span className="input-group-text bg-dark border-secondary text-warning"><FaStar /></span>
                    <input 
                      type="number" 
                      className="form-control form-control-dark text-white bg-dark border-secondary" 
                      min="0" max="10" 
                      value={userRating}
                      onChange={(e) => setUserRating(e.target.value)}
                    />
                  </div>
                </div>

                {/* Interesse */}
                <div className="col-12">
                  <label className="form-label text-white-50 small text-uppercase fw-bold">Interesse</label>
                  <select 
                    className="form-select form-control-dark text-white bg-dark border-secondary" 
                    value={interest} 
                    onChange={(e) => setInterest(e.target.value)}
                  >
                    <option value="N/A">N/A</option>
                    <option value="Baixo">Baixo</option>
                    <option value="Médio">Médio</option>
                    <option value="Alto">Alto</option>
                  </select>
                </div>

                <div className="col-12 mt-4">
                  <button type="submit" className="btn btn-brand-red w-100 fw-bold">
                    Salvar Alterações
                  </button>
                </div>
              </div>
            </form>
          </div>

        </div>

        {/* === COLUNA DA DIREITA (Conteúdo Principal) === */}
        <div className="col-lg-8">
          
          {/* Cabeçalho */}
          <div className="mb-4">
            <h1 className="display-4 fw-bold text-white mb-3">{gameData.name}</h1>
            <div className="d-flex flex-wrap gap-2 align-items-center mb-4">
              {gameData.genero && gameData.genero.split(', ').map((gen, idx) => (
                <span key={idx} className="badge bg-secondary bg-opacity-25 border border-secondary border-opacity-25 text-white">
                  {gen}
                </span>
              ))}
              {gameData.metacritic && (
                 <span className="badge border border-warning text-warning">
                   Metacritic: {gameData.metacritic}
                 </span>
              )}
            </div>

            {/* Descrição - HTML Seguro */}
            <div className="p-4 rounded-4 bg-dark bg-opacity-50 border border-secondary border-opacity-10">
               <h4 className="text-white fw-bold mb-3">Sobre o Jogo</h4>
               <div className="text-light" style={{ fontSize: '1.05rem', lineHeight: '1.7', opacity: '0.9' }}>
                  {/* Verifica qual campo de descrição existe */}
                  {gameData.short_description || gameData.descricao || gameData.descricao_completa ? (
                    <div dangerouslySetInnerHTML={{ __html: gameData.descricao_completa || gameData.short_description || gameData.descricao }} />
                  ) : (
                    "Sem descrição disponível."
                  )}
               </div>
            </div>
          </div>

          {/* Seção de Requisitos e Idiomas */}
          <div className="card bg-dark border-0 rounded-4 p-4 shadow-sm mt-5">
            <h4 className="text-white fw-bold mb-4 border-bottom border-secondary border-opacity-25 pb-3">
              Especificações Técnicas
            </h4>
            
            <div className="row g-4">
              {/* Requisitos */}
              <div className="col-lg-7">
                <h6 className="text-primary fw-bold mb-3 d-flex align-items-center">
                  <FaWindows className="me-2" /> Requisitos de Sistema (PC)
                </h6>
                <div className="bg-black bg-opacity-25 p-3 rounded-3 text-light small font-monospace" style={{ opacity: 0.85 }}>
                  
                  {/* Verifica se tem requisitos MÍNIMOS */}
                  {gameData.requisitos_minimos ? (
                    <div className="mb-3">
                        <div dangerouslySetInnerHTML={{ __html: gameData.requisitos_minimos }} />
                    </div>
                  ) : (
                    <p className="mb-2">Requisitos mínimos não informados.</p>
                  )}

                  {/* Verifica se tem requisitos RECOMENDADOS (opcional, mas legal mostrar) */}
                  {gameData.requisitos_recomendados && (
                    <div className="mt-3 pt-3 border-top border-secondary border-opacity-25">
                        <div dangerouslySetInnerHTML={{ __html: gameData.requisitos_recomendados }} />
                    </div>
                  )}

                  {/* Caso não tenha nada */}
                  {!gameData.requisitos_minimos && !gameData.requisitos_recomendados && (
                    "Detalhes técnicos indisponíveis."
                  )}

                </div>
              </div>

              {/* Idiomas */}
              <div className="col-lg-5">
                <h6 className="text-primary fw-bold mb-3 d-flex align-items-center">
                  <FaGlobe className="me-2" /> Idiomas Suportados
                </h6>
                <div className="text-light small" style={{ lineHeight: '1.6', opacity: 0.85 }}>
                  {gameData.linguas ? (
                    <div dangerouslySetInnerHTML={{ __html: gameData.linguas }} />
                  ) : (
                    "Não informado."
                  )}
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default GameDetails;
