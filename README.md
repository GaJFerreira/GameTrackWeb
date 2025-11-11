# GameTrack: Organizador Inteligente de Biblioteca Steam

**Alunos:**  
Gabriel Jose Ferreira Nunes Ribeiro, Pedro Henrique M. Eichler, Wesley Leonardo Jose Costa Filho

---

## 1. Resumo Executivo

O projeto **GameTrack** consiste no desenvolvimento de uma plataforma web para auxiliar jogadores da plataforma **Steam** a gerenciar suas extensas bibliotecas de jogos digitais.

Utilizando uma arquitetura moderna com **backend em Python**, **frontend em Next.js** e **banco de dados e autenticação providos pelo Firebase**, o sistema permitirá que os usuários importem seus jogos, organizem-nos por status e interesse, e planejem suas sessões de jogatina.

O diferencial do projeto é a aplicação de um **algoritmo de Inteligência Artificial** que analisará o perfil e histórico do jogador para gerar recomendações personalizadas, sugerindo quais jogos do seu backlog ele tem maior probabilidade de jogar e finalizar — combatendo assim a *"síndrome do backlog"*.

---

## 2. Introdução

Este projeto está sendo desenvolvido por uma equipe de estudantes de tecnologia como parte de um trabalho acadêmico multidisciplinar.

A situação atual do mercado de jogos digitais, especialmente na plataforma Steam, é caracterizada pelo fácil acúmulo de jogos através de promoções, resultando em bibliotecas com centenas de títulos não jogados. Essa abundância gera um **paradoxo de escolha**, onde o jogador passa mais tempo decidindo o que jogar do que efetivamente jogando.

O **GameTrack** nasce da necessidade de uma ferramenta inteligente e centralizada para transformar essa coleção massiva de jogos em uma experiência de lazer organizada e gratificante.

---

## 3. Problema / Oportunidade

**Problema:**  
O crescimento exponencial de bibliotecas de jogos digitais leva a um fenômeno conhecido como *"síndrome do backlog"* ou *"síndrome do PC gamer"*. Jogadores acumulam dezenas ou centenas de jogos que nunca iniciam, gerando ansiedade, sensação de desperdício financeiro e dificuldade de organização. Ferramentas atuais de gerenciamento são, em sua maioria, manuais e não oferecem insights sobre qual jogo priorizar com base no comportamento do usuário.

**Oportunidade:**  
Existe a oportunidade de criar uma solução que não apenas organiza, mas também **guia o usuário de forma inteligente**. Ao aplicar IA para analisar o perfil do jogador (gêneros preferidos, jogos finalizados, tempo de jogo), o **GameTrack** pode oferecer recomendações proativas e personalizadas, aumentando o engajamento do usuário com sua própria biblioteca e otimizando seu tempo de lazer.

---

## 4. Objetivos

### Objetivo Geral
Desenvolver uma aplicação web funcional e intuitiva que se integre à **API da Steam** para organizar bibliotecas de jogos e fornecer recomendações inteligentes baseadas em IA para ajudar os usuários a gerenciar seu backlog.

### Objetivos Específicos (Metodologia SMART)

- **Autenticação:**  
  - **Específico:** Desenvolver um sistema de autenticação de usuários seguro utilizando o Firebase Authentication.  
  - **Mensurável:** Permitir cadastro, login e gerenciamento de sessão de usuários.  
  - **Alcançável:** A tecnologia do Firebase é bem documentada e adequada para este fim.  
  - **Relevante:** Essencial para a personalização e segurança dos dados.  
  - **Temporal:** Concluir até o final do **1º mês** de desenvolvimento.

- **Importação da Biblioteca Steam:**  
  - **Específico:** Implementar a funcionalidade de importação automática da biblioteca via API da Steam.  
  - **Mensurável:** Exibir corretamente a lista de jogos após fornecer o SteamID64.  
  - **Alcançável:** A API da Steam fornece os endpoints necessários.  
  - **Relevante:** Funcionalidade central para alimentação de dados.  
  - **Temporal:** Concluir até o final do **1º mês**.

- **Modelo de IA:**  
  - **Específico:** Criar um modelo de classificação para prever a probabilidade de o usuário finalizar um jogo do backlog.  
  - **Mensurável:** Gerar uma lista ordenada de jogos recomendados.  
  - **Alcançável:** Utilizando Python e Scikit-learn com os dados coletados.  
  - **Relevante:** Principal diferencial da plataforma.  
  - **Temporal:** Desenvolver e integrar até o final do **3º mês**.

- **Deploy da Aplicação:**  
  - **Específico:** Realizar o deploy do backend e frontend em ambiente de nuvem.  
  - **Mensurável:** A aplicação deve estar acessível publicamente via URL.  
  - **Alcançável:** Usando Vercel (frontend) e Render/Heroku (backend).  
  - **Relevante:** Entrega final do projeto funcional.  
  - **Temporal:** Concluir na **última semana do projeto**.

---

## 5. Escopo do Projeto

### Entregas

- Aplicação web responsiva com cadastro e login de usuários.  
- Painel de usuário para visualização da biblioteca importada da Steam.  
- Funcionalidade para alterar o status de cada jogo (*"Quero Jogar"*, *"Jogando"*, *"Finalizado"*, *"Abandonado"*).  
- Página de recomendações com lista priorizada pela IA.  
- Funcionalidade para adicionar manualmente o SteamID de membros da família.

### Limites do Projeto (Não incluído no escopo)

- Integração com outras lojas (Epic Games, GOG, etc.).  
- Funcionalidades sociais (amigos, chat, fóruns).  
- Lançamento de jogos pela plataforma.  
- Sincronização de dados em tempo real (atualizações sob demanda).

---

## 6. Metodologia e Plano de Ação

O projeto seguirá uma abordagem **ágil**, dividida em fases com entregas incrementais.

### Fase 1 – Planejamento e Estruturação (Semanas 1–2)
- Definição da arquitetura.  
- Design do banco no Firestore.  
- Configuração do ambiente (Python/Next.js).  
- Criação do projeto no Firebase.

### Fase 2 – Desenvolvimento do Core (Semanas 3–8)
- Implementação da autenticação.  
- Integração com a API da Steam.  
- Desenvolvimento das telas principais do frontend.

### Fase 3 – IA e Funcionalidades Adicionais (Semanas 9–12)
- Coleta e tratamento de dados para o modelo de IA.  
- Treinamento do algoritmo e criação do endpoint de recomendação.  
- Implementação da funcionalidade *"Família Steam"*.

### Fase 4 – Testes, Refinamento e Deploy (Semanas 13–16)
- Testes integrados.  
- Ajustes de UI/UX.  
- Configuração de CI/CD (GitHub Actions).  
- Deploy final.

---

## 7. Cronograma

| Fase | Atividade Principal | Duração Estimada |
|------|---------------------|------------------|
| **Mês 1** | Planejamento, Configuração de Ambiente, Autenticação e API Steam | 4 semanas |
| **Mês 2** | Desenvolvimento do Dashboard e CRUD de Jogos (Frontend/Backend) | 4 semanas |
| **Mês 3** | Desenvolvimento e Treinamento do Modelo de IA, Feature "Família Steam" | 4 semanas |
| **Mês 4** | Testes Finais, Refinamentos e Deploy da Aplicação | 4 semanas |

---

## 8. Recursos

### Recursos Humanos
- Equipe acadêmica com desenvolvedores para **backend**, **frontend** e **IA**.

### Recursos Materiais
- **Hardware:** Computadores pessoais para desenvolvimento.  
- **Software:** Python, Node.js, VS Code, Git, Docker (opcional).  
- **Serviços/Contas:** GitHub, Google (Firebase), API Steam, Vercel.

### Recursos Financeiros (Estimativa)
- **Custo Estimado:** R$ 0,00  
  O projeto será desenvolvido utilizando camadas gratuitas (*free tier*) dos serviços necessários (Firebase Spark Plan, Vercel Hobby, etc.), suficientes para o escopo acadêmico.

---
****
