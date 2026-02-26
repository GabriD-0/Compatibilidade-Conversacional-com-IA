# Checklist — Compatibilidade Conversacional com IA

Checklist completo baseado no documento do projeto. Use `[ ]` para pendente e `[x]` para concluído.

---

## Capa

- [x] **Título do Projeto** definido: Compatibilidade Conversacional com IA
- [x] **Nome do Estudante** preenchido: Gabriel de Oliveira
- [x] **Curso** preenchido: Engenharia de Software
- [x] **Data de Entrega** definida: 02/12/2025
- [x] Logo da instituição (images/instituicao_logo.png) presente

---

## Resumo

- [ ] Resumo redigido e alinhado aos objetivos
- [ ] Menção às três dimensões: LSM, sentimentos, sinais comportamentais
- [ ] Menção à API REST, banco relacional, protótipo (chat + dashboard)
- [ ] Menção à LGPD e transparência

---

## 1. Introdução

### Contexto

- [ ] Contexto descrito (plataformas digitais, comunicação textual)
- [ ] Noção de compatibilidade conversacional explicada
- [ ] Oportunidades (pareamento, redução de atritos, decisões) mencionadas

### Justificativa

- [ ] Crítica a perfis estáticos/questionários extensos
- [ ] Diálogos reais como fonte de dados justificada
- [ ] Explicabilidade e transparência citadas
- [ ] Boas práticas de IA responsável mencionadas

### Objetivos

- [ ] **Objetivo Geral**: sistema de IA para score de compatibilidade conversacional
- [ ] **Objetivo Específico 1**: módulo LSM em português (palavras-função)
- [ ] **Objetivo Específico 2**: análise de sentimentos em PT-BR (polaridade, intensidade, convergência)
- [ ] **Objetivo Específico 3**: sinais comportamentais (latência, equilíbrio de turnos, comprimento)
- [ ] **Objetivo Específico 4**: agregação heurística em score único
- [ ] **Objetivo Específico 5**: API REST + protótipo (chat + dashboard)
- [ ] **Objetivo Específico 6**: conformidade com LGPD (consentimento, anonimização, minimização, exclusão)

---

## 2. Descrição do Projeto

### Linha e Tema

- [x] **Linha de Projeto**: Projetos com IA
- [x] **Tema do Projeto**: sistema de IA para índice de compatibilidade conversacional

### Propósito e Uso Prático

- [ ] Inserir e visualizar conversas (chat, mensagens por participante e timestamp)
- [ ] Obter análise de compatibilidade (score + explicações)
- [ ] Visualizar métricas e insights (dashboard, distribuições, comparações)
- [ ] Integrar via API (sistemas externos)
- [ ] Problema de pareamento/avaliação objetiva descrito

### Público-Alvo

- [ ] Gestores de equipes e líderes de projetos
- [ ] Plataformas de atendimento ao cliente e contact centers
- [ ] Plataformas de relacionamento e mentoria
- [ ] Pesquisadores e analistas de comunicação

### Problemas a Resolver

- [ ] Dificuldade em medir compatibilidade comunicativa de forma objetiva
- [ ] Pareamento baseado só em perfis estáticos
- [ ] Ausência de ferramentas com score unificado e explicável
- [ ] Pouca transparência em sistemas de IA para interações humanas

### Diferenciação/Ineditismo

- [ ] Foco em compatibilidade conversacional (não só sentimentos)
- [ ] LSM adaptado para português
- [ ] Três dimensões (estilo, sentimento, comportamento) em score único com explicações
- [ ] Arquitetura API-first

### Limitações

- [ ] Apenas conversas textuais em PT-BR (sem áudio, vídeo, imagens, figurinhas, outros idiomas)
- [ ] Não avalia conteúdo temático profundo
- [ ] Qualidade dependente de quantidade/qualidade dos dados
- [ ] Protótipo funcional, não necessariamente em escala comercial
- [ ] Modelo supervisionado condicionado a dados rotulados (possível abordagem heurística inicial)

### Normas e Legislações Aplicáveis

- [ ] LGPD (Lei nº 13.709/2018)
- [ ] Normas e boas práticas de segurança (ex.: ISO/IEC 27001)
- [ ] Diretrizes éticas em IA (UNESCO, OECD)
- [ ] Boas práticas de acessibilidade (ex.: WCAG)

### Métricas de Sucesso

#### Qualidade do Score

- [ ] Concordância com avaliação humana (classificação baixa/média/alta)
- [ ] Coerência relativa entre diálogos (ordenação “faz sentido”)
- [ ] Comportamento das métricas parciais (LSM, sentimentos, sinais comportamentais)

#### Desempenho Técnico

- [ ] Tempo de resposta da API ≤ 3 segundos
- [ ] Confiabilidade básica (ausência de erros críticos)
- [ ] Uso de recursos (CPU, memória) observado

#### Uso e Adoção

- [ ] Número de diálogos analisados
- [ ] Número de usuários/contextos atendidos
- [ ] Frequência de uso (análises por usuário/sessão)

#### Usabilidade e Conformidade

- [ ] Satisfação com o protótipo (escala 1–5)
- [ ] Percepção de justiça e transparência
- [ ] Aspectos de privacidade e LGPD (compreensão, exclusão, ausência de incidentes)

---

## 3. Especificação Técnica

### 3.1. Requisitos de Software

#### Requisitos Funcionais (RF)

- [ ] **RF01**: API REST recebe diálogos (mensagens, autor, timestamps)
- [ ] **RF02**: Pré-processamento (normalização, tokenização, autor) para português
- [ ] **RF03**: Cálculo do índice LSM entre participantes
- [ ] **RF04**: Análise de sentimentos em PT-BR por mensagem e agregada
- [ ] **RF05**: Extração de sinais comportamentais (latência, equilíbrio de turnos, comprimento)
- [ ] **RF06**: Combinação em score unificado de compatibilidade conversacional
- [ ] **RF07**: Sumário explicável com fatores que influenciaram o score
- [ ] **RF08**: Estratégia heurística de agregação; arquitetura permite modelo supervisionado futuro
- [ ] **RF09**: Armazenamento em PostgreSQL (conversas/scores/métricas, versionamento)
- [ ] **RF10**: Interface de chat para inserção e visualização de diálogos
- [ ] **RF11**: Dashboard com métricas agregadas (distribuição, top-N, explicabilidade)
- [ ] **RF12**: Mecanismos de exclusão de dados (LGPD)

#### Requisitos Não-Funcionais (RNF)

- [ ] **RNF01**: API com tempo de resposta adequado ao uso interativo
- [ ] **RNF02**: HTTPS e acesso autenticado/autorizado
- [ ] **RNF03**: UX do chat e dashboard (visual limpo, feedbacks, textos explicativos)
- [ ] **RNF04**: Arquitetura permite horizontalização dos serviços de cálculo
- [ ] **RNF05**: Execução em ambiente local e em contêiner
- [ ] **RNF06**: Código modular, documentado e versionado
- [ ] **RNF07**: Logs mínimos para auditoria, sem dados sensíveis desnecessários
- [ ] **RNF08**: Pseudonimização/anonimização; exclusão conforme LGPD; consentimento explícito

#### Representação dos Requisitos

- [ ] Diagrama de Casos de Uso (UML) com atores e fluxos
- [ ] Diagrama de fluxo de consentimento e exclusão de dados (LGPD)
- [ ] Imagem diagrama_casos_uso.png
- [ ] Imagem diagrama_fluso_lgpd.png

#### Aderência à Linha de Projeto (IA)

- [ ] Uso de técnicas de IA (sentimentos, LSM, agregação heurística)
- [ ] API REST para consumo do serviço
- [ ] Questões éticas, viés e privacidade consideradas
- [ ] Monitoramento de desempenho do modelo (métricas, logs de erros)

### 3.2. Considerações de Design

#### Arquitetura em Camadas

- [x] Camada de Apresentação (frontend Vue.js: chat + dashboard)
- [x] Camada de Serviços/API (Flask, endpoints REST)
- [x] Camada Motor de IA (pré-processamento, LSM, sentimentos, sinais, agregação)
- [x] Camada de Persistência (PostgreSQL)

#### Padrões de Arquitetura

- [x] Arquitetura em camadas (apresentação, negócio, dados)
- [x] API-first no backend
- [x] Vue.js no frontend (componentes, composables, separação de responsabilidades)

#### Modelos C4

- [ ] C4 Nível 1 – Diagrama de Contexto do Sistema (c4_nivel1_contexto.png)
- [ ] C4 Nível 2 – Diagrama de Contêineres (c4_nivel2_conteineres.png)
- [ ] C4 Nível 3 – Diagrama de Componentes (c4_nivel3_componentes.png)
- [ ] C4 Nível 4 – Diagrama de Código (c4_nivel4_codigo.png)

#### Mockups

- [ ] Tela de Chat (Figma ou similar)
- [ ] Dashboard de Métricas (gráficos, top-N, explicabilidade por par)
- [ ] Tela de Configurações/Administrativo (quando aplicável)
- [ ] Validação de acessibilidade (WCAG) nos mockups

#### Decisões e Alternativas

- [x] Flask justificado (FastAPI considerado)
- [x] PostgreSQL justificado
- [x] Abordagem heurística inicial com evolução para supervisionado
- [x] Aplicação web responsiva (não app mobile nativo)

#### Critérios de Escalabilidade, Resiliência e Segurança

- [ ] Contêineres para backend
- [ ] Possibilidade de motor de IA como serviço independente
- [ ] Tratamento de erros robusto (mensagens ao usuário, logs estruturados)
- [ ] Boas práticas de segurança adotadas

### 3.3. Stack Tecnológica

#### Linguagens

- [x] Python (backend, motor de IA, pré-processamento, métricas)
- [x] TypeScript (frontend)

#### Frameworks e Bibliotecas

- [x] Flask para API REST
- [ ] Bibliotecas de NLP em português (a definir)
- [x] Vue.js para frontend
- [ ] Bibliotecas de visualização para dashboard
- [x] SQLAlchemy como ORM para PostgreSQL

#### Ferramentas

- [x] Git + GitHub para versionamento
- [x] VS Code como IDE
- [x] Documentação em Markdown e diagramas UML/C4

#### Licenciamento

- [x] Licença MIT do projeto
- [ ] Verificação de licenças de modelos e bibliotecas de NLP

### 3.4. Considerações de Segurança

#### Riscos

- [ ] Vazamento de dados sensíveis das conversas
- [ ] Acesso não autorizado à API ou ao banco
- [ ] Armazenamento excessivo de dados pessoais
- [ ] Vieses nos modelos gerando scores injustos

#### Medidas de Mitigação

- [ ] Criptografia em trânsito (HTTPS/TLS)
- [ ] Controles de acesso (autenticação e autorização)
- [ ] Minimização de dados; anonimização/pseudonimização
- [ ] Políticas de retenção de dados
- [ ] Monitoramento de logs para acessos anômalos
- [ ] Análise crítica dos modelos para mitigar vieses

#### Normas e Boas Práticas

- [ ] OWASP Top 10
- [ ] ISO/IEC 27001 (princípios)
- [ ] LGPD (Lei nº 13.709/2018)
- [ ] Princípios de IA Responsável (UNESCO, OECD)
- [ ] Desenvolvimento seguro (validação, sanitização, parâmetros preparados, tratamento de erros)

#### Responsabilidade Ética

- [ ] Clareza de que o score é estimativa probabilística
- [ ] Evitar uso em cenários de alto risco sem avaliação ética/técnica
- [ ] Documentação de limitações e potenciais vieses
- [ ] Possibilidade de explicações adicionais e exclusão de dados

### 3.5. Conformidade e Normas Aplicáveis

#### LGPD

- [ ] Princípio da Finalidade
- [ ] Princípio da Necessidade
- [ ] Princípio da Transparência (política de privacidade)
- [ ] Consentimento explícito (com revogação)
- [ ] Direitos dos titulares (Art. 18: acesso, correção, exclusão, portabilidade, revisão)
- [ ] Anonimização e pseudonimização
- [ ] Segurança e prevenção
- [ ] Retenção de dados (prazos, anonimização/exclusão)

#### OWASP Top 10

- [ ] Diretrizes aplicadas (validação, injeção, autenticação, dados sensíveis, configuração)

#### IA Responsável (UNESCO e OECD)

- [ ] Transparência e explicabilidade
- [ ] Justiça e não discriminação
- [ ] Responsabilidade humana
- [ ] Privacidade e proteção de dados (privacy by design, LGPD)
- [ ] Robustez e segurança

#### WCAG

- [ ] Diretrizes de acessibilidade (nível AA como referência)
- [ ] Contraste, navegação por teclado, leitores de tela, textos alternativos, estrutura semântica

---

## 3.6. Desenvolvimento (Backend Flask + Frontend Vue.js)

Seção dedicada às tarefas de implementação do backend (Flask) e do frontend (Vue.js). Itens já definidos/em acordo com o documento estão marcados com [x].

### Backend (Flask)

#### Projeto e ambiente

- [x] Stack definida: Python + Flask + SQLAlchemy + PostgreSQL
- [ ] Estrutura de pastas do backend (rotas, serviços, modelos, motor de IA)
- [ ] Ambiente virtual Python (venv ou similar) e `requirements.txt`
- [ ] Variáveis de ambiente para banco e configurações (.env / config)
- [ ] Aplicação Flask inicial com blueprint ou módulos

#### API REST (Flask)

- [ ] Endpoint para receber diálogos (ex.: `POST /api/v1/dialogos` ou equivalente)
- [ ] Endpoint para obter score e métricas (ex.: `GET /api/v1/dialogos/{id}/score`)
- [ ] Endpoint para listar diálogos/analises (ex.: `GET /api/v1/dialogos`)
- [ ] Endpoint de exclusão de dados (LGPD) (ex.: `DELETE /api/v1/dados/{identificador}`)
- [ ] Validação de entrada (mensagens, autor, timestamps) e códigos de erro adequados
- [ ] Respostas em JSON padronizado (score, métricas, explicabilidade)
- [ ] CORS configurado para o frontend Vue.js
- [ ] Documentação da API (OpenAPI/Swagger ou README com exemplos)

#### Persistência (PostgreSQL + SQLAlchemy)

- [ ] Conexão e configuração do PostgreSQL
- [ ] Modelos SQLAlchemy: conversas/diálogos, mensagens, scores, métricas
- [ ] Versionamento dos cálculos e histórico de análises (RF09)
- [ ] Migrações (Alembic ou equivalente) para esquema do banco

#### Motor de IA (integração no backend)

- [ ] Módulo de pré-processamento chamado pela API (normalização, tokenização, autor)
- [ ] Módulo LSM integrado ao fluxo de análise
- [ ] Módulo de análise de sentimentos (PT-BR) integrado
- [ ] Módulo de sinais comportamentais integrado
- [ ] Módulo de agregação (heurística → score único)
- [ ] Módulo de explicabilidade (sumário de fatores) integrado à resposta da API

#### Qualidade e operação (backend)

- [ ] Tratamento de erros centralizado (mensagens claras, logs estruturados)
- [ ] Logs mínimos para auditoria, sem dados sensíveis (RNF07)
- [ ] Testes unitários e/ou de integração para endpoints e motor de IA
- [ ] Execução em ambiente local e em contêiner (Docker) (RNF05)

### Frontend (Vue.js)

#### Projeto e ambiente

- [x] Stack definida: Vue.js
- [ ] Projeto Vue criado (Vite ou Vue CLI) com estrutura de pastas
- [ ] Configuração para consumir a API do backend (URL base, ambiente dev/prod)
- [ ] Gerenciamento de estado (Pinia ou Vuex) se necessário para chat/dashboard
- [ ] Roteamento (Vue Router) para Chat, Dashboard e demais telas

#### Interface de Chat (RF10)

- [ ] Tela/rota de Chat para inserção de diálogos
- [ ] Formulário/área para mensagens (autor, texto, timestamp)
- [ ] Listagem/visualização das mensagens por participante e ordem temporal
- [ ] Ação de envio do diálogo para a API e exibição do score + explicações
- [ ] Indicador de carregamento e tratamento de erro na chamada à API
- [ ] Layout responsivo e feedbacks claros (RNF03)

#### Dashboard (RF11)

- [ ] Tela/rota de Dashboard
- [ ] Visualização da distribuição de scores (gráfico)
- [ ] Lista ou cards de top-N pares / análises
- [ ] Visualização detalhada por par (métricas, barras estilo/sentimento/comportamento, explicabilidade)
- [ ] Integração com endpoints da API para listar e detalhar análises
- [ ] Bibliotecas de gráficos integradas (ex.: Chart.js, ApexCharts)

#### Integração e UX

- [ ] Cliente HTTP (axios ou fetch) configurado para a API Flask
- [ ] Tratamento de erros e feedback ao usuário em todas as telas
- [ ] Textos explicativos sobre o significado do score e das métricas (RNF03)
- [ ] Acessibilidade (WCAG): contraste, teclado, estrutura semântica

#### Qualidade (frontend)

- [ ] Código modular: componentes reutilizáveis, composables onde fizer sentido
- [ ] Documentação ou comentários nos componentes principais
- [ ] Testes (unitários ou e2e) para fluxos críticos (envio de diálogo, exibição do score)

### Integração Backend + Frontend

- [ ] Frontend Vue.js consome apenas a API Flask (sem lógica de negócio duplicada)
- [ ] Fluxo completo: inserir diálogo no Chat → API processa → exibir score e explicabilidade
- [ ] Fluxo Dashboard: carregar listagem e detalhes a partir da API
- [ ] Ambiente de desenvolvimento: backend e frontend rodando e comunicando (localhost)

---

## 4. Próximos Passos

### 4.1. Portfólio I (Planejamento e Fundamentos)

#### Refinamento de Requisitos e Planejamento

- [ ] Revisão e detalhamento de RF01–RF12 e RNF01–RNF08
- [ ] Casos de uso detalhados e cenários de teste
- [ ] Critérios de aceitação por funcionalidade
- [ ] Estratégia de coleta e validação de dados

#### Modelagem e Arquitetura

- [ ] Diagrama de Casos de Uso (UML)
- [ ] Diagramas C4 (Contexto, Contêineres, Componentes, Código se necessário)
- [ ] Modelagem do banco (esquema relacional PostgreSQL)
- [ ] Contratos de API (endpoints, requisição/resposta)

#### Definição de Stack

- [ ] Seleção final de bibliotecas de NLP para português
- [ ] Definição de bibliotecas de visualização para dashboard
- [ ] Configuração do ambiente de desenvolvimento

#### Design de Interface

- [ ] Mockups de alta fidelidade (Figma): Tela de Chat
- [ ] Mockups: Dashboard de Métricas
- [ ] Identidade visual e padrões de UX
- [ ] Validação de acessibilidade (WCAG) nos mockups

#### Protótipo Inicial

- [ ] Estrutura básica do backend com rotas principais
- [ ] Esqueleto do motor de IA
- [ ] Configuração inicial do PostgreSQL
- [ ] Setup do frontend Vue.js (estrutura de componentes)

### 4.2. Portfólio II (Implementação, Validação e Entrega)

#### Motor de IA

- [ ] Módulo de Pré-processamento (normalização, tokenização, autor em PT-BR)
- [ ] Módulo LSM (Language Style Matching para PT-BR)
- [ ] Módulo de Análise de Sentimentos (polaridade em português)
- [ ] Módulo de Sinais Comportamentais (latência, turnos, comprimento)
- [ ] Módulo de Agregação (heurística → score único)
- [ ] Módulo de Explicabilidade (sumários dos fatores)

#### Backend

- [ ] API REST com todos os endpoints
- [ ] Integração PostgreSQL (diálogos anonimizados, scores, métricas)
- [ ] Versionamento dos cálculos e histórico
- [ ] Mecanismos de exclusão de dados (LGPD)

#### Frontend

- [ ] Interface de Chat (inserção e visualização de diálogos)
- [ ] Dashboard (métricas agregadas, distribuições, explicabilidade)
- [ ] Integração completa com a API REST
- [ ] Tratamento de erros e feedback ao usuário

#### Testes e Validação

- [ ] Testes funcionais (RF01–RF12)
- [ ] Testes de desempenho (tempo de resposta, recursos)
- [ ] Testes de usabilidade (compreensão do score, facilidade de uso)
- [ ] Validação do score (20–30 diálogos, avaliação humana, concordância/correlação)

#### Piloto e Feedback

- [ ] Piloto com pelo menos 10 usuários em diferentes contextos
- [ ] Coleta de feedback qualitativo e quantitativo
- [ ] Análise de métricas de uso
- [ ] Ajustes finais com base no feedback

#### Documentação e Entrega

- [ ] Documentação técnica completa
- [ ] Documentação de usuário
- [ ] Documentação ética, LGPD e mitigação de vieses
- [ ] Apresentação para Demo Day e documentação final do TCC

---

## 5. Referências

- [ ] Lei nº 13.709/2018 (LGPD) citada com link e data de acesso
- [ ] OECD AI Principles citados
- [ ] OWASP Top 10 citado
- [ ] Pennebaker et al. (LIWC2007) citado
- [ ] UNESCO – Ética da IA citada
- [ ] Documentação Flask, Vue.js, PostgreSQL, SQLAlchemy referenciada

---

## 6. Apêndices

- [ ] Definir se haverá apêndices (documento indica que não contempla no momento)

---

## 7. Avaliações de Professores

- [ ] Considerações Professor/a 1
- [ ] Considerações Professor/a 2
- [ ] Considerações Professor/a 3

---

## Artefatos e Imagens

- [ ] `images/instituicao_logo.png`
- [ ] `images/diagrama_casos_uso.png`
- [ ] `images/diagrama_fluso_lgpd.png`
- [ ] `images/c4_nivel1_contexto.png`
- [ ] `images/c4_nivel2_conteineres.png`
- [ ] `images/c4_nivel3_componentes.png`
- [ ] `images/c4_nivel4_codigo.png`

---

*Checklist gerado a partir do documento "Compatibilidade Conversacional com IA".*
*Última atualização: conforme documento de referência.*
