# GameTrack: Organizador Inteligente de Biblioteca Steam

**Alunos:**  
Gabriel Jose Ferreira Nunes Ribeiro, Pedro Henrique M. Eichler, Wesley Leonardo Jose Costa Filho

---

## 1. Resumo Executivo

O **GameTrack** é uma plataforma web desenvolvida para auxiliar jogadores da Steam a superar a "síndrome do backlog" ou "síndrome do PC gamer". O sistema centraliza a biblioteca de jogos digitais, oferecendo ferramentas avançadas de organização e controle para transformar uma coleção massiva de títulos em uma experiência de lazer organizada e gratificante.

O diferencial do projeto é a combinação de organização de produtividade com um algoritmo de Inteligência Artificial que analisará o perfil e histórico do jogador para gerar recomendações personalizadas, sugerindo quais jogos do seu backlog ele tem maior probabilidade de jugar e finalizar.

---

## 2. Introdução

Este projeto está sendo desenvolvido por uma equipe de estudantes de tecnologia como parte de um trabalho acadêmico multidisciplinar. O mercado atual de jogos digitais, especialmente na Steam, facilita o acúmulo de jogos por meio de promoções, resultando em bibliotecas com centenas de títulos não jogados. Isso leva ao paradoxo da escolha, onde o jogador passa mais tempo decidindo o que jogar do que jogando.

O GameTrack surge como uma ferramenta inteligente e centralizada para transformar essa coleção massiva em uma experiência de lazer mais eficiente e prazerosa.

---

## 3. Problema / Oportunidade

### Problema
O crescimento das bibliotecas digitais gera a "síndrome do backlog" — quando os jogadores acumulam jogos que nunca iniciam, gerando ansiedade e sensação de desperdício. As ferramentas atuais não oferecem recomendações ou insights baseados no comportamento do usuário.

### Oportunidade
Criar uma solução que vai além da organização, oferecendo recomendações inteligentes com base no perfil do jogador, aumentando o engajamento com sua própria biblioteca e otimizando seu tempo de lazer.

---

## 4. Funcionalidades Principais Detalhadas

O GameTrack oferece um ambiente completo para o usuário gerenciar sua biblioteca de jogos e metas relacionadas ao backlog.

### 4.1. Importação e Organização da Biblioteca Steam
- **Importação Automática:** integração com API da Steam para carregar a biblioteca do usuário.
- **Enriquecimento de Dados:** metadados como gênero, desenvolvedor e descrição via Steam Store API.
- **Status de Jogo:** categorização com status como *Não Iniciado*, *Jogando*, *Finalizado*, *Pausado* ou *Abandonado*.

### 4.2. Sistema de Metas e Tarefas
O usuário pode criar metas por jogo, com tipos:
- **TEMPO:** estipular horas estimadas de jogo.
- **CONCLUSÃO:** definir uma data limite (*data_limite*) para finalizar o jogo.

Status das metas: *EM_ANDAMENTO*, *CONCLUIDA* ou *EXPIRADA*.

### 4.3. Recomendação Inteligente
O sistema utiliza algoritmos de classificação para sugerir quais jogos o usuário deve jogar com base em seu perfil e histórico.

---

## 5. Objetivos

### Objetivo Geral
Desenvolver uma aplicação web funcional e intuitiva integrada à API da Steam para organizar bibliotecas de jogos e gerar recomendações inteligentes.

### Objetivos Específicos (SMART)
- **Autenticação:** Integrar com Firebase Authentication. _Prazo: 1º mês._
- **Importação da Biblioteca Steam:** Concluir integração com API da Steam. _Prazo: 1º mês._
- **Modelo de IA:** Treinar modelo de classificação para recomendações. _Prazo: até o 3º mês._
- **Deploy da Aplicação:** Publicar backend e frontend. _Prazo: última semana do projeto._

---

## 6. Escopo do Projeto

### Entregas
- Cadastro e login de usuários
- Dashboard com visualização da biblioteca da Steam
- Alteração manual de status de jogo
- Metas e tarefas de jogatina
- Página de recomendações com IA
- Adição de SteamID de familiares

### Fora do Escopo Inicial
- Integração com outras lojas (Epic, GOG, etc.)

---

## 7. Metodologia e Plano de Ação

Abordagem ágil com entregas incrementais:

| Fase | Atividade | Duração |
|------|-----------|---------|
| Fase 1 | Planejamento e configuração | Semanas 1–2 |
| Fase 2 | Desenvolvimento do core (auth, API Steam) | Semanas 3–8 |
| Fase 3 | IA e funcionalidades adicionais | Semanas 9–12 |
| Fase 4 | Testes, refinamento e deploy | Semanas 13–16 |

---

## 8. Cronograma

| Mês | Atividade Principal |
|-----|---------------------|
| 1   | Setup, Autenticação, API Steam |
| 2   | Dashboard e CRUD de Jogos |
| 3   | Modelo de IA e Família Steam |
| 4   | Testes, Refinamentos e Deploy |

---

## 9. Arquitetura de Desenvolvimento

### 9.1. Backend, Banco e Segurança
- **Framework:** FastAPI (Python)
- **Autenticação:** Firebase Authentication
- **Banco de Dados:** Firestore
- **Estrutura:** Subcoleções `users/{user_id}/games`
- **Otimização:** Escritas em lote com batch

### 9.2. Frontend
- **Framework:** Next.js 16 (App Router)
- **Linguagem:** TypeScript
- **Estilização:** Tailwind CSS (Design Tokens em OKLCH)
- **Tipografia:** Fonte Geist

### 9.3. DevOps
- Controle de versão via GitHub

---

## 10. Modelo de IA e Expansão de Escopo

### 10.1. Implementação da IA
- **Algoritmo:** Modelos de classificação
- **Objetivo:** Recomendar jogos com base nos hábitos do usuário

### 10.2. Expansão Futura
- Suporte a múltiplas plataformas
- Recomendação externa
- Recurso social / Steam Family

---

## 11. Recursos

### Humanos
Equipe acadêmica com desenvolvedores backend, frontend e IA.

### Materiais
- **Hardware:** Computadores pessoais
- **Software:** Python, Node.js, VS Code, Git, Docker
- **Serviços:** GitHub, Firebase, Steam API, Vercel

### Financeiros
- **Custo estimado:** R$ 0,00 (camadas gratuitas dos serviços)

