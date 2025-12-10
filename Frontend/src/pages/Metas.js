import React, { useState, useEffect } from 'react';
import { FaBullseye, FaPlus, FaCalendarAlt, FaGamepad } from 'react-icons/fa';
import { toast } from 'react-toastify';
import api from '../services/api';

const Metas = () => {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newGoal, setNewGoal] = useState({ game: '', type: 'Conclusão', target: '', deadline: '' });
  const [libraryGames, setLibraryGames] = useState([]);

  useEffect(() => {
    const fetchGoals = async () => {
      try {
        const authResponse = await api.get('/auth/me');
        const uid = authResponse.data.user.uid;
        
        const response = await api.get(`/metas/${uid}`);
        setGoals(response.data);
        const gamesResponse = await api.get(`/games/${uid}`);
        const sortedGames = gamesResponse.data.sort((a, b) => a.name.localeCompare(b.name));
        setLibraryGames(sortedGames);

      } catch (error) {
        console.error("Erro ao carregar metas", error);
      } finally {
        setLoading(false);
      }
    };
    fetchGoals();
  }, []);

  const handleAddGoal = async (e) => {
    e.preventDefault();
    
    if (!newGoal.game || !newGoal.target) {
        toast.error('Preencha o nome do jogo e o alvo da meta!');
        return;
    }

    try {
        const authResponse = await api.get('/auth/me');
        const uid = authResponse.data.user.uid;

        const response = await api.post(`/metas/${uid}`, newGoal);
        
        setGoals([...goals, response.data]);
        
        setNewGoal({ game: '', type: 'Conclusão', target: '', deadline: '' }); 
        toast.success('Meta criada com sucesso!');

    } catch (error) {
        console.error(error);
        toast.error('Erro ao salvar meta.');
    }
  };

  return (
    <div className="container py-5">
      <div className="row">
        
        {/* Formulário de Nova Meta */}
        <div className="col-lg-4 mb-5">
          <div className="card bg-dark text-white border-0 shadow-lg rounded-4 p-4 sticky-top" style={{top: '20px'}}>
            <h4 className="fw-bold mb-4 d-flex align-items-center gap-2">
              <FaPlus className="text-danger" /> Nova Meta
            </h4>
            
            <form onSubmit={handleAddGoal}>
              
              <div className="mb-3">
                <label className="form-label text-secondary small">Selecione o Jogo</label>
                <div className="input-group">
                  <span className="input-group-text bg-dark border-secondary text-secondary"><FaGamepad /></span>
                  <select 
                    className="form-select form-control-dark text-white bg-dark border-secondary"
                    value={newGoal.game}
                    onChange={e => setNewGoal({...newGoal, game: e.target.value})}
                  >
                    <option value="">Escolha um jogo da biblioteca...</option>
                    {libraryGames.map(game => (
                      <option key={game.appid} value={game.name}>
                        {game.name}
                      </option>
                    ))}
                  </select>
                </div>
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

        {/* Lista de Metas */}
        <div className="col-lg-8">
          <div className="d-flex align-items-center justify-content-between mb-4">
            <h2 className="text-white fw-bold mb-0">Minhas Metas Atuais</h2>
            <span className="badge bg-secondary">{goals.length} Ativas</span>
          </div>

          <div className="row g-4">
            {goals.map((goal, index) => (
              <div key={goal.id || index} className="col-12">
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

                  <div>
                    <div className="d-flex justify-content-between small mb-1 text-secondary">
                      <span>Progresso</span>
                      <span>{goal.progress || 0}%</span>
                    </div>
                    <div className="progress bg-black" style={{ height: '8px' }}>
                      <div 
                        className={`progress-bar ${goal.progress === 100 ? 'bg-success' : 'bg-brand-red'}`} 
                        role="progressbar" 
                        style={{ width: `${goal.progress || 0}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            {!loading && goals.length === 0 && (
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