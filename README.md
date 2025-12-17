# 🎮 GameTrack: Organizador Inteligente de Biblioteca Steam

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-Auth-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)

> **GameTrack** é uma plataforma Full Stack que ajuda jogadores a vencerem a "**Síndrome do Backlog**" ou "**Síndrome do PC Gamer**" integrando diretamente com a Steam API e utilizando IA para recomendar o próximo jogo.

---

## 📸 Screenshots

|  Biblioteca | Detalhes do Jogo |
|:---:|:---:|
| ![Biblioteca](./assets/dashboard.png) | ![Game Details](./assets/details.png) |

---

## 🚀 Sobre o Projeto

Desenvolvido como projeto final de semestre acadêmico, o GameTrack resolve o paradoxo da escolha enfrentado por gamers com bibliotecas imensas.

**Principais Diferenciais:**
* **Integração Real:** Conecta com a conta Steam do usuário para puxar jogos e conquistas automaticamente.
* **Recomendação via IA:** Algoritmo (XGBoost/Scikit-learn) que analisa o perfil de jogo para sugerir títulos com maior probabilidade de finalização.
* **Gestão de Metas:** Defina prazos ou metas de horas para "zerar" seus jogos.

---

## 🛠️ Tecnologias Utilizadas

### Backend
* **Linguagem:** Python
* **Framework:** FastAPI
* **Banco de Dados/Auth:** Firebase (Firestore & Authentication)
* **IA & Dados:** XGBoost, Scikit-learn, Pandas, Numpy
* **Validação:** Pydantic

### Frontend
* **Framework:** React.js (v18)
* **Estilização:** Bootstrap 5
* **Roteamento:** React Router Dom
* **Requisições:** Axios
* **Notificações:** React Toastify

### DevOps
* **Containerização:** Docker & Docker Compose

---

## ⚙️ Como Executar

Você pode rodar o projeto via Docker (recomendado) ou manualmente.

### Pré-requisitos
* Git
* Docker (Opcional, mas recomendado)
* Python 3.8+ e Node.js (Para execução manual)
* **Configuração de Ambiente:** Crie um arquivo `.env` na pasta `backend/` com as credenciais do Firebase e chave da API Steam.

### Opção 1: Via Docker (Rápido)
Como o projeto já possui orquestração configurada, basta rodar:

```bash
# Na raiz do projeto
docker-compose up --build
````

### Opção 2: Execução Manual

Backend

```bash
cd backend
# Criar ambiente virtual
python -m venv venv
# Ativar venv (Windows)
.\venv\Scripts\Activate
# Linux/Mac: source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar servidor
uvicorn app.main:app --reload
````
Frontend

```bash
cd Frontend
# Instalar dependências
npm install
# Iniciar aplicação
npm start
````

## 📂 Estrutura do Projeto
```bash
GameTrackWeb/
├── backend/            # API FastAPI e Lógica de IA
│   ├── app/
│   │   ├── routers/    # Rotas (Auth, Games, Steam, Recomendações)
│   │   ├── services/   # Regras de negócio e integração externa
│   │   └── models/     # Modelos Pydantic e Schemas
│   ├── requirements.txt
│   └── Dockerfile
├── Frontend/           # Aplicação React
│   ├── src/
│   │   ├── components/ # Componentes (GameCard, Navbar, etc.)
│   │   ├── pages/      # Telas (Biblioteca, Metas, Login)
│   │   └── services/   # Consumo da API (Axios)
│   └── package.json
└── docker-compose.yml  # Orquestração dos containers
````

## 👥 Autores
- Gabriel Jose Ferreira Nunes Ribeiro
- Pedro Henrique M. Eichler
- Wesley Leonardo Jose Costa Filho
