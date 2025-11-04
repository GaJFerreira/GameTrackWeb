# GameTrack (Python/FastAPI)

Port do projeto Android/Java para uma API Python usando FastAPI + SQLite.

## Rodar

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt

# cria o banco e sobe
uvicorn app.main:app --reload
```

Abre em: `http://127.0.0.1:8000/docs`

## Endpoints principais

- `POST /auth/register` — cria usuário
- `POST /auth/login` — retorna JWT
- `GET /jogos/` — lista jogos (requer Bearer Token)
- `POST /jogos/` — cria jogo
- `PUT /jogos/{id}` — atualiza jogo
- `DELETE /jogos/{id}` — remove jogo
- `GET /metas/` — lista metas
- `POST /metas/` — cria meta
- `PUT /metas/{id}` — atualiza meta
- `DELETE /metas/{id}` — remove meta

## Modelo de dados (simplificado)

- **Usuario**: id, nome, email, senha_hash
- **Jogo**: id, titulo, plataforma, horas_jogadas, status, owner_id (FK Usuario)
- **Meta**: id, descricao, concluida, data_limite, jogo_id (FK Jogo), owner_id (FK Usuario)

## Notas

- JWT simples com expiração de 2h
- `sqlite:///./gametrack.db` no diretório raiz
- Sem migrações (usa `create_all` na primeira execução)
