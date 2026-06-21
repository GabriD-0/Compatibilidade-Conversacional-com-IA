# Roteiro 1 — Pitch

**Público:** Banca avaliadora, professores, desenvolvedores  
**Tom:** Direto — apresenta problema, objetivo, solução, diferenciais e impacto  
**Teclas:** `Espaço` avança elemento · `→` pula tela · `R` troca roteiro

---

## Página 1 — O Problema
| O que aparece na tela | O que você diz |
|---|---|
| Label "O PROBLEMA" | Hoje não existe forma objetiva de medir a qualidade de uma conversa entre duas pessoas. |
| Pergunta principal em destaque | Como saber se duas pessoas **realmente se entendem**, de forma mensurável e consistente? |
| Linha divisória + parágrafo explicativo | Mal-entendidos afetam equipes, atendimentos e relações de ensino. Mesmo assim, a comunicação costuma ser avaliada por impressão, não por dados. |
| Estatística "70%" animando de 0 | O desafio é transformar esse problema subjetivo em algo analisável. |
| Stats "3×" e "0 ferramentas" + badge TCC·IFSP·2025 | O projeto preenche essa lacuna: medir compatibilidade conversacional em português, com critérios claros e consistentes. |

---

## Página 2 — A Solução
| O que aparece na tela | O que você diz |
|---|---|
| Sidebar (logo "IA", ícones 💬📊👤) + label "A SOLUÇÃO" | A solução proposta é o sistema **Compatibilidade Conversacional com Inteligência Artificial**. |
| Título "Compatibilidade Conversacional com Inteligência Artificial" + subtítulo | O objetivo é analisar conversas em português e calcular um **score objetivo de compatibilidade** entre os participantes. |
| Card Pilar 1 — 🔤 Estilo Linguístico (LSM) · badge "40% do score" | O primeiro pilar é o **estilo linguístico**, que mede espelhamento na forma de escrever. |
| Card Pilar 2 — 💛 Convergência Emocional · badge "35% do score" | O segundo é a **convergência emocional**, que identifica alinhamento ou divergência no tom. |
| Card Pilar 3 — 🔄 Sinais Comportamentais · badge "25% do score" | O terceiro são os **sinais comportamentais**, como turnos, reciprocidade e tempo de resposta. |
| Row "Score Final · 0 – 100 · LOW · MID · HIGH" | A combinação desses três pilares gera um score de **0 a 100**, classificado como LOW, MID ou HIGH. |

---

## Página 3 — Interface de Chat
| O que aparece na tela | O que você diz |
|---|---|
| Sidebar com conversas (Ana & Bruno 87, Carlos & Maria, João & Laura) | Na interface, cada conversa fica organizada por participantes e pode ser analisada individualmente. |
| Cabeçalho "Ana & Bruno · 24 mensagens" + botão "⚡ Analisar Compatibilidade" | Ao selecionar uma conversa, o sistema lê o histórico e inicia a análise. |
| Mensagens 1 a 5 completando o diálogo | Mensagens e horários alimentam tanto a análise linguística quanto a comportamental. |
| Score overlay: anel 0→87 · "HIGH" · label "SCORE DE COMPATIBILIDADE" | Em poucos segundos, o sistema retorna um resultado: neste exemplo, **87 de 100**, classificado como **HIGH**. |
| Três mini-barras preenchendo: Estilo 91 · Sentimentos 84 · Comportamento 78 | Além do score final, ele mostra os sub-scores de estilo, sentimento e comportamento, permitindo entender de onde o resultado veio. |

---

## Página 4 — Análise Detalhada
| O que aparece na tela | O que você diz |
|---|---|
| Modal escala para o tamanho final com cabeçalho e painel esquerdo | A análise detalhada mostra o resultado de forma explicável, não apenas como um número isolado. |
| Anel SVG anima até 87 · badge "✦ HIGH" aparece · pesos LSM/Sentimentos/Comportamento no painel | O score aparece junto com os pesos dos módulos, mostrando como a decisão foi construída. |
| Card LSM 91/100 com barras Pronomes 94% · Artigos 89% · Conectivos 91% | No estilo linguístico, compara pronomes, artigos e conectivos para medir espelhamento de escrita. |
| Card Sentimentos 84/100 · "Polaridade média: +0.72" | Na parte emocional, observa a polaridade e a compatibilidade do tom. |
| Card Comportamento 78/100 · Ana 52% · Bruno 48% · Reciprocidade 81% · 2min | No comportamento, analisa participação, reciprocidade e tempo médio de resposta. |

---

## Página 5 — Dashboard
| O que aparece na tela | O que você diz |
|---|---|
| Sidebar (ícone 📊 ativo) + header "Dashboard de Análises" · abas 7 dias / **30 dias** / 3 meses | Para acompanhar várias conversas, o sistema também possui um dashboard. |
| 4 KPI cards: 18 conversas · 74,3 score médio · 7 HIGH (39%) · 12 pares únicos | Ele mostra volume de análises, score médio, pares avaliados e distribuição de compatibilidade. |
| Gráfico de barras S1 62 → S7 87, barras crescendo | A evolução por período indica se a comunicação está melhorando ou piorando. |
| Radar hexagonal com 6 eixos (LSM, Emoção, Comportamento, Engajamento, Reciproc., Fluidez) | O radar destaca dimensões específicas para facilitar diagnóstico e comparação. |
| Donut: arco verde HIGH 39% · teal MID 39% · magenta LOW 22% · centro "18" | Esses indicadores transformam conversas comuns em dados úteis para decisão. |

---

## Página 6 — Motor de IA
| O que aparece na tela | O que você diz |
|---|---|
| Título "O motor de Inteligência Artificial" | Por trás da interface existe um pipeline de IA para conversas em português. |
| Box "💬 Entrada de Texto" · badge PT-BR | O sistema recebe mensagens com participantes e horários. |
| Box "⚙️ Pré-processamento" · badge NLP | Depois faz normalização e extração de características linguísticas. |
| Triple grid: 🔤 LSM 40% · 💛 Sentimentos 35% · 🔄 Comportamento 25% | Em seguida, calcula os três pilares: estilo linguístico, convergência emocional e sinais comportamentais. |
| Box "∑ Agregação" · badge Heurística + Box "✦ Score Final" · badge HIGH | Esses resultados são agregados em um score final, acompanhado de uma explicação. |
| Flow labels aparecem · contador de score anima 0→87 | O diferencial é entregar uma métrica objetiva, interpretável, em português e sem depender de APIs externas. |

---

## Página 7 — Casos de Uso
| O que aparece na tela | O que você diz |
|---|---|
| Label "aplicações práticas" · título "Onde a solução pode ser usada" · subtítulo | A solução pode ser usada em qualquer contexto onde a qualidade da comunicação importa. |
| Card 🎧 Atendimento ao Cliente | Em atendimento ao cliente, permite identificar baixa compatibilidade antes que ela se transforme em reclamação. |
| Card 👥 Formação de Equipes | Em equipes, ajuda a comparar padrões comunicativos e apoiar acompanhamento. |
| Cards 🎓 Educação e Tutoria + 🔬 Pesquisa Acadêmica | Na educação e na pesquisa, oferece um indicador padronizado para interações em português. |
| CTA "API REST + Interface Web · Pronto para integrar" com tags REST API · WebSocket · LGPD · PT-BR | O projeto chama atenção porque transforma algo subjetivo em dado: um score explicável, em português, com interface web, API e preocupação com LGPD. Assim, a comunicação passa a ser analisada com critérios objetivos. |
