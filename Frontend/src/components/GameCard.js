import React from 'react';
import { FaStar, FaClock } from 'react-icons/fa';

const GameCard = ({ title, genre, image, rating, hours, tag, tagColor }) => {
  return (
    <div className="card h-100 bg-dark border-0 rounded-4 shadow-sm overflow-hidden text-white">
      {/* Imagem e Tag */}
      <div className="position-relative">
        <img 
          src={image} 
          className="card-img-top" 
          alt={title} 
          style={{ height: '220px', objectFit: 'cover', opacity: '0.9' }} 
        />
        {tag && (
          <span 
            className="position-absolute top-0 end-0 m-3 badge py-2 px-3"
            style={{ backgroundColor: tagColor || '#2563eb' }}
          >
            {tag}
          </span>
        )}
      </div>

      {/* Corpo do Card */}
      <div className="card-body d-flex flex-column">
        <p className="mb-2 text-uppercase fw-bold" style={{ color: '#4f46e5', fontSize: '0.75rem', letterSpacing: '1px' }}>
          {genre}
        </p>
        <h5 className="card-title fw-bold mb-auto">{title}</h5>

        {/* Rodapé: Nota e Horas */}
        <div className="d-flex justify-content-between align-items-center mt-3 pt-3 border-top border-secondary">
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