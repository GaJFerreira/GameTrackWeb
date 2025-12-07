import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score
from fastapi import HTTPException
from typing import List, Dict, Any, Tuple
from datetime import datetime

from ..models import game_model
from ..schemas.game_schema import GameStatus, InteresseNivel

# Diretório para salvar os modelos treinados
MODEL_DIR = "app/models_data"
os.makedirs(MODEL_DIR, exist_ok=True)

def get_model_path(user_id: str):
    return os.path.join(MODEL_DIR, f"model_{user_id}.pkl")

def get_model_instance():
    # Mantivemos Random Forest pois performa bem com dados tabulares mistos
    return RandomForestClassifier(
        n_estimators=100, 
        class_weight="balanced", 
        random_state=42,
        max_depth=10
    )

def analyze_data_coverage(games_list: list) -> List[str]:
    df = pd.DataFrame(games_list)
    warnings = []

    if "status" not in df.columns or df.empty:
        return warnings

    jogos_nao_iniciados = df[df["status"] == GameStatus.nao_iniciado.value]
    total = len(jogos_nao_iniciados)

    if total == 0:
        return warnings

    interesse_na = jogos_nao_iniciados[
        (jogos_nao_iniciados["interesse"].isnull()) |
        (jogos_nao_iniciados["interesse"] == InteresseNivel.na.value) |
        (jogos_nao_iniciados["interesse"] == "N/A")
    ]

    if len(interesse_na) > 0:
        pct = round(len(interesse_na) / total * 100)
        warnings.append(
            f"{pct}% do backlog está sem Nível de Interesse. Defina para melhorar a IA."
        )

    nota_na = jogos_nao_iniciados[
        (jogos_nao_iniciados["nota_pessoal"].isnull()) |
        (jogos_nao_iniciados["nota_pessoal"] == 0)
    ]

    if len(nota_na) > 0:
        pct = round(len(nota_na) / total * 100)
        warnings.append(
            f"{pct}% do backlog está sem Nota Pessoal. Avalie seus jogos jogados."
        )

    return warnings

def prepare_data_for_ai(games_list: list) -> pd.DataFrame | None:
    if not games_list:
        return None

    df = pd.DataFrame(games_list)
    if "status" not in df.columns:
        return None

    # Target: 1 se finalizado, 0 caso contrário
    df["target_finalizado"] = df["status"].apply(
        lambda x: 1 if x == GameStatus.finalizado.value else 0
    )

    # Tratamento Numérico
    df["playtime_forever"] = df.get("playtime_forever", 0).fillna(0)
    df["log_playtime"] = df["playtime_forever"].apply(lambda x: np.log1p(x))
    df["nota_pessoal"] = df.get("nota_pessoal", 0).fillna(0)
    df["metacritic"] = df.get("metacritic", 0).fillna(0)

    # Tratamento de Preço
    def extract_log_final_price(price_data):
        if isinstance(price_data, dict):
            price_raw = price_data.get("preco_final")
            if isinstance(price_raw, (int, float)):
                return np.log1p(price_raw / 100)
        return 0
    df["log_final_price"] = df.get("preco", None).apply(extract_log_final_price)

    # Tratamento de Data
    meses_pt_en = {
        "jan.": "Jan", "fev.": "Feb", "mar.": "Mar", "abr.": "Apr",
        "mai.": "May", "jun.": "Jun", "jul.": "Jul", "ago.": "Aug",
        "set.": "Sep", "out.": "Oct", "nov.": "Nov", "dez.": "Dec"
    }
    def calcular_idade(data_str: str) -> int:
        if not isinstance(data_str, str) or not data_str.strip(): return 0
        data_lower = data_str.lower()
        for pt, en in meses_pt_en.items():
            if pt in data_lower:
                data_lower = data_lower.replace(pt, en)
                break
        try:
            dt = pd.to_datetime(data_lower, errors="coerce")
            if pd.isna(dt): return 0
            return (datetime.now() - dt).days
        except: return 0
        
    df["idade_lancamento_dias"] = df.get("data_lancamento", "").apply(calcular_idade)

    # Tratamento de Interesse
    df["interesse"] = df.get("interesse", "N/A").fillna("N/A")
    interesse_map = {"N/A": 0, "Baixo": 1, "Médio": 2, "Alto": 3}
    df["nivel_interesse_numerico"] = df["interesse"].map(interesse_map).fillna(0)

    # One-Hot Encoding (Gêneros e Categorias)
    df["genero_list"] = df.get("genero", "").fillna("").astype(str).str.split(", ")
    df["categoria_list"] = df.get("categorias", "").fillna("").astype(str).str.split(", ")

    mlb_gen = MultiLabelBinarizer()
    genero_bin = mlb_gen.fit_transform(df["genero_list"])
    genero_df = pd.DataFrame(genero_bin, columns=[f"gen_{g}" for g in mlb_gen.classes_])

    mlb_cat = MultiLabelBinarizer()
    cat_bin = mlb_cat.fit_transform(df["categoria_list"])
    categoria_df = pd.DataFrame(cat_bin, columns=[f"cat_{c}" for c in mlb_cat.classes_])

    # Concatena tudo
    df_final = pd.concat([df.reset_index(drop=True), genero_df, categoria_df], axis=1)
    
    return df_final

def train_and_save_model(user_id: str) -> Dict[str, Any]:
    """
    Treina o modelo com os dados atuais e salva o artefato no disco.
    """
    print(f"[IA] Iniciando treinamento para {user_id}...")
    games_list = game_model.get_user_games(user_id)
    
    if not games_list:
        return {"status": "error", "message": "Sem dados para treinar."}

    try:
        df = prepare_data_for_ai(games_list)
    except Exception as e:
        print(f"[IA] Erro ao preparar dados: {e}")
        return {"status": "error", "message": "Erro no processamento de dados."}

    # Separa Treino (Jogados)
    status_nao_iniciado = GameStatus.nao_iniciado.value
    df_train = df[df["status"] != status_nao_iniciado]

    if len(df_train) < 5:
        # Menos de 5 jogos jogados é muito pouco para treinar
        return {"status": "skipped", "message": "Poucos jogos jogados para treinar IA."}

    # Definição de Features
    feature_cols = [
        col for col in df.columns
        if col.startswith("gen_") or col.startswith("cat_") or col in [
            "log_playtime", "nota_pessoal", "metacritic", 
            "nivel_interesse_numerico", "idade_lancamento_dias", "log_final_price"
        ]
    ]

    X = df_train[feature_cols]
    y = df_train["target_finalizado"]

    # Se só tem 1 classe (ex: o cara amou todos os jogos), o modelo não aprende nada
    if len(np.unique(y)) < 2:
        return {"status": "skipped", "message": "Necessário ter jogos finalizados E não finalizados para aprender."}

    try:
        model = get_model_instance()
        model.fit(X, y)
        
        # Salvamos um dicionário com TUDO que precisamos para prever depois
        artifact = {
            "model": model,
            "features": feature_cols,
            "last_trained": datetime.now().isoformat()
        }
        
        joblib.dump(artifact, get_model_path(user_id))
        print(f"[IA] Modelo salvo com sucesso em {get_model_path(user_id)}")
        
        return {"status": "success", "accuracy": round(model.score(X, y), 2)}

    except Exception as e:
        print(f"[IA] Erro no treinamento: {e}")
        return {"status": "error", "message": str(e)}

def generate_recommendations(user_id: str) -> Dict[str, Any]:
    """
    Carrega o modelo salvo e faz previsões no backlog.
    Se não houver modelo, tenta treinar ou usa fallback.
    """
    games_list = game_model.get_user_games(user_id)
    warnings = analyze_data_coverage(games_list)
    
    if not games_list:
        raise HTTPException(status_code=404, detail="Biblioteca vazia.")

    # Tenta carregar modelo
    model_path = get_model_path(user_id)
    artifact = None
    
    if os.path.exists(model_path):
        try:
            artifact = joblib.load(model_path)
        except:
            print("[IA] Arquivo de modelo corrompido. Treinando novo...")
    
    # Se não tem modelo carregado, tenta treinar agora (cold start)
    if artifact is None:
        train_result = train_and_save_model(user_id)
        if train_result["status"] == "success":
            artifact = joblib.load(model_path)
    
    # Prepara dados atuais
    try:
        df = prepare_data_for_ai(games_list)
    except:
        raise HTTPException(status_code=400, detail="Erro dados.")

    # Filtra Backlog
    status_nao_iniciado = GameStatus.nao_iniciado.value
    df_predict = df[df["status"] == status_nao_iniciado].copy()

    if df_predict.empty:
        return {"recommendations": [], "warnings": ["Backlog vazio!"]}

    # Lógica de Predição
    if artifact:
        model = artifact["model"]
        trained_features = artifact["features"]
        
        # Alinhamento de Colunas (Crucial em ML Produção)
        for col in trained_features:
            if col not in df_predict.columns:
                df_predict[col] = 0
        
        X_pred = df_predict[trained_features].fillna(0)
        
        try:
            probs = model.predict_proba(X_pred)[:, 1]
            df_predict["probabilidade_finalizar"] = probs
        except Exception as e:
            print(f"[IA] Erro na predição: {e}. Usando fallback.")
            df_predict["probabilidade_finalizar"] = 0.5
    else:
        # Fallback se não conseguiu treinar (poucos dados)
        df_predict["probabilidade_finalizar"] = 0.5
        warnings.append("IA em modo básico (dados insuficientes para personalização).")

    # Ordenação e Resposta
    ranked = df_predict.sort_values(by=["probabilidade_finalizar", "metacritic"], ascending=[False, False])

    final_list = []
    for _, row in ranked.head(10).iterrows():
        prob = row.get("probabilidade_finalizar", 0.5)
        final_list.append({
            "appid": int(row["appid"]),
            "name": str(row["name"]),
            "probabilidade_finalizar": round(float(prob) * 100, 1),
            "genero": str(row.get("genero", ""))
        })

    return {
        "recommendations": final_list,
        "warnings": warnings
    }