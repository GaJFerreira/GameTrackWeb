import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import GameCard from '../components/GameCard';
import api from '../services/api';
import { FaRobot, FaChartLine, FaExclamationTriangle, FaSync } from 'react-icons/fa';

const Recomendacoes = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [warnings, setWarnings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        setLoading(true);
        // 1. Pega ID do usuário
        const authResponse = await api.get('/auth/me');
        const firebaseUid = authResponse.data.user.uid;

        // 2. Busca recomendações da IA
        const response = await api.get(`/recommendations/${firebaseUid}`);
        
        setRecommendations(response.data.recommendations || []);
        setWarnings(response.data.warnings || []);

      } catch (err) {
        console.error("Erro ao buscar recomendações:", err);
        // Tratamento para quando a IA não tem dados suficientes (404 ou 400)
        if (err.response && (err.response.status === 404 || err.response.status === 400)) {
          setError(err.response.data.detail);
        } else {
          setError("Falha ao conectar com o serviço de IA.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, []);

  // Helper para cor da probabilidade
  const getMatchColor = (score) => {
    if (score >= 80) return '#10b981'; // Verde
    if (score >= 50) return '#f59e0b'; // Amarelo
    return '#ef4444'; // Vermelho
  };

  // Helper para imagem (mesma lógica da Biblioteca para garantir qualidade)
  const getGameImage = (appid) => {
    return `https://cdn.akamai.steamstatic.com/steam/apps/${appid}/header.jpg`;
  };

  if (loading) {
    return (
      <div className="container py-5 text-center">
        <div className="spinner-border text-primary mb-3" role="status"></div>
        <h4 className="text-white">Analisando seu perfil de jogador...</h4>
        <p className="text-secondary">Nossa IA está calculando as melhores sugestões para você.</p>
      </div>
    );
  }

  return (
    <div className="container py-5">
      
      {/* Cabeçalho da IA */}
      <div className="d-flex align-items-center mb-5 p-4 rounded-4 bg-dark border border-primary border-opacity-25 shadow-lg">
        <div className="bg-primary bg-opacity-10 p-3 rounded-circle me-3">
          <FaRobot size={32} className="text-primary" />
        </div>
        <div>
          <h2 className="text-white fw-bold mb-1">Análise de Compatibilidade IA</h2>
          <p className="text-secondary mb-0">
            Algoritmo baseado em <strong>Random Forest</strong> analisando seus jogos.
            Para que o Algoritmo faça recomendacoes melhores ẽ importante que vocẽ jogue e avalie mais titulos na sua biblioteca.
          </p>
        </div>
      </div>

      {/* Exibição de Avisos da IA (se houver) */}
      {warnings.length > 0 && (
        <div className="alert alert-warning border-0 rounded-4 mb-5 d-flex align-items-center">
          <FaExclamationTriangle className="me-3 fs-4" />
          <div>
            <h6 className="fw-bold mb-1">Dica para melhorar as recomendações:</h6>
            <ul className="mb-0 small ps-3">
              {warnings.map((warn, idx) => (
                <li key={idx}>{warn}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Estado de Erro / Sem Dados */}
      {error ? (
        <div className="text-center py-5 rounded-4 bg-dark border border-secondary border-opacity-25">
          <FaChartLine size={48} className="text-secondary mb-3 opacity-50" />
          <h3 className="text-white fw-bold">Não foi possível gerar recomendações</h3>
          <p className="text-danger mb-4">{error}</p>
          <Link to="/biblioteca" className="btn btn-outline-light">
            <FaSync className="me-2" /> Ir para Biblioteca e Jogar/Avaliar
          </Link>
        </div>
      ) : (
        /* Lista de Recomendações */
        <div className="row g-4">
          {recommendations.map(game => (
            <div key={game.appid} className="col-md-3">
              
              {/* Card do Jogo */}
              <GameCard 
                id={game.appid}
                title={game.name}
                genre={game.genero ? game.genero.split(',')[0] : 'Gênero n/a'}
                // IA não retorna nota/horas do jogo recomendado, passamos 0 ou omitimos
                rating={0} 
                hours={0} 
                image={getGameImage(game.appid)}
                tag={`${game.probabilidade_finalizar}% Chance`}
                tagColor={getMatchColor(game.probabilidade_finalizar)}
              />

              {/* Barra de Probabilidade (Abaixo do Card) */}
              <div className="mt-3 px-2">
                <div className="d-flex justify-content-between align-items-center mb-1">
                  <small className="text-secondary fw-bold" style={{fontSize: '0.7rem'}}>PROBABILIDADE DE FINALIZAR</small>
                  <small className="fw-bold" style={{color: getMatchColor(game.probabilidade_finalizar)}}>
                    {game.probabilidade_finalizar}%
                  </small>
                </div>
                
                <div className="progress bg-dark border border-secondary border-opacity-25" style={{ height: '6px' }}>
                  <div 
                    className="progress-bar" 
                    role="progressbar" 
                    style={{ 
                      width: `${game.probabilidade_finalizar}%`, 
                      backgroundColor: getMatchColor(game.probabilidade_finalizar),
                      borderRadius: '10px'
                    }} 
                  ></div>
                </div>
              </div>

            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Recomendacoes;