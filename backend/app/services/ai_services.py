import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer 
from fastapi import HTTPException
from typing import List, Dict, Any
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.svm import SVC

from ..models import game_model  
from ..schemas.game_schema import GameStatus, InteresseNivel

def get_model(model_type: str = "logistic"):
    if model_type == "random_forest":
        return RandomForestClassifier(
            n_estimators=100, 
            class_weight="balanced", 
            random_state=42,
            max_depth=10
        )
    
    elif model_type == "xgbo ost":
        return XGBClassifier(
            use_label_encoder=False,
            eval_metric="logloss",
            scale_pos_weight=5,
            random_state=42
        )
    
    elif model_type == "knn":
        return KNeighborsClassifier(
            n_neighbors=5,
            weights="distance",
        )
    
    elif model_type == "svm":
        return SVC(
            kernel="rbf",
            probability=True,
            random_state=42,
           class_weight="balanced" 
        )
    
    else:
        return LogisticRegression(
            solver="liblinear",
            class_weight="balanced",
            random_state=42
        )
    

def analyze_data_coverage(games_list: list) -> List[str]:
    df = pd.DataFrame(games_list)
    warnings = []

    if "status" not in df.columns:
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
            f"{pct}% dos jogos no backlog estão com Nível de Interesse 'N/A'. "
            "Defina Baixo, Médio ou Alto para melhorar as recomendações."
        )

    nota_na = jogos_nao_iniciados[
        (jogos_nao_iniciados["nota_pessoal"].isnull()) |
        (jogos_nao_iniciados["nota_pessoal"] == 0)
    ]

    if len(nota_na) > 0:
        pct = round(len(nota_na) / total * 100)
        warnings.append(
            f"{pct}% dos jogos no backlog estão sem Nota Pessoal (0). "
            "Avalie de 1 a 10 para enriquecer o modelo."
        )

    return warnings


def prepare_data_for_ai(games_list: list) -> pd.DataFrame | None:
    if not games_list or len(games_list) < 10:
        return None

    df = pd.DataFrame(games_list)

    if "status" not in df.columns:
        return None

    df["target_finalizado"] = df["status"].apply(
        lambda x: 1 if x == GameStatus.finalizado.value else 0
    )

    df["playtime_forever"] = df.get("playtime_forever", 0).fillna(0)
    df["log_playtime"] = df["playtime_forever"].apply(lambda x: np.log1p(x))

    df["nota_pessoal"] = df.get("nota_pessoal", 0).fillna(0)

    df["metacritic"] = df.get("metacritic", 0).fillna(0)

    df["genero"] = df.get("genero", "").fillna("")
    df["genero_list"] = df["genero"].astype(str).str.split(", ")

    mlb_gen = MultiLabelBinarizer()
    genero_bin = mlb_gen.fit_transform(df["genero_list"])
    genero_df = pd.DataFrame(genero_bin, columns=[f"gen_{g}" for g in mlb_gen.classes_])

    df["categorias"] = df.get("categorias", "").fillna("")
    df["categoria_list"] = df["categorias"].astype(str).str.split(", ")

    mlb_cat = MultiLabelBinarizer()
    cat_bin = mlb_cat.fit_transform(df["categoria_list"])
    categoria_df = pd.DataFrame(cat_bin, columns=[f"cat_{c}" for c in mlb_cat.classes_])

    df["interesse"] = df.get("interesse", "N/A").fillna("N/A")
    interesse_map = {"N/A": 0, "Baixo": 1, "Médio": 2, "Alto": 3}
    df["nivel_interesse_numerico"] = df["interesse"].map(interesse_map).fillna(0)

    meses_pt_en = {
        "jan.": "Jan", "fev.": "Feb", "mar.": "Mar", "abr.": "Apr",
        "mai.": "May", "jun.": "Jun", "jul.": "Jul", "ago.": "Aug",
        "set.": "Sep", "out.": "Oct", "nov.": "Nov", "dez.": "Dec"
    }

    def limpar_e_converter_data(data_str: str):
        if not isinstance(data_str, str) or not data_str.strip():
            return pd.NaT

        data_lower = data_str.lower()
        
        for pt, en in meses_pt_en.items():
            if pt in data_lower:
                data_lower = data_lower.replace(pt, en)
                break

        return pd.to_datetime(data_lower, errors="coerce")

    def calcular_idade_lancamento(data_str: str) -> int:
        date_obj = limpar_e_converter_data(data_str)
        
        if pd.isna(date_obj):
            return 0
            
        return (datetime.now() - date_obj).days

    df["idade_lancamento_dias"] = df.get("data_lancamento", "").apply(calcular_idade_lancamento)
    

    def extract_log_final_price(price_data):
        if isinstance(price_data, dict):
            price_raw = price_data.get("preco_final")
            if isinstance(price_raw, (int, float)):
                return np.log1p(price_raw / 100)
        return 0

    df["log_final_price"] = df.get("preco", None).apply(extract_log_final_price)

    df = pd.concat([df.reset_index(drop=True), genero_df, categoria_df], axis=1)

    numeric_features = [
        "log_playtime",
        "nota_pessoal",
        "metacritic",
        "nivel_interesse_numerico",
        "idade_lancamento_dias",
        "log_final_price"
    ]

    feature_cols = [
        col for col in df.columns
        if col.startswith("gen_") or col.startswith("cat_") or col in numeric_features
    ]

    required = ["name", "target_finalizado", "appid", "status", "genero"]
    for col in required:
        if col not in df.columns:
            df[col] = None

    df_final = df[feature_cols + required].fillna(0)

    return df_final.copy()



def generate_recommendations(user_id: str) -> Dict[str, Any]:
    
    games_list = game_model.get_user_games(user_id)
    warnings = analyze_data_coverage(games_list)

    processed_df = prepare_data_for_ai(games_list)

    if processed_df is None or processed_df[processed_df["status"] == GameStatus.nao_iniciado.value].empty:
        raise HTTPException(status_code=404, detail="Dados insuficientes para IA.")

    df_train = processed_df[processed_df["status"] != GameStatus.nao_iniciado.value]
    df_predict = processed_df[processed_df["status"] == GameStatus.nao_iniciado.value]

    if df_train.empty:
        raise HTTPException(status_code=400, detail="Você precisa jogar alguns jogos para treinar a IA.")

    train_features = [
        col for col in processed_df.columns
        if col.startswith("gen_")
        or col.startswith("cat_")
        or col in [
            "log_playtime",
            "nota_pessoal",
            "metacritic",
            "nivel_interesse_numerico",
            "idade_lancamento_dias",
            "log_final_price"
        ]
    ]

    X_train = df_train[train_features]
    y_train = df_train["target_finalizado"]

    unique_classes = np.unique(y_train)

    df_predict = df_predict.copy()

    if len(unique_classes) < 2:
        df_predict["probabilidade_finalizar"] = 0.5

    else:
        model = get_model("random_forest")  # Opções: "logistic", "random_forest", "xgboost", "knn", "svm"

    try:
        model.fit(X_train, y_train)
        
        preds_train = model.predict(X_train)
        print(f"Acurácia no Treino ({type(model).__name__}): {accuracy_score(y_train, preds_train):.2f}")

        X_pred = df_predict[train_features].reindex(columns=train_features, fill_value=0)
        
        df_predict["probabilidade_finalizar"] = model.predict_proba(X_pred)[:, 1]

    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Erro no modelo IA: {e}")

    ranked = df_predict.sort_values(by="probabilidade_finalizar", ascending=False)

    final_list = []
    for _, row in ranked.head(10).iterrows():
        final_list.append({
            "appid": int(row["appid"]),
            "name": str(row["name"]),
            "probabilidade_finalizar": round(float(row["probabilidade_finalizar"]) * 100, 2),
            "genero": str(row["genero"])
        })

    return {
        "recommendations": final_list,
        "warnings": warnings
    }
