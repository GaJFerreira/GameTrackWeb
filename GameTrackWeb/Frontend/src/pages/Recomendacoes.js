import React from 'react';
import GameCard from '../components/GameCard';

const Recomendacoes = () => {
  // Simulando dados de IA
  const recommended = [
    { id: 1, title: 'Dark Souls III', genre: 'RPG', rating: 4.8, hours: 0, tag: 'Porque você jogou Elden Ring', tagColor: '#10b981', image: 'https://images.unsplash.com/photo-1599582200230-03a0d9b4b09b?auto=format&fit=crop&w=400' },
    { id: 2, title: 'Celeste', genre: 'Indie', rating: 4.9, hours: 0, tag: 'Similar a Hollow Knight', tagColor: '#8b5cf6', image: 'https://images.unsplash.com/photo-1523825036634-aab3cce05919?auto=format&fit=crop&w=400' },
    { id: 3, title: 'Overwatch 2', genre: 'FPS', rating: 4.1, hours: 0, tag: 'Gênero que você gosta', tagColor: '#f59e0b', image: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=400' },
  ];

  return (
    <div className="container py-5">
      <div className="mb-5">
        <h2 className="text-white fw-bold">Central de Recomendações IA</h2>
        <p className="text-secondary">Jogos selecionados baseados no seu perfil de jogador.</p>
      </div>
      
      <div className="row g-4">
        {recommended.map(game => (
           <div key={game.id} className="col-md-4">
             <GameCard {...game} />
           </div>
        ))}
      </div>
    </div>
  );
};

export default Recomendacoes;