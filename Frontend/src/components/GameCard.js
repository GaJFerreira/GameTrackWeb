import React from 'react';
import { FaStar, FaClock } from 'react-icons/fa';
import { Link } from 'react-router-dom'; // Importação essencial para navegação

const GameCard = ({ id, title, genre, image, rating, hours, tag, tagColor }) => {
  // Se não vier um ID (nos dados simulados), usamos '1' para o link não quebrar
  const gameId = id || 1;

  return (
    <div className="card h-100 bg-dark border-0 rounded-4 shadow-sm overflow-hidden text-white hover-effect">
      {/* Imagem com Link para Detalhes */}
      <div className="position-relative">
        <Link to={`/jogo/${gameId}`}>
          <img 
            src={image} 
            className="card-img-top" 
            alt={title} 
            style={{ height: '220px', objectFit: 'cover', opacity: '0.9', cursor: 'pointer' }} 
          />
        </Link>
        
        {tag && (
          <span 
            className="position-absolute top-0 end-0 m-3 badge py-2 px-3"
            style={{ backgroundColor: tagColor || '#2563eb' }}
          >
            {tag}
          </span>
        )}
      </div>

      <div className="card-body d-flex flex-column">
        <p className="mb-2 text-uppercase fw-bold" style={{ color: '#4f46e5', fontSize: '0.75rem', letterSpacing: '1px' }}>
          {genre}
        </p>

        {/* Título com Link */}
        <Link to={`/jogo/${gameId}`} className="text-white text-decoration-none">
          <h5 className="card-title fw-bold mb-auto hover-underline">{title}</h5>
        </Link>

        <div className="d-flex justify-content-between align-items-center mt-3 pt-3 border-top border-secondary border-opacity-25">
          <div className="d-flex align-items-center text-warning">
            <FaStar className="me-2" />
            <span className="fw-bold text-white">{rating}</span>
          </div>
          <div className="d-flex align-items-center text-secondary">
            <FaClock className="me-2" />
            <small>{hours ? `${hours}h` : 'N/A'}</small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GameCard;