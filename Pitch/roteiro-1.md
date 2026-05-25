# Roteiro 1 — Técnico

**Público:** Banca avaliadora, professores, desenvolvedores  
**Tom:** Preciso — nomeia módulos, pesos, tecnologias e decisões de engenharia  
**Teclas:** `Espaço` avança elemento · `→` pula tela · `R` troca roteiro

---

## Página 1 — O Problema
| O que aparece na tela | O que você diz |
|---|---|
| Label "O PROBLEMA" | O problema: hoje não existe forma objetiva de medir a qualidade de uma conversa entre duas pessoas. |
| Pergunta principal em destaque | A questão central — como saber se duas pessoas **realmente se entendem**, de forma mensurável e reproduzível? |
| Linha divisória + parágrafo explicativo | Mal-entendidos custam tempo, dinheiro e relacionamentos. A comunicação humana nunca foi tratada como dado estruturado. |
| Estatística "70%" animando de 0 | **70%** dos conflitos profissionais têm origem em falhas de comunicação — sem diagnóstico preciso. |
| Stats "3×" e "0 ferramentas" + badge TCC·IFSP·2025 | Equipes com boa sintonia são **3× mais produtivas**. E até hoje: zero ferramentas em português para medir isso. Este sistema preenche essa lacuna. |

---

## Página 2 — A Solução
| O que aparece na tela | O que você diz |
|---|---|
| Sidebar (logo "IA", ícones 💬📊👤) + label "A SOLUÇÃO" | Compatibilidade Conversacional com IA. Sidebar com navegação e label "A SOLUÇÃO". |
| Título "Compatibilidade Conversacional com Inteligência Artificial" + subtítulo | O objetivo: analisar conversas em português e calcular um **score objetivo de compatibilidade** entre os participantes. |
| Card Pilar 1 — 🔤 Estilo Linguístico (LSM) · badge "40% do score" | Primeiro módulo: **Language Style Matching — 40%** do score. Mede o espelhamento de estilo de escrita entre os dois interlocutores. |
| Card Pilar 2 — 💛 Convergência Emocional · badge "35% do score" | Segundo módulo: **Convergência Emocional — 35%**. Analisa o alinhamento de sentimentos ao longo da conversa com NLP em português. |
| Card Pilar 3 — 🔄 Sinais Comportamentais · badge "25% do score" | Terceiro módulo: **Sinais Comportamentais — 25%**. Mede tempo de resposta, equilíbrio de turnos e reciprocidade. |
| Row "Score Final · 0 – 100 · LOW · MID · HIGH" | Os três módulos combinados produzem um score de **0 a 100**, classificado em LOW, MID ou HIGH. |

---

## Página 3 — Interface de Chat
| O que aparece na tela | O que você diz |
|---|---|
| Sidebar com conversas (Ana & Bruno 87, Carlos & Maria, João & Laura) | Sidebar com lista de conversas. "Ana & Bruno" aparece com score 87 já calculado, ao lado de outros pares. |
| Cabeçalho "Ana & Bruno · 24 mensagens" + botão "⚡ Analisar Compatibilidade" | Cabeçalho da conversa: dois participantes identificados, 24 mensagens. Botão de análise em destaque. |
| Mensagem 1 (Ana, 10:23) e Mensagem 2 (Bruno, 10:25) | Mensagens 1 e 2: Ana pergunta sobre a revisão; Bruno responde com atenção. Timestamps registrados. |
| Mensagens 3, 4 e 5 completando o diálogo | Mais 3 mensagens completam o histórico. O diálogo está salvo e disponível para análise. |
| Score overlay: anel 0→87 · "HIGH" · label "SCORE DE COMPATIBILIDADE" | Clique em Analisar: resultado em menos de 3 segundos. **87 de 100, classificação HIGH**. Anel circular confirma visualmente. |
| Três mini-barras preenchendo: Estilo 91 · Sentimentos 84 · Comportamento 78 | Sub-scores detalhados: Estilo Linguístico **91**, Sentimentos **84**, Comportamento **78**. |

---

## Página 4 — Análise Detalhada
| O que aparece na tela | O que você diz |
|---|---|
| Modal escala para o tamanho final com cabeçalho e painel esquerdo | Modal "Análise Detalhada · Ana & Bruno". 24 mensagens analisadas, calculado em 25 mai. 2025 às 10h29. |
| Anel SVG anima até 87 · badge "✦ HIGH" aparece · pesos LSM/Sentimentos/Comportamento no painel | O anel SVG anima até **87**. Classificação **HIGH** aparece. Painel esquerdo exibe os pesos de cada módulo. |
| Card LSM 91/100 com barras Pronomes 94% · Artigos 89% · Conectivos 91% | Language Style Matching: **91 / 100**. Pronomes 94%, artigos 89%, conectivos 91% — espelhamento quase perfeito. |
| Card Sentimentos 84/100 · "Polaridade média: +0.72" | Convergência de Sentimentos: **84 / 100**. Tom positivo e construtivo ao longo de toda a conversa. Polaridade média +0,72. |
| Card Comportamento 78/100 · Ana 52% · Bruno 48% · Reciprocidade 81% · 2min | Sinais Comportamentais: **78 / 100**. Ana 52%, Bruno 48% dos turnos. Reciprocidade 81%. Tempo médio de resposta: 2 minutos. |

---

## Página 5 — Dashboard
| O que aparece na tela | O que você diz |
|---|---|
| Sidebar (ícone 📊 ativo) + header "Dashboard de Análises" · abas 7 dias / **30 dias** / 3 meses | Dashboard de Análises. Sidebar com ícone 📊 ativo. Período selecionado: **30 dias**. |
| 4 KPI cards: 18 conversas · 74,3 score médio · 7 HIGH (39%) · 12 pares únicos | **18** conversas analisadas · Score médio **74,3** · **7** pares HIGH (39%) · **12** pares únicos. |
| Gráfico de barras S1 62 → S7 87, barras crescendo | Gráfico semanal: S1 62 → S7 **87**. Crescimento de 25 pontos em 7 semanas. |
| Radar hexagonal com 6 eixos (LSM, Emoção, Comportamento, Engajamento, Reciproc., Fluidez) | Radar chart com **6 dimensões**: LSM, Emoção, Comportamento, Engajamento, Reciprocidade e Fluidez. |
| Donut: arco verde HIGH 39% · teal MID 39% · magenta LOW 22% · centro "18" | Donut de distribuição: **HIGH 39%** · MID 39% · LOW 22%. Total de 18 análises no centro. |

---

## Página 6 — Motor de IA
| O que aparece na tela | O que você diz |
|---|---|
| Título "O motor de Inteligência Artificial" | O **Motor de Inteligência Artificial**. Pipeline Python construído para processar conversas em português. |
| Box "💬 Entrada de Texto" · badge PT-BR | Etapa 1 — **Entrada de Texto**: mensagens dos dois participantes em PT-BR com timestamps. |
| Box "⚙️ Pré-processamento" · badge NLP | Etapa 2 — **Pré-processamento**: normalização, tokenização e extração de palavras-função em português. |
| Triple grid: 🔤 LSM 40% · 💛 Sentimentos 35% · 🔄 Comportamento 25% | Etapa 3 — três módulos em paralelo: **LSM 40%** · **Sentimentos 35%** · **Comportamento 25%**. |
| Box "∑ Agregação" · badge Heurística + Box "✦ Score Final" · badge HIGH | Etapa 4 — **Agregação** ponderada e geração de explicação. Etapa 5 — **Score Final** classificado HIGH. |
| Flow labels aparecem · contador de score anima 0→87 | De texto bruto a score explicável: **87 de 100** em menos de 3 segundos, sem APIs externas. |

---

## Página 7 — Casos de Uso
| O que aparece na tela | O que você diz |
|---|---|
| Label "aplicações práticas" · título "Onde a solução pode ser usada" · subtítulo | "Onde a solução pode ser usada" — qualquer contexto onde a qualidade da comunicação importa. |
| Card 🎧 Atendimento ao Cliente | 🎧 **Atendimento ao Cliente**: score de rapport por atendimento. Identifique baixa compatibilidade antes da reclamação. |
| Card 👥 Formação de Equipes | 👥 **Formação de Equipes**: compare perfis comunicativos antes de montar squads. Reduza conflitos e melhore a sinergia. |
| Cards 🎓 Educação e Tutoria + 🔬 Pesquisa Acadêmica | 🎓 **Educação**: detecte desalinhamento tutor-aluno. 🔬 **Pesquisa Acadêmica**: API com score padronizado. |
| CTA "API REST + Interface Web · Pronto para integrar" com tags REST API · WebSocket · LGPD · PT-BR | API REST + Interface Web · Flask, Vue 3, PostgreSQL, WebSockets · **Conformidade LGPD** · Pronto para integrar. |

---

## Página 8 — Stack Tecnológico
| O que aparece na tela | O que você diz |
|---|---|
| Título "Stack completo e moderno" · Camada de Apresentação (Vue 3+TS+Pinia+Chart.js) · chips Frontend | Camada de Apresentação: **Vue 3 + TypeScript + Pinia + Chart.js**. |
| Conectores HTTP/HTTPS e WebSocket · Camada de API (Flask+SocketIO+JWT) · Camada de IA (LSM·Sentimentos·Comportamento) · chips Backend + IA | Camada de API: **Flask + SocketIO + JWT + Rate Limiting**. Motor de IA: **HuggingFace Transformers + PyTorch**. |
| Conector SQLAlchemy ORM · Camada de Persistência (PostgreSQL+Alembic) · chips Dados e Qualidade (pytest · LGPD) | Camada de Persistência: **PostgreSQL + Alembic**. Qualidade: **pytest + LGPD**. |

---

## Página 9 — Fechamento
| O que aparece na tela | O que você diz |
|---|---|
| Label "Compatibilidade Conversacional com IA" · título "Comunicação analisada, relacionamentos transformados." | Compatibilidade Conversacional com IA. **Comunicação analisada, relacionamentos transformados.** |
| Parágrafo "Chega de achismos. Pela primeira vez..." | Pela primeira vez em português: uma forma objetiva de medir o quanto duas pessoas se entendem em uma conversa. |
| 6 badges em cascata (Score 0–100 · LSM+Sent+Comp · API REST · LGPD · PT-BR · < 3 segundos) | Score 0–100 explicável · LSM + Sentimentos + Comportamento · API REST · LGPD · PT-BR nativo · resultado em < 3 segundos. |
| Contador 0→87 · badge "HIGH ✦" · créditos "IFSP · 2025" | **Score 87 de 100 · HIGH**. Trabalho de Conclusão de Curso — IFSP 2025. |
