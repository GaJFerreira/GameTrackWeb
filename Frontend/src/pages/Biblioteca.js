import React from 'react';
import GameCard from '../components/GameCard';

const Biblioteca = () => {
  const myGames = [
    { id: 1, title: 'Elden Ring', genre: 'RPG', rating: 5.0, hours: 210, image: 'https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=400' },
    { id: 2, title: 'God of War', genre: 'Ação', rating: 4.9, hours: 45, image: 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=400' },
    { id: 3, title: 'Hollow Knight', genre: 'Indie', rating: 4.8, hours: 30, image: 'https://images.unsplash.com/photo-1542751110-97427bbecf20?auto=format&fit=crop&w=400' },
    { id: 4, title: 'Valorant', genre: 'FPS', rating: 4.2, hours: 500, image: 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?auto=format&fit=crop&w=400' },
  ];

  return (
    <div className="container py-5">
      <h2 className="text-white fw-bold mb-4">Minha Biblioteca</h2>
      <div className="row g-4">
        {myGames.map((game, idx) => (
          <div key={idx} className="col-6 col-md-3">
            <GameCard {...game} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Biblioteca;