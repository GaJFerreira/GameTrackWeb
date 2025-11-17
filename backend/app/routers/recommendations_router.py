# app/routers/recommendations_router.py
from fastapi import APIRouter, Path, HTTPException
# CORREÇÃO AQUI: Importa a função diretamente do arquivo ai_service.py
from ..services.ai_services import generate_recommendations 
from typing import List, Dict, Any

router = APIRouter(
    prefix="/recommendations",
    tags=["Inteligência Artificial (IA)"]
)

# ROTA DE IA (MODO DE TESTE)
@router.get("/{user_id}", response_model=List[Dict[str, Any]])
async def get_game_recommendations(
    user_id: str = Path(..., title="ID do Usuário no Firebase", description="UID do usuário para gerar recomendações.")
):
    """
    Gera e retorna a lista dos 10 jogos do backlog que o usuário tem 
    a maior probabilidade de finalizar, com base no seu histórico de jogatina.
    """
    try:
        # Chama a função diretamente
        recommendations = generate_recommendations(user_id)
        
        if not recommendations:
            raise HTTPException(status_code=404, detail="Dados insuficientes para gerar recomendações. Jogue ou sincronize mais jogos!")
            
        return recommendations
        
    except HTTPException as e:
        raise e
    except Exception as e:
        # A lógica da IA é complexa, se der erro, retorna 500 com o detalhe
        raise HTTPException(status_code=500, detail=f"Erro interno ao gerar recomendações de IA: {e}")