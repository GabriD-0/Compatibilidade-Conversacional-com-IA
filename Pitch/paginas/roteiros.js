/**
 * roteiros.js — conteúdo de narração do pitch.
 */
window.ROTEIROS = {
  meta: {
    1: {
      nome: 'Pitch',
      desc: 'Direto ao ponto: problema, objetivo, solução, diferenciais e impacto.',
    },
  },

  1: {
    1: [
      'Hoje não existe forma objetiva de medir a qualidade de uma conversa entre duas pessoas.',
      'Como saber se duas pessoas <strong>realmente se entendem</strong>, de forma mensurável e consistente?',
      'Mal-entendidos afetam equipes, atendimentos e relações de ensino. Mesmo assim, a comunicação costuma ser avaliada por impressão, não por dados.',
      'O desafio é transformar esse problema subjetivo em algo analisável.',
      'O projeto preenche essa lacuna: medir compatibilidade conversacional em português, com critérios claros e consistentes.',
    ],
    2: [
      'A solução proposta é o sistema <strong>Compatibilidade Conversacional com Inteligência Artificial</strong>.',
      'O objetivo é analisar conversas em português e calcular um <strong>score objetivo de compatibilidade</strong> entre os participantes.',
      'O primeiro pilar é o <strong>estilo linguístico</strong>, que mede espelhamento na forma de escrever.',
      'O segundo é a <strong>convergência emocional</strong>, que identifica alinhamento ou divergência no tom.',
      'O terceiro são os <strong>sinais comportamentais</strong>, como turnos, reciprocidade e tempo de resposta.',
      'A combinação desses três pilares gera um score de <strong>0 a 100</strong>, classificado como LOW, MID ou HIGH.',
    ],
    3: [
      'Na interface, cada conversa fica organizada por participantes e pode ser analisada individualmente.',
      'Ao selecionar uma conversa, o sistema lê o histórico e inicia a análise.',
      'Mensagens e horários alimentam tanto a análise linguística quanto a comportamental.',
      'Em poucos segundos, o sistema retorna um resultado: neste exemplo, <strong>87 de 100</strong>, classificado como <strong>HIGH</strong>.',
      'Além do score final, ele mostra os sub-scores de estilo, sentimento e comportamento, permitindo entender de onde o resultado veio.',
    ],
    4: [
      'A análise detalhada mostra o resultado de forma explicável, não apenas como um número isolado.',
      'O score aparece junto com os pesos dos módulos, mostrando como a decisão foi construída.',
      'No estilo linguístico, compara pronomes, artigos e conectivos para medir espelhamento de escrita.',
      'Na parte emocional, observa a polaridade e a compatibilidade do tom.',
      'No comportamento, analisa participação, reciprocidade e tempo médio de resposta.',
    ],
    5: [
      'Para acompanhar várias conversas, o sistema também possui um dashboard.',
      'Ele mostra volume de análises, score médio, pares avaliados e distribuição de compatibilidade.',
      'A evolução por período indica se a comunicação está melhorando ou piorando.',
      'O radar destaca dimensões específicas para facilitar diagnóstico e comparação.',
      'Esses indicadores transformam conversas comuns em dados úteis para decisão.',
    ],
    6: [
      'Por trás da interface existe um pipeline de IA para conversas em português.',
      'O sistema recebe mensagens com participantes e horários.',
      'Depois faz normalização e extração de características linguísticas.',
      'Em seguida, calcula os três pilares: estilo linguístico, convergência emocional e sinais comportamentais.',
      'Esses resultados são agregados em um score final, acompanhado de uma explicação.',
      'O diferencial é entregar uma métrica objetiva, interpretável, em português e sem APIs externas.',
    ],
    7: [
      'A solução pode ser usada em qualquer contexto onde a qualidade da comunicação importa.',
      'Em atendimento ao cliente, permite identificar baixa compatibilidade antes que ela se transforme em reclamação.',
      'Em equipes, ajuda a comparar padrões comunicativos e apoiar acompanhamento.',
      'Na educação e na pesquisa, oferece um indicador padronizado para interações em português.',
      'O projeto chama atenção porque transforma algo subjetivo em dado: um score explicável, em português, com interface web, API e preocupação com LGPD. Assim, a comunicação passa a ser analisada com critérios objetivos.',
    ],
  },
};
