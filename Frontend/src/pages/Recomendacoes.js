import React from 'react';
import GameCard from '../components/GameCard';
import { FaRobot, FaChartLine, FaInfoCircle } from 'react-icons/fa';

const Recomendacoes = () => {
  // Simulação dos dados retornados pela sua IA (Python/Backend)
  const aiRecommendations = [
    { 
      id: 101, 
      title: 'Dark Souls III', 
      genre: 'Action RPG', 
      rating: 4.8, 
      hours: 60, 
      image: 'https://images.unsplash.com/photo-1599582200230-03a0d9b4b09b?auto=format&fit=crop&w=600',
      matchScore: 98, // Porcentagem de chance de terminar
      reason: 'Baseado no seu amor por Elden Ring'
    },
    { 
      id: 102, 
      title: 'Hades', 
      genre: 'Roguelike', 
      rating: 4.9, 
      hours: 45, 
      image: 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=600',
      matchScore: 85,
      reason: 'Alta compatibilidade com mecânicas rápidas'
    },
    { 
      id: 103, 
      title: 'Starfield', 
      genre: 'RPG / Espacial', 
      rating: 4.2, 
      hours: 100, 
      image: 'https://images.unsplash.com/photo-1614728853913-1e2221b01a69?auto=format&fit=crop&w=600',
      matchScore: 64,
      reason: 'Você gosta do gênero, mas costuma abandonar jogos muito longos'
    },
    { 
      id: 104, 
      title: 'Returnal', 
      genre: 'Bullet Hell', 
      rating: 4.5, 
      hours: 30, 
      image: 'https://images.unsplash.com/photo-1627856014759-0852292467d9?auto=format&fit=crop&w=600',
      matchScore: 45,
      reason: 'Estilo de jogo diferente do seu habitual'
    },
  ];

  // Função para definir a cor da "Tag" baseada na porcentagem
  const getMatchColor = (score) => {
    if (score >= 90) return '#10b981'; // Verde (Muito provável)
    if (score >= 70) return '#f59e0b'; // Amarelo (Provável)
    return '#ef4444'; // Vermelho (Arriscado)
  };

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
            Nosso modelo analisou seu perfil e calculou a probabilidade de você <strong>zerar</strong> estes jogos.
          </p>
        </div>
      </div>

      <div className="row g-4">
        {aiRecommendations.map(game => (
          <div key={game.id} className="col-md-3">
            
            {/* Renderizamos o Card */}
            <GameCard 
              id={game.id}
              title={game.title}
              genre={game.genre}
              rating={game.rating}
              hours={game.hours}
              image={game.image}
              // A tag agora mostra a porcentagem
              tag={`${game.matchScore}% Chance de Zerar`}
              // A cor muda dinamicamente (Verde/Amarelo/Vermelho)
              tagColor={getMatchColor(game.matchScore)}
            />

            {/* Painel de Detalhes da IA (Abaixo do Card) */}
            <div className="mt-3 px-2">
              {/* Barra de Progresso Visual */}
              <div className="d-flex justify-content-between align-items-center mb-1">
                <small className="text-secondary fw-bold" style={{fontSize: '0.7rem'}}>MATCH SCORE</small>
                <small className="fw-bold" style={{color: getMatchColor(game.matchScore)}}>{game.matchScore}%</small>
              </div>
              
              <div className="progress bg-dark border border-secondary border-opacity-25 mb-3" style={{ height: '6px' }}>
                <div 
                  className="progress-bar" 
                  role="progressbar" 
                  style={{ 
                    width: `${game.matchScore}%`, 
                    backgroundColor: getMatchColor(game.matchScore),
                    borderRadius: '10px'
                  }} 
                ></div>
              </div>
              
              {/* Motivo da Recomendação */}
              <div className="d-flex align-items-start text-secondary bg-black bg-opacity-25 p-2 rounded-3 border border-secondary border-opacity-10">
                <FaChartLine className="me-2 mt-1 flex-shrink-0" style={{ color: getMatchColor(game.matchScore) }} />
                <span style={{ fontSize: '0.8rem', lineHeight: '1.4' }}>{game.reason}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recomendacoes;