from fastapi import APIRouter, Path, HTTPException
from fastapi.responses import StreamingResponse
from ..services.ai_services import generate_recommendations, prepare_data_for_ai, train_and_save_model
from ..models import game_model
from typing import List, Dict, Any, Union
import io
import pandas as pd
from fastapi import BackgroundTasks

router = APIRouter(
    prefix="/recommendations",
    tags=["Inteligência Artificial (IA)"]
)
@router.get("/{user_id}", response_model=Dict[str, Union[List[Dict[str, Any]], List[str]]])
async def get_game_recommendations(
    user_id: str = Path(..., title="ID do Usuário no Firebase", description="UID do usuário para gerar recomendações.")
):

    try:
        result = generate_recommendations(user_id)
        recommendations = result.get("recommendations")
        
        if not recommendations:
            raise HTTPException(status_code=404, detail="Dados insuficientes para gerar recomendações. Jogue ou sincronize mais jogos!")
            
        return result
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao gerar recomendações de IA: {e}")

@router.get("/export-csv/{user_id}")
async def export_user_data_csv(
    user_id: str = Path(..., title="ID do Usuário", description="UID para exportar dados.")
):

    try:
    
        games_list = game_model.get_user_games(user_id)
        if not games_list:
            raise HTTPException(status_code=404, detail="Nenhum jogo encontrado.")

        df = prepare_data_for_ai(games_list)
        
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail="Erro ao processar dados (DataFrame vazio).")

        stream = io.StringIO()
        df.to_csv(stream, index=False)
        stream.seek(0)
       
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = f"attachment; filename=dados_ia_{user_id}.csv"
        
        return response

    except Exception as e:
        print(f"Erro ao exportar CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao exportar CSV: {str(e)}")
    
@router.post("/train/{user_id}")
async def force_train_model(
    background_tasks: BackgroundTasks,
    user_id: str = Path(..., title="ID do Usuário")
):

    background_tasks.add_task(train_and_save_model, user_id)
    return {"message": "Treinamento de IA agendado.", "status": "processing"}