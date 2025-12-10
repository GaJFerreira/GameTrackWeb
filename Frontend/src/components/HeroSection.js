import { Link } from "react-router-dom"
import { FaArrowRight } from "react-icons/fa"

const HeroSection = () => {
  return (
    <section className="py-16 lg:py-20 border-bottom border-secondary border-opacity-25">
      <div className="container">
        <div className="row align-items-center g-5 lg:g-0">
          <div className="col-lg-6 mb-4 lg:mb-0 pt-4 lg:pt-8">
            <div className="tag-badge mb-6 text-opacity-80 tracking-wide">● Descubra seus próximos games favoritos</div>

            <h1 className="display-4 fw-bold text-white mb-2 lh-tight">GameTrack</h1>
            <h3 className="display-5 fw-bold text-white mb-8 lh-tight" style={{ fontSize: "2.8rem" }}>
              Organize <br className="d-none d-lg-block" />
              Sua Biblioteca
            </h3>

            <p className="lead text-secondary mb-3 lh-relaxed fw-500" style={{ maxWidth: "90%" }}>
              Crie metas de jogatina e receba sugestões de jogos alinhadas ao seu estilo.
            </p>
            <p className="lead text-secondary mb-8 lh-relaxed" style={{ maxWidth: "95%" }}>
              Algoritimo de IA que aprende com suas preferências e hábitos de jogo. Para te recomendar títulos que você
              realmente vai amar
            </p>

            <div className="d-flex gap-3">
              <Link
                to="/recomendacoes"
                className="btn btn-brand-red btn-lg px-5 d-flex align-items-center gap-2 fw-600 transition-transform"
                style={{ transform: "translateZ(0)" }}
              >
                Começar a Explorar <FaArrowRight size={16} />
              </Link>
            </div>
          </div>

          <div className="col-lg-6 d-flex justify-content-center justify-content-lg-end">
            <div
              className="card border-0 rounded-4 overflow-hidden shadow-lg"
              style={{
                width: "100%",
                maxWidth: "520px",
                aspectRatio: "16 / 10",
                boxShadow: "0 20px 60px rgba(0, 0, 0, 0.5)",
              }}
            >
              <img
                src="https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&q=80&w=800"
                alt="Hero Gaming"
                className="img-fluid h-100 object-cover"
                style={{
                  filter: "brightness(0.65) contrast(1.1)",
                  objectFit: "cover",
                  objectPosition: "center",
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default HeroSection
