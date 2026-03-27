# Resumo do Projeto

## Compatibilidade Conversacional com IA

Este projeto de Trabalho de Conclusao de Curso em Engenharia de Software propoe o desenvolvimento de um sistema de Inteligencia Artificial capaz de estimar um indice de compatibilidade conversacional entre duas pessoas a partir de suas interacoes textuais em portugues (PT-BR). A solucao parte da premissa de que a harmonia comunicativa pode ser inferida diretamente do dialogo, combinando tres dimensoes de analise: similaridade de estilo linguistico (Language Style Matching), convergencia emocional por meio de analise de sentimentos e sinais comportamentais como tempo de resposta, equilibrio de turnos e extensao das mensagens.

Essas metricas sao consolidadas por uma camada de agregacao — inicialmente heuristica, com possibilidade de evolucao para aprendizado supervisionado — gerando um score unico de 0 a 100, acompanhado de explicacoes textuais que garantem transparencia ao usuario.

A arquitetura do sistema segue o modelo API-first, com backend em Python (Flask) e banco de dados PostgreSQL, alem de um frontend em Vue.js 3 com TypeScript que oferece interface de chat para insercao de dialogos e um dashboard interativo para visualizacao de metricas e insights. Todo o projeto foi concebido em conformidade com a LGPD, incluindo mecanismos de consentimento, anonimizacao e exclusao de dados.

O sistema e voltado a gestores de equipes, plataformas de atendimento, aplicacoes de mentoria e pesquisadores em linguistica computacional e comunicacao, oferecendo uma ferramenta objetiva e explicavel para avaliar a qualidade da interacao entre participantes de um dialogo.
