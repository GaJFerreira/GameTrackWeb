import React, { useState, useEffect } from 'react';
import { FaBullseye, FaPlus, FaCalendarAlt } from 'react-icons/fa';
import { toast } from 'react-toastify';
import api from '../services/api';

const Metas = () => {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newGoal, setNewGoal] = useState({ game: '', type: 'Conclusão', target: '', deadline: '' });

  useEffect(() => {
    const fetchGoals = async () => {
      try {
        const authResponse = await api.get('/auth/me');
        const uid = authResponse.data.user.uid;

        const response = await api.get(`/users/${uid}/goals`); 
        setGoals(response.data);
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
        const response = await api.post(`/users/${uid}/goals`, newGoal);
        
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
        <div className="col-lg-4 mb-5">
           <div className="card bg-dark text-white border-0 shadow-lg rounded-4 p-4 sticky-top">
             <h4 className="fw-bold mb-4 d-flex align-items-center gap-2"><FaPlus className="text-danger"/> Nova Meta</h4>
             <form onSubmit={handleAddGoal}>
                <div className="mb-3">
                    <label className="text-secondary small">Nome do Jogo</label>
                    <input type="text" className="form-control form-control-dark" value={newGoal.game} onChange={e => setNewGoal({...newGoal, game: e.target.value})} />
                </div>
                 <div className="mb-3">
                    <label className="text-secondary small">Alvo</label>
                    <input type="text" className="form-control form-control-dark" value={newGoal.target} onChange={e => setNewGoal({...newGoal, target: e.target.value})} />
                </div>
                <button type="submit" className="btn btn-brand-red w-100 fw-bold">Criar Meta</button>
             </form>
           </div>
        </div>

        {/* Lista de Metas */}
        <div className="col-lg-8">
            <h2 className="text-white fw-bold mb-4">Minhas Metas</h2>
            {loading ? <p className="text-white">Carregando...</p> : (
                <div className="row g-4">
                    {goals.map(goal => (
                    <div key={goal.id} className="col-12">
                        <div className="card bg-dark border border-secondary border-opacity-25 rounded-4 p-4 text-white">
                            <h5 className="fw-bold text-primary">{goal.game}</h5>
                            <p>{goal.target}</p>
                        </div>
                    </div>
                    ))}
                </div>
            )}
        </div>
      </div>
    </div>
  );
};

export default Metas;