import React, { useState, useEffect } from 'react';
import { FaBullseye, FaPlus, FaCalendarAlt, FaTrash, FaCheckCircle, FaHourglassHalf } from 'react-icons/fa';
import api from '../services/api';

const Metas = () => {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState(null);

  // Estado para o formulário
  const [newGoal, setNewGoal] = useState({ 
    game_name: '', 
    tipo: 'CONCLUSAO', 
    valor_meta: '', 
    data_limite: '' 
  });

  // 1. Carregar Usuário e Metas
  useEffect(() => {
    const fetchData = async () => {
      try {
        const authRes = await api.get('/auth/me');
        const uid = authRes.data.user.uid;
        setUserData(authRes.data.user);

        const metasRes = await api.get(`/metas/${uid}`);
        
        // O Firebase retorna os dados, mas precisamos garantir que o ID venha junto para poder deletar depois
        // O router atual retorna a lista direta dos dados, se o ID não estiver no corpo, pode faltar.
        // Assumindo que seu backend salva o ID ou retorna ele:
        setGoals(metasRes.data); 

      } catch (error) {
        console.error("Erro ao carregar metas:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // 2. Criar Meta
  const handleAddGoal = async (e) => {
    e.preventDefault();
    if (!newGoal.game_name || !newGoal.valor_meta) return;

    try {
      const payload = {
        ...newGoal,
        progresso_atual: 0,
        status: 'EM_ANDAMENTO',
        created_at: new Date().toISOString()
      };

      const response = await api.post(`/metas/${userData.uid}`, payload);
      
      // O backend retorna { message: "...", id: "..." }
      // Adicionamos na lista localmente para não precisar recarregar tudo
      setGoals([...goals, { ...payload, id: response.data.id }]);
      
      // Limpa formulário
      setNewGoal({ game_name: '', tipo: 'CONCLUSAO', valor_meta: '', data_limite: '' });
      alert("Meta criada com sucesso!");

    } catch (error) {
      console.error("Erro ao criar meta:", error);
      alert("Erro ao salvar meta.");
    }
  };

  // 3. Deletar Meta
  const handleDeleteGoal = async (metaId) => {
    if (!window.confirm("Tem certeza que deseja excluir esta meta?")) return;

    try {
      // Como o backend no list_metas pode não estar retornando o ID do documento dentro do objeto,
      // precisamos garantir que o create_meta ou list_metas inclua isso.
      // Se tiver problemas aqui, me avise para ajustarmos o backend.
      await api.delete(`/metas/${userData.uid}/${metaId}`);
      
      // Remove da lista visualmente
      setGoals(goals.filter(g => g.id !== metaId && g._id !== metaId)); // Tenta pegar id ou _id caso varie

    } catch (error) {
      console.error("Erro ao deletar:", error);
      alert("Não foi possível deletar a meta.");
    }
  };

  // Função auxiliar para cor do badge
  const getTypeBadge = (type) => {
    return type === 'TEMPO' ? 'bg-info text-dark' : 'bg-success text-white';
  };

  return (
    <div className="container py-5">
      <div className="row">
        
        {/* LADO ESQUERDO: Formulário de Nova Meta */}
        <div className="col-lg-4 mb-5">
          <div className="card bg-dark text-white border-secondary border-opacity-25 shadow-lg rounded-4 p-4 sticky-top" style={{top: '20px'}}>
            <h4 className="fw-bold mb-4 d-flex align-items-center gap-2">
              <FaPlus className="text-danger" /> Nova Meta
            </h4>
            
            <form onSubmit={handleAddGoal}>
              <div className="mb-3">
                <label className="form-label text-secondary small text-uppercase fw-bold">Jogo</label>
                <input 
                  type="text" 
                  className="form-control form-control-dark" 
                  placeholder="Ex: Elden Ring"
                  value={newGoal.game_name}
                  onChange={e => setNewGoal({...newGoal, game_name: e.target.value})}
                />
              </div>

              <div className="mb-3">
                <label className="form-label text-secondary small text-uppercase fw-bold">Tipo</label>
                <select 
                  className="form-select form-control-dark"
                  value={newGoal.tipo}
                  onChange={e => setNewGoal({...newGoal, tipo: e.target.value})}
                >
                  <option value="CONCLUSAO">Conclusão (Zerar/Platinar)</option>
                  <option value="TEMPO">Tempo de Jogo (Horas)</option>
                </select>
              </div>

              <div className="mb-3">
                <label className="form-label text-secondary small text-uppercase fw-bold">Objetivo</label>
                <input 
                  type="text" 
                  className="form-control form-control-dark" 
                  placeholder={newGoal.tipo === 'TEMPO' ? "Ex: Chegar a 50 horas" : "Ex: Matar Malenia"}
                  value={newGoal.valor_meta}
                  onChange={e => setNewGoal({...newGoal, valor_meta: e.target.value})}
                />
              </div>

              <div className="mb-4">
                <label className="form-label text-secondary small text-uppercase fw-bold">Prazo</label>
                <input 
                  type="date" 
                  className="form-control form-control-dark"
                  value={newGoal.data_limite}
                  onChange={e => setNewGoal({...newGoal, data_limite: e.target.value})}
                />
              </div>

              <button type="submit" className="btn btn-brand-red w-100 fw-bold py-2" disabled={!userData}>
                {userData ? 'Criar Meta' : 'Carregando...'}
              </button>
            </form>
          </div>
        </div>

        {/* LADO DIREITO: Lista de Metas */}
        <div className="col-lg-8">
          <div className="d-flex align-items-center justify-content-between mb-4">
            <h2 className="text-white fw-bold mb-0">Minhas Metas</h2>
            <span className="badge bg-secondary">{goals.length} Ativas</span>
          </div>

          {loading ? (
            <div className="text-center text-white mt-5">Carregando metas...</div>
          ) : (
            <div className="row g-4">
              {goals.map((goal, index) => (
                <div key={goal.id || index} className="col-12">
                  <div className="card bg-dark border border-secondary border-opacity-25 rounded-4 p-4 text-white">
                    <div className="d-flex justify-content-between align-items-start">
                      
                      {/* Conteúdo da Meta */}
                      <div>
                        <div className="d-flex align-items-center gap-2 mb-2">
                          <h5 className="fw-bold mb-0 text-white">{goal.game_name}</h5>
                          <span className={`badge ${getTypeBadge(goal.tipo)} rounded-pill`} style={{fontSize: '0.65rem'}}>
                            {goal.tipo === 'CONCLUSAO' ? 'CONCLUSÃO' : 'TEMPO'}
                          </span>
                        </div>
                        
                        <h3 className="fw-bold text-primary mb-3">{goal.valor_meta}</h3>
                        
                        <div className="d-flex align-items-center gap-3 text-secondary small">
                          <div className="d-flex align-items-center gap-1">
                            <FaCalendarAlt /> 
                            <span>{goal.data_limite ? new Date(goal.data_limite).toLocaleDateString('pt-BR') : 'Sem prazo'}</span>
                          </div>
                          {goal.status === 'EM_ANDAMENTO' && (
                            <div className="d-flex align-items-center gap-1 text-warning">
                              <FaHourglassHalf /> Em andamento
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Botão de Excluir */}
                      <div>
                        <button 
                          onClick={() => handleDeleteGoal(goal.id)}
                          className="btn btn-outline-danger btn-sm border-0"
                          title="Excluir Meta"
                        >
                          <FaTrash />
                        </button>
                      </div>
                    </div>

                    {/* Barra de Progresso (Simulada, pois o backend ainda não calcula progresso real) */}
                    <div className="mt-3">
                      <div className="progress bg-black bg-opacity-50" style={{ height: '6px' }}>
                        <div 
                          className="progress-bar bg-primary" 
                          role="progressbar" 
                          style={{ width: `${goal.progresso_atual || 0}%` }}
                        ></div>
                      </div>
                    </div>

                  </div>
                </div>
              ))}
              
              {goals.length === 0 && (
                <div className="text-center text-secondary py-5 border border-secondary border-opacity-10 rounded-4 dashed-border">
                  <FaBullseye size={48} className="mb-3 opacity-25" />
                  <p className="mb-0">Nenhuma meta definida.</p>
                  <small>Use o formulário ao lado para criar seu primeiro objetivo!</small>
                </div>
              )}
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default Metas;