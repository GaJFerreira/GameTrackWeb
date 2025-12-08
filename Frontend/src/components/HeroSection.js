import React from 'react';
import { Link } from 'react-router-dom';
import { FaArrowRight } from 'react-icons/fa'; // Removi FaPlay

const HeroSection = () => {
  return (
    <section className="py-5 border-bottom border-secondary border-opacity-25">
      <div className="container">
        <div className="row align-items-center">
          <div className="col-lg-6 mb-5 mb-lg-0">
            <div className="tag-badge">● Descubra seus próximos games favoritos</div>
            <h1 className="display-4 fw-bold text-white mb-4">Recomendações de <br />Jogos Personalizadas</h1>
            <p className="lead text-secondary mb-5">
              Nosso algoritmo inteligente recomenda títulos incríveis baseados no que você joga.
            </p>
            <div className="d-flex gap-3">
              <Link to="/recomendacoes" className="btn btn-brand-red btn-lg px-4 d-flex align-items-center gap-2">
                Começar a Explorar <FaArrowRight />
              </Link>
              
              {/* 3. BOTÃO 'VER DEMO' REMOVIDO DAQUI */}

            </div>
          </div>
          <div className="col-lg-6">
            <div className="card border-0 rounded-4 overflow-hidden position-relative shadow-lg">
              <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&q=80&w=800" alt="Hero" className="img-fluid" style={{ filter: 'brightness(0.6)' }} />
              <div className="position-absolute bottom-0 start-0 p-4">
  
                
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;