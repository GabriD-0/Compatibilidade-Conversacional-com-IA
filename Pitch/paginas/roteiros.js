/**
 * roteiros.js — conteúdo de narração para os 3 roteiros do pitch.
 * Cada subtítulo descreve exatamente o que está aparecendo na tela naquele step.
 */
window.ROTEIROS = {

  meta: {
    1: {
      nome: 'Técnico',
      desc: 'Para bancas e desenvolvedores. Nomeia componentes, pesos e decisões de engenharia.',
    },
    2: {
      nome: 'Produto',
      desc: 'Para gestores e investidores. Foca no valor entregue e no que o usuário consegue fazer.',
    },
    3: {
      nome: 'Narrativo',
      desc: 'Para o público geral. Conta a história de Ana e Bruno do problema à solução.',
    },
  },

  /* ══════════════════════════ ROTEIRO 1 — TÉCNICO ══════════════════════════ */
  1: {
    /* Página 1 — O Problema */
    1: [
      'O problema: hoje não existe forma objetiva de medir a qualidade de uma conversa entre duas pessoas.',
      'A questão central — como saber se duas pessoas <strong>realmente se entendem</strong>, de forma mensurável e reproduzível?',
      'Mal-entendidos custam tempo, dinheiro e relacionamentos. A comunicação humana nunca foi tratada como dado estruturado.',
      '<strong>70%</strong> dos conflitos profissionais têm origem em falhas de comunicação — sem diagnóstico preciso.',
      'Equipes com boa sintonia são <strong>3× mais produtivas</strong>. E até hoje: zero ferramentas em português para medir isso. Este sistema preenche essa lacuna.',
    ],
    /* Página 2 — A Solução */
    2: [
      'Compatibilidade Conversacional com IA. Sidebar com navegação e label "A SOLUÇÃO".',
      'O objetivo: analisar conversas em português e calcular um <strong>score objetivo de compatibilidade</strong> entre os participantes.',
      'Primeiro módulo: <strong>Language Style Matching — 40%</strong> do score. Mede o espelhamento de estilo de escrita entre os dois interlocutores.',
      'Segundo módulo: <strong>Convergência Emocional — 35%</strong>. Analisa o alinhamento de sentimentos ao longo da conversa com NLP em português.',
      'Terceiro módulo: <strong>Sinais Comportamentais — 25%</strong>. Mede tempo de resposta, equilíbrio de turnos e reciprocidade.',
      'Os três módulos combinados produzem um score de <strong>0 a 100</strong>, classificado em LOW, MID ou HIGH.',
    ],
    /* Página 3 — Interface de Chat */
    3: [
      'Sidebar com lista de conversas. "Ana &amp; Bruno" aparece com score 87 já calculado, ao lado de outros pares.',
      'Cabeçalho da conversa: dois participantes identificados, 24 mensagens. Botão "⚡ Analisar Compatibilidade" em destaque.',
      'Mensagens 1 e 2: Ana pergunta sobre a revisão; Bruno responde com atenção. Timestamps registrados.',
      'Histórico completo salvo. Um clique em <strong>Analisar Compatibilidade</strong> e o sistema processa em menos de 3 segundos.',
    ],
    /* Página 4 — Análise Detalhada */
    4: [
      'Modal "Análise Detalhada · Ana &amp; Bruno". 24 mensagens analisadas, calculado em 25 mai. 2025 às 10h29.',
      'O anel SVG anima até <strong>87</strong>. Classificação <strong>HIGH</strong> aparece. Painel esquerdo exibe os pesos de cada módulo.',
      'Language Style Matching: <strong>91 / 100</strong>. Pronomes 94%, artigos 89%, conectivos 91% — espelhamento quase perfeito.',
      'Convergência de Sentimentos: <strong>84 / 100</strong>. Tom positivo e construtivo ao longo de toda a conversa. Polaridade média +0,72.',
      'Sinais Comportamentais: <strong>78 / 100</strong>. Ana 52%, Bruno 48% dos turnos. Reciprocidade 81%. Tempo médio de resposta: 2 minutos.',
    ],
    /* Página 5 — Dashboard */
    5: [
      'Dashboard de Análises. Sidebar com ícone 📊 ativo. Abas de período: 7 dias, <strong>30 dias</strong>, 3 meses.',
      '<strong>18</strong> conversas analisadas · Score médio <strong>74,3</strong> · <strong>7</strong> pares HIGH (39%) · <strong>12</strong> pares únicos.',
      'Gráfico de barras semanal: S1 62 → S7 <strong>87</strong>. Crescimento de 25 pontos em 7 semanas.',
      'Radar chart com <strong>6 dimensões</strong>: LSM, Emoção, Comportamento, Engajamento, Reciprocidade e Fluidez.',
      'Donut de distribuição: <strong>HIGH 39%</strong> · MID 39% · LOW 22%. Total de 18 análises no centro.',
    ],
    /* Página 6 — Motor de IA */
    6: [
      'O <strong>Motor de Inteligência Artificial</strong>. Pipeline Python construído para processar conversas em português.',
      'Etapa 1 — <strong>Entrada de Texto</strong>: mensagens dos dois participantes em PT-BR com timestamps.',
      'Etapa 2 — <strong>Pré-processamento</strong>: normalização, tokenização e extração de palavras-função em português.',
      'Etapa 3 — três módulos em paralelo: <strong>LSM 40%</strong> · <strong>Sentimentos 35%</strong> · <strong>Comportamento 25%</strong>.',
      'Etapa 4 — <strong>Agregação</strong> ponderada e geração de explicação. Etapa 5 — <strong>Score Final</strong> classificado HIGH.',
      'De texto bruto a score explicável: <strong>87 de 100</strong> em menos de 3 segundos, sem APIs externas.',
    ],
    /* Página 7 — Casos de Uso */
    7: [
      '"Onde a solução pode ser usada" — qualquer contexto onde a qualidade da comunicação importa.',
      '🎧 <strong>Atendimento ao Cliente</strong>: score de rapport por atendimento. Identifique baixa compatibilidade antes da reclamação.',
      '👥 <strong>Formação de Equipes</strong>: compare perfis comunicativos antes de montar squads. Reduza conflitos e melhore a sinergia.',
      '🎓 <strong>Educação</strong>: detecte desalinhamento tutor-aluno. 🔬 <strong>Pesquisa Acadêmica</strong>: API com score padronizado.',
      'API REST + Interface Web · Flask, Vue 3, PostgreSQL, WebSockets · <strong>Conformidade LGPD</strong> · Pronto para integrar.',
    ],
    /* Página 8 — Stack */
    8: [
      'Camada de Apresentação: <strong>Vue 3 + TypeScript + Pinia + Chart.js</strong>.',
      'Camada de API: <strong>Flask + SocketIO + JWT + Rate Limiting</strong>. Motor de IA: <strong>HuggingFace Transformers + PyTorch</strong>.',
      'Camada de Persistência: <strong>PostgreSQL + Alembic</strong>. Qualidade: <strong>pytest + LGPD</strong>.',
    ],
    /* Página 9 — Fechamento */
    9: [
      'Compatibilidade Conversacional com IA. <strong>Comunicação analisada, relacionamentos transformados.</strong>',
      'Pela primeira vez em português: uma forma objetiva de medir o quanto duas pessoas se entendem em uma conversa.',
      'Score 0–100 explicável · LSM + Sentimentos + Comportamento · API REST · LGPD · PT-BR nativo · resultado em &lt; 3 segundos.',
      '<strong>87 de 100 · HIGH</strong>. Trabalho de Conclusão de Curso — IFSP 2025.',
    ],
  },

  /* ══════════════════════════ ROTEIRO 2 — PRODUTO ══════════════════════════ */
  2: {
    1: [
      'O problema começa aqui: toda vez que duas pessoas conversam, algo decide se vão se entender — ou não.',
      'Como saber, de forma concreta, se duas pessoas <strong>realmente se entenderam</strong>? Essa resposta nunca existiu — até agora.',
      'Mal-entendidos custam caro: clientes perdidos, equipes em conflito, aprendizado prejudicado. O problema é real.',
      '<strong>70%</strong> dos conflitos profissionais vêm de falhas de comunicação que ninguém consegue medir com precisão.',
      'Equipes alinhadas são <strong>3× mais produtivas</strong>. E até hoje, zero ferramentas em português para medir isso. Este sistema muda esse cenário.',
    ],
    2: [
      'Esta é a interface — sidebar organizada, navegação limpa. Projetada para qualquer usuário, não só para técnicos.',
      'Compatibilidade Conversacional com IA: ele lê uma conversa e diz, objetivamente, o quanto os dois lados estão em sintonia.',
      'Primeiro pilar: <strong>Estilo Linguístico — 40%</strong>. Quando dois interlocutores se entendem bem, eles começam a usar as mesmas estruturas sem perceber.',
      'Segundo pilar: <strong>Convergência Emocional — 35%</strong>. Os dois estão em sintonia emocional, ou indo em direções opostas?',
      'Terceiro pilar: <strong>Sinais Comportamentais — 25%</strong>. Quem fala mais? Quem responde mais rápido? A conversa é equilibrada?',
      'Os três pilares geram um único número: <strong>0 a 100</strong>. Com classificação LOW, MID ou <strong>HIGH</strong>.',
    ],
    3: [
      'Sidebar: todas as conversas salvas. "Ana &amp; Bruno" com score <strong>87</strong>, Carlos &amp; Maria, João &amp; Laura. Tudo organizado.',
      'Ao abrir a conversa, os dois participantes são identificados. Um clique é tudo que separa a conversa do resultado.',
      'As mensagens aparecem em ordem: Ana pergunta sobre a revisão, Bruno responde com atenção. A troca parece fluida.',
      'Histórico completo salvo. Um clique em <strong>Analisar Compatibilidade</strong> e o sistema processa em menos de 3 segundos.',
    ],
    4: [
      'Um clique abre a análise completa: 24 mensagens analisadas, data e hora registradas. O contexto completo.',
      'Score <strong>87, HIGH</strong>. O anel confirma. À esquerda, os pesos de cada pilar ficam expostos — <strong>nenhuma caixa-preta</strong>.',
      'Estilo Linguístico: <strong>91</strong>. Pronomes, artigos e conectivos quase idênticos entre os dois. Eles se expressam de forma muito similar.',
      'Sentimentos: <strong>84</strong>. Tom positivo e construtivo. A conversa não teve polarizações emocionais bruscas.',
      'Comportamento: <strong>78</strong>. 52% Ana, 48% Bruno. Respostas rápidas, boa reciprocidade. Uma troca genuína.',
    ],
    5: [
      'O Dashboard conta a história do mês. Período de <strong>30 dias</strong>. Todas as análises em um só lugar.',
      '<strong>18 conversas</strong> analisadas · Score médio <strong>74,3</strong> com tendência de alta · <strong>7 HIGH</strong> · 12 pares monitorados.',
      'Evolução semanal: de 62 na semana 1 a <strong>87 na semana 7</strong>. A tendência de melhora é clara e mensurável.',
      'Radar com 6 dimensões: visão rápida de onde está o ponto forte e onde está o gargalo da comunicação.',
      '<strong>39% HIGH</strong> · 39% MID · 22% LOW. Dados concretos para decisões de treinamento e formação de times.',
    ],
    6: [
      'Por trás da interface simples, há um motor de IA construído <strong>especificamente para o português</strong>.',
      'A entrada são as mensagens dos dois participantes — texto bruto, em português, com timestamps.',
      'Pré-processamento calibrado para PT-BR. O sistema <strong>entende o português</strong>, não apenas o tolera.',
      'Três módulos em paralelo: <strong>LSM 40%</strong>, <strong>Sentimentos 35%</strong> e <strong>Comportamento 25%</strong>.',
      'Agregação dos sub-scores e geração de explicação automática. Score e contexto juntos.',
      '<strong>87 de 100 em menos de 3 segundos</strong>. Rápido o suficiente para uso em tempo real.',
    ],
    7: [
      '"Onde a solução pode ser usada?" O sistema foi construído como plataforma — não como ferramenta pontual.',
      '🎧 <strong>Atendimento ao cliente</strong>: cada interação vira um score. Identifique problemas com dados antes da reclamação.',
      '👥 <strong>Formação de equipes</strong>: compare perfis comunicativos antes de montar um squad. Menos conflito, mais sinergia.',
      '🎓 <strong>Educação online</strong>: detecte desalinhamento tutor-aluno. 🔬 <strong>Pesquisa</strong>: API com score padronizado.',
      'API REST · WebSocket · Vue 3 · Flask · PostgreSQL · <strong>LGPD</strong> · Pronto para integrar ao que já existe.',
    ],
    8: [
      'Frontend: <strong>Vue 3, TypeScript, Pinia, Vite, Tailwind e PrimeVue</strong>. Interface responsiva e pronta para produção.',
      'Backend: <strong>Flask + JWT + SocketIO + Rate Limiting</strong>. IA: <strong>HuggingFace + PyTorch</strong> rodando localmente.',
      'Dados: <strong>PostgreSQL + Alembic</strong>. Qualidade: <strong>pytest</strong>. Privacidade: <strong>LGPD</strong> integrada na arquitetura.',
    ],
    9: [
      'Compatibilidade Conversacional com IA. <strong>Comunicação analisada, relacionamentos transformados.</strong>',
      'Chega de achismos. Agora existe uma forma de medir, em português, o quanto duas pessoas se entendem.',
      'Score 0–100 · LSM + Sentimentos + Comportamento · API REST · WebSocket · LGPD · PT-BR · &lt; 3 segundos.',
      '<strong>87 de 100 · HIGH</strong>. IFSP, 2025.',
    ],
  },

  /* ══════════════════════════ ROTEIRO 3 — NARRATIVO ══════════════════════════ */
  3: {
    1: [
      'O problema começa com uma sensação familiar: você saiu de uma reunião e algo não funcionou — mas você não sabe exatamente o quê.',
      'Como saber se duas pessoas <strong>realmente se entenderam</strong>? Não a impressão — o dado. Essa pergunta ficou sem resposta por muito tempo.',
      'Mal-entendidos custam relacionamentos, projetos, confiança. E a comunicação nunca foi tratada como algo que se possa medir.',
      '<strong>70%</strong> dos conflitos profissionais têm raiz em falhas de comunicação. A maioria passa sem diagnóstico.',
      'Equipes alinhadas são <strong>3× mais produtivas</strong>. E até hoje não existia nenhuma ferramenta em português para medir isso. Até agora.',
    ],
    2: [
      'Este é o sistema. Sidebar à esquerda com as conversas, logo "IA" no topo. Navegação simples e direta.',
      'Compatibilidade Conversacional com IA: ele lê uma conversa e calcula, objetivamente, o quanto os dois lados estão em sintonia.',
      'O primeiro fator é o <strong>Estilo Linguístico — 40%</strong>. Quando duas pessoas se entendem bem, elas começam a usar as mesmas estruturas de linguagem sem perceber.',
      'O segundo é a <strong>Convergência Emocional — 35%</strong>. Ao longo da conversa, os tons estão se aproximando — ou se afastando?',
      'O terceiro são os <strong>Sinais Comportamentais — 25%</strong>. Quem fala mais? Quem responde mais rápido? A conversa é de mão dupla, ou monólogo?',
      'Os três fatores combinados dão um número de <strong>0 a 100</strong>. LOW, MID ou HIGH. Simples de ler, complexo de calcular.',
    ],
    3: [
      'A sidebar mostra as conversas salvas. "Ana &amp; Bruno" está aqui, com score 87. Vamos ver de onde esse número veio.',
      'O cabeçalho identifica os dois: Ana e Bruno, <strong>24 mensagens</strong>. O botão "Analisar Compatibilidade" espera um clique.',
      'Primeiras mensagens: Ana pergunta se Bruno revisou o documento. Bruno responde que sim, com cuidado. A troca parece tranquila.',
      'Histórico completo salvo. Um clique em <strong>Analisar Compatibilidade</strong> e o sistema processa em menos de 3 segundos.',
    ],
    4: [
      'Ana quer entender melhor. Um clique abre a análise completa: <strong>24 mensagens</strong>, calculadas no dia 25 de maio às 10h29.',
      '<strong>87, HIGH</strong>. O anel vai se completando enquanto o número sobe. À esquerda, os pesos de cada fator — transparência total.',
      'Estilo Linguístico: <strong>91</strong>. Pronomes 94%, artigos 89%, conectivos 91%. Ana e Bruno estavam escrevendo de forma muito parecida — sem perceber.',
      'Sentimentos: <strong>84</strong>. Tom positivo e construtivo do começo ao fim. Polaridade média de +0,72 — bem acima do neutro.',
      'Comportamento: <strong>78</strong>. 52% Ana, 48% Bruno. Respostas em média a cada 2 minutos. Uma conversa equilibrada, sem dominância.',
    ],
    5: [
      'Com o tempo, o Dashboard conta a história completa. Período de <strong>30 dias</strong>. Todas as análises de Ana em um só lugar.',
      '<strong>18 conversas</strong>, score médio <strong>74,3</strong>. 7 pares em HIGH — quase 4 em cada 10. 12 pares únicos monitorados.',
      'Semana a semana: começou em 62, chegou a <strong>87 na semana 7</strong>. A comunicação de Ana está melhorando — com dados para provar.',
      'O radar mostra onde ela está forte e onde pode melhorar: <strong>6 dimensões</strong>, do LSM à Fluidez.',
      'Distribuição: <strong>39% HIGH</strong> · 39% MID · 22% LOW. Ana sabe exatamente em quais conversas algo não funcionou.',
    ],
    6: [
      'O que acontece nos bastidores quando Ana clica em Analisar? Este é o motor que processa tudo.',
      'A entrada são as mensagens — texto em português com timestamps. É o começo do pipeline.',
      'Primeiro, o pré-processamento: normalização e tokenização calibradas para PT-BR. Foi feito para o português, não é uma adaptação.',
      'Depois, três módulos em paralelo: <strong>LSM 40%</strong>, <strong>Sentimentos 35%</strong>, <strong>Comportamento 25%</strong>.',
      'Os resultados são agregados e o sistema gera uma explicação em português. Ana recebe um contexto, não um número cru.',
      '<strong>87 de 100</strong> em menos de 3 segundos. Sem nuvem, sem custo por análise. Tudo processado localmente.',
    ],
    7: [
      'A história de Ana é só um exemplo. Esse sistema foi feito para qualquer lugar onde a comunicação importa.',
      '🎧 No <strong>atendimento ao cliente</strong>: o supervisor identifica os casos de baixa compatibilidade antes da reclamação.',
      '👥 Na <strong>formação de equipes</strong>: dois colaboradores que se comunicam bem trabalham melhor juntos — agora você pode medir isso.',
      '🎓 Na <strong>educação</strong>: o tutor com baixo score com um aluno específico recebe um alerta. 🔬 Na <strong>pesquisa</strong>: API com score reproduzível.',
      'API REST · WebSockets · conformidade <strong>LGPD</strong> · documentação completa. Pronto para integrar ao que já existe.',
    ],
    8: [
      'Para construir isso, usamos uma stack moderna. No frontend: <strong>Vue 3, TypeScript, Pinia</strong> e Chart.js para os gráficos.',
      'No servidor: <strong>Flask com SocketIO</strong> para tempo real, JWT e rate limiting. A IA usa HuggingFace — <strong>nenhum dado sai do servidor</strong>.',
      'Na base: <strong>PostgreSQL com Alembic</strong> para migrations controladas. Testes com pytest. <strong>LGPD</strong> embutida desde o início.',
    ],
    9: [
      'Ana e Bruno ainda trabalham juntos. Mas agora, quando uma conversa não funciona, eles não ficam só com a sensação.',
      'Eles têm dados. Sabem se o problema foi no estilo, na emoção ou na dinâmica. E podem trabalhar isso de forma consciente.',
      'Score 0–100 · LSM + Sentimentos + Comportamento · API REST · LGPD · PT-BR · resultado em &lt; 3 segundos.',
      '<strong>87 de 100 · HIGH</strong>. Comunicação analisada, relacionamentos transformados. IFSP, 2025.',
    ],
  },

};
