import React from 'react';
import HeroSection from '../components/HeroSection';
import GameCard from '../components/GameCard';

const Home = () => {
  const games = [
    { id: 1, title: 'Cyberpunk Edge', genre: 'RPG / Ação', rating: 4.8, hours: 85, tag: 'Recomendado', tagColor: '#2563eb', image: 'https://images.unsplash.com/photo-1533230408703-912440333d64?auto=format&fit=crop&w=400' },
    { id: 2, title: 'Phantom Protocol', genre: 'Estratégia', rating: 4.6, hours: 120, tag: 'Trending', tagColor: '#1e3a8a', image: 'https://images.unsplash.com/photo-1616588589676-60b30c3c7448?auto=format&fit=crop&w=400' },
    { id: 3, title: 'Neon Horizons', genre: 'Aventura', rating: 4.9, hours: 65, tag: 'Top Rated', tagColor: '#4338ca', image: 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=400' },
  ];

  return (
    <>
      <HeroSection />
      <section className="container py-5">
        <div className="mb-4">
          <p className="text-primary fw-bold mb-1 text-uppercase small">Para você</p>
          <h2 className="text-white fw-bold">Destaques da Semana</h2>
        </div>
        <div className="row g-4">
          {games.map(game => (
            <div key={game.id} className="col-md-4">
              <GameCard {...game} />
            </div>
          ))}
        </div>
      </section>
    </>
  );
};

export default Home;