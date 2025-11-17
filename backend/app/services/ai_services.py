import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer 
from fastapi import HTTPException
from typing import List, Dict, Any

from ..models import game_model  
from ..schemas.game_schema import GameStatus  


def prepare_data_for_ai(games_list: list) -> pd.DataFrame | None:

    if not games_list or len(games_list) < 10: 
        return None

    df = pd.DataFrame(games_list)
    
    # 1. CRIAÇÃO DA VARIÁVEL ALVO (TARGET)
    # 1 (Sim) se o status do jogo for "Finalizado", 0 (Não) caso contrário.
    df['target_finalizado'] = df['status'].apply(
        lambda x: 1 if x == GameStatus.finalizado.value else 0
    )
    
    # 2. ENGENHARIA DE FEATURES NUMÉRICAS
    df['playtime_forever'] = df['playtime_forever'].fillna(0)
    df['log_playtime'] = df['playtime_forever'].apply(lambda x: np.log1p(x))
    
    # 3. PROCESSAMENTO DE GÊNEROS (ONE-HOT ENCODING)
    # O objetivo é transformar a string de gêneros em colunas binárias numéricas.
    df['genero'] = df['genero'].fillna('') 
    df['genero_list'] = df['genero'].astype(str).str.split(', ')

    mlb = MultiLabelBinarizer()
    generos_binarios = mlb.fit_transform(df['genero_list'])
    
    # Cria um DataFrame para os gêneros, prefixando com 'gen_'
    genero_df = pd.DataFrame(generos_binarios, columns=[f'gen_{g}' for g in mlb.classes_])
    
    # Concatena as colunas de gênero com o DataFrame principal
    df = pd.concat([df.reset_index(drop=True), genero_df.reset_index(drop=True)], axis=1)
    
    # 4. Retorno Final
    # Seleciona as colunas de features criadas
    feature_cols = [col for col in df.columns if col.startswith('gen_') or col in ['log_playtime']]

    return df.fillna(0)[feature_cols + ['target_finalizado', 'appid', 'name', 'status', 'genero']].copy()


def generate_recommendations(user_id: str) -> List[Dict[str, Any]]:
    """
    Busca os dados do usuário, treina o modelo de classificação e gera as recomendações.
    """
    # 1. BUSCAR DADOS DO BANCO E PREPARAR
    games_list = game_model.get_user_games(user_id) 
    processed_df = prepare_data_for_ai(games_list)
    
    # Verifica se há dados suficientes para treinar a IA
    if processed_df is None or processed_df[processed_df['status'] != GameStatus.nao_iniciado.value].empty:
        raise HTTPException(status_code=404, detail="Dados insuficientes para treinar a IA. Você precisa ter mais de 10 jogos e ter finalizado/jogado alguns.")

    # 2. SEPARAR DADOS DE TREINAMENTO E PREDIÇÃO
    # Treinamento: Jogos com resultado conhecido (finalizado ou jogando/abandonado)
    df_train = processed_df[processed_df['status'] != GameStatus.nao_iniciado.value]
    
    # Predição: Jogos do backlog (status 'Não Iniciado')
    df_predict = processed_df[processed_df['status'] == GameStatus.nao_iniciado.value]
    
    if df_predict.empty:
        return [{"message": "Parabéns! Você já jogou todos os seus jogos!"}] 

    # Colunas de Features (X)
    train_features = [col for col in df_train.columns if col.startswith('gen_') or col in ['log_playtime']]
    
    X_train = df_train[train_features]
    y_train = df_train['target_finalizado']
    
    # 3. TREINAMENTO DO MODELO (Regressão Logística)
    # class_weight='balanced' ajuda o modelo a lidar com o desbalanceamento de classes (poucos jogos finalizados)
    model = LogisticRegression(solver='liblinear', random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    # 4. PREDIÇÃO
    # X_predict deve ter as mesmas colunas que X_train
    X_predict = df_predict[train_features].fillna(0)
    
    # Preve a probabilidade de o jogo ser finalizado (coluna [:, 1] é a probabilidade do "1")
    probabilities = model.predict_proba(X_predict)[:, 1]
    
    # Adiciona as probabilidades ao DataFrame de previsão
    df_predict = df_predict.copy()
    df_predict['probabilidade_finalizar'] = probabilities
    
    # 5. RETORNAR AS TOP RECOMENDAÇÕES
    
    # Classifica os jogos pela maior probabilidade e pega os 10 primeiros
    top_recommendations = df_predict.sort_values(by='probabilidade_finalizar', ascending=False)
    
    recommendations_list = top_recommendations[['appid', 'name', 'probabilidade_finalizar', 'genero']].head(10).to_dict('records')

    # Converte a probabilidade para porcentagem (Ex: 0.85 -> 85.00)
    for rec in recommendations_list:
        rec['probabilidade_finalizar'] = round(rec['probabilidade_finalizar'] * 100, 2)
        rec['appid'] = int(rec['appid']) 
        
    return recommendations_list