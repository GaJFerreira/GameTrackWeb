import React, { useState } from 'react';
import { FaBullseye, FaPlus, FaCalendarAlt, FaCheckCircle, FaHourglassHalf } from 'react-icons/fa';

const Metas = () => {
  // Lista inicial de metas (Simulação)
  const [goals, setGoals] = useState([
    { id: 1, game: 'Elden Ring', type: 'Conclusão', target: 'Zerar Campanha', deadline: '2023-12-31', progress: 80 },
    { id: 2, game: 'Valorant', type: 'Tempo', target: '100 Horas', deadline: '2023-11-20', progress: 45 },
  ]);

  // Estado para o formulário
  const [newGoal, setNewGoal] = useState({ game: '', type: 'Conclusão', target: '', deadline: '' });

  const handleAddGoal = (e) => {
    e.preventDefault();
    if (!newGoal.game || !newGoal.target) return;

    const goalToAdd = {
      id: Date.now(),
      ...newGoal,
      progress: 0 // Começa com 0%
    };

    setGoals([...goals, goalToAdd]);
    setNewGoal({ game: '', type: 'Conclusão', target: '', deadline: '' }); // Limpa form
    alert("Meta adicionada com sucesso!");
  };

  return (
    <div className="container py-5">
      <div className="row">
        
        {/* LADO ESQUERDO: Formulário de Nova Meta */}
        <div className="col-lg-4 mb-5">
          <div className="card bg-dark text-white border-0 shadow-lg rounded-4 p-4 sticky-top" style={{top: '20px'}}>
            <h4 className="fw-bold mb-4 d-flex align-items-center gap-2">
              <FaPlus className="text-danger" /> Nova Meta
            </h4>
            
            <form onSubmit={handleAddGoal}>
              <div className="mb-3">
                <label className="form-label text-secondary small">Nome do Jogo</label>
                <input 
                  type="text" 
                  className="form-control form-control-dark" 
                  placeholder="Ex: God of War"
                  value={newGoal.game}
                  onChange={e => setNewGoal({...newGoal, game: e.target.value})}
                />
              </div>

              <div className="mb-3">
                <label className="form-label text-secondary small">Tipo de Meta</label>
                <select 
                  className="form-select form-control-dark"
                  value={newGoal.type}
                  onChange={e => setNewGoal({...newGoal, type: e.target.value})}
                >
                  <option value="Conclusão">Conclusão (Zerar/Platinar)</option>
                  <option value="Tempo">Tempo de Jogo (Horas)</option>
                </select>
              </div>

              <div className="mb-3">
                <label className="form-label text-secondary small">Valor do Alvo</label>
                <input 
                  type="text" 
                  className="form-control form-control-dark" 
                  placeholder={newGoal.type === 'Tempo' ? "Ex: 50 Horas" : "Ex: Finalizar modo Difícil"}
                  value={newGoal.target}
                  onChange={e => setNewGoal({...newGoal, target: e.target.value})}
                />
              </div>

              <div className="mb-4">
                <label className="form-label text-secondary small">Prazo (Data Limite)</label>
                <input 
                  type="date" 
                  className="form-control form-control-dark"
                  value={newGoal.deadline}
                  onChange={e => setNewGoal({...newGoal, deadline: e.target.value})}
                />
              </div>

              <button type="submit" className="btn btn-brand-red w-100 fw-bold">
                Criar Meta
              </button>
            </form>
          </div>
        </div>

        {/* LADO DIREITO: Lista de Metas */}
        <div className="col-lg-8">
          <div className="d-flex align-items-center justify-content-between mb-4">
            <h2 className="text-white fw-bold mb-0">Minhas Metas Atuais</h2>
            <span className="badge bg-secondary">{goals.length} Ativas</span>
          </div>

          <div className="row g-4">
            {goals.map(goal => (
              <div key={goal.id} className="col-12">
                <div className="card bg-dark border border-secondary border-opacity-25 rounded-4 p-4 text-white">
                  <div className="d-flex justify-content-between align-items-start mb-3">
                    <div>
                      <h5 className="fw-bold mb-1 text-primary">{goal.game}</h5>
                      <span className={`badge ${goal.type === 'Tempo' ? 'bg-info' : 'bg-success'} mb-2`}>
                        {goal.type}
                      </span>
                      <h4 className="fw-bold">{goal.target}</h4>
                    </div>
                    <div className="text-end text-secondary">
                      <div className="d-flex align-items-center gap-2 mb-1">
                        <FaCalendarAlt /> 
                        <small>{goal.deadline || 'Sem prazo'}</small>
                      </div>
                    </div>
                  </div>

                  {/* Barra de Progresso Simulada */}
                  <div>
                    <div className="d-flex justify-content-between small mb-1 text-secondary">
                      <span>Progresso</span>
                      <span>{goal.progress}%</span>
                    </div>
                    <div className="progress bg-black" style={{ height: '8px' }}>
                      <div 
                        className={`progress-bar ${goal.progress === 100 ? 'bg-success' : 'bg-brand-red'}`} 
                        role="progressbar" 
                        style={{ width: `${goal.progress}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            {goals.length === 0 && (
              <div className="text-center text-secondary py-5">
                <FaBullseye size={48} className="mb-3 opacity-50" />
                <p>Nenhuma meta definida. Crie uma para começar!</p>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};

export default Metas;