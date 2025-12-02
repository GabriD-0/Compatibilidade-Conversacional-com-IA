# Compatibilidade Conversacional com IA

Sistema de Inteligência Artificial para estimar um **índice de compatibilidade conversacional** entre duas pessoas a partir de suas interações textuais. A solução analisa conversas e gera uma pontuação unificada que reflete a sintonia entre os participantes, combinando análise de estilo linguístico (LSM), convergência de sentimentos e sinais comportamentais.

> **⚠️ Status do Projeto**: Este projeto está atualmente em **fase de documentação e planejamento**. O código ainda não foi implementado. Este repositório contém a documentação técnica completa, diagramas de arquitetura e especificações do sistema.

## 📋 Sobre o Projeto

Este projeto visa aprimorar a colaboração, o engajamento e a satisfação em cenários como atendimento ao cliente, equipes de projeto, duplas de estudo e relacionamentos pessoais, partindo da premissa de que a harmonia comunicativa pode ser inferida diretamente do diálogo.

### Objetivo Geral

Desenvolver um sistema de IA capaz de analisar conversas textuais entre duas pessoas e estimar um **score de compatibilidade conversacional**, refletindo sintonia de estilo, alinhamento emocional e dinâmica de interação.

### Diferenciais

- Foco na **compatibilidade conversacional** e não apenas na análise de sentimentos ou conteúdo
- Uso de **Language Style Matching (LSM)** adaptado para português
- Combinação de **três dimensões complementares** — estilo, sentimento e comportamento — em um **score único**
- **Explicabilidade**: sumários textuais destacando os principais fatores que influenciaram o resultado
- Arquitetura **API-first**, facilitando integração com outros sistemas
- Conformidade com **LGPD** e princípios de IA responsável

## 🎯 Funcionalidades Planejadas

### Motor de IA

- **Similaridade de Estilo Linguístico (LSM)**: cálculo de alinhamento no uso de palavras-função entre participantes
- **Análise de Sentimentos**: classificação de polaridade e intensidade em PT-BR, com avaliação de convergência emocional
- **Sinais Comportamentais**: extração de métricas como tempo médio de resposta, equilíbrio de turnos de fala e comprimento médio das mensagens
- **Agregação Heurística**: combinação das métricas em um score único de compatibilidade conversacional
- **Explicabilidade**: geração de sumários explicáveis sobre os fatores que influenciaram o score

### Interface Web

- **Chat**: interface para inserção e visualização de diálogos entre dois participantes
- **Dashboard**: visualização de métricas agregadas, distribuições de scores, top-N matches e painéis de explicabilidade

### API REST

- Endpoints para envio de diálogos e recuperação de scores e métricas
- Suporte a integração com sistemas externos (plataformas de atendimento, sistemas de gestão de equipes, etc.)

## 🛠️ Stack Tecnológica Planejada

### Backend

- **Python**: implementação do backend, motor de IA, pré-processamento de texto e cálculo de métricas
- **Flask**: framework para API REST
- **SQLAlchemy**: ORM para PostgreSQL
- **Bibliotecas de NLP**: processamento de linguagem natural em português (a definir)

### Frontend

- **React**: framework para construção da interface web
- **JavaScript/TypeScript**: desenvolvimento do frontend
- **Bibliotecas de visualização**: gráficos e dashboards (a definir)

### Banco de Dados

- **PostgreSQL**: armazenamento de conversas (anonimizadas), scores, métricas e logs

### Ferramentas

- **Git**: controle de versão
- **Docker**: containerização (planejado)

## 🏗️ Arquitetura Proposta

O sistema seguirá uma **arquitetura em camadas**:

- **Camada de Apresentação**: aplicação web (frontend) com tela de chat e dashboard
- **Camada de Serviços / API**: backend em Flask que expõe endpoints REST
- **Camada de Motor de IA**: módulos responsáveis pelo pré-processamento, cálculo de LSM, análise de sentimentos, extração de sinais comportamentais e agregação em score
- **Camada de Persistência**: banco de dados PostgreSQL

### Diagramas C4

O projeto inclui diagramas C4 Model em quatro níveis (disponíveis na documentação):
- Nível 1: Diagrama de Contexto do Sistema
- Nível 2: Diagrama de Contêineres
- Nível 3: Diagrama de Componentes
- Nível 4: Diagrama de Código (módulo de agregação)

Consulte a documentação completa em `Documents/Compatibilidade Conversacional com IA.md`.

## 📦 Requisitos Planejados

Os seguintes requisitos serão necessários quando o projeto entrar em fase de implementação:

- Python 3.12+
- Node.js 22+ LTS (para o frontend)
- PostgreSQL
- Git

## 🚀 Instalação e Uso

> **Nota**: O projeto está atualmente em **fase de documentação**. As instruções de instalação e uso serão adicionadas quando o código for implementado durante o Portfólio II.

As instruções de instalação, configuração e uso serão documentadas conforme o desenvolvimento do projeto progredir.

## 📁 Estrutura do Projeto

Atualmente, o repositório contém apenas a documentação do projeto:

```
Compatibilidade-Conversacional-com-IA/
├── Documents/              # Documentação completa do projeto
│   ├── Compatibilidade Conversacional com IA.md
│   └── images/            # Diagramas C4, casos de uso e fluxos
├── LICENSE                # Licença MIT
└── README.md              # Este arquivo
```

> **Nota**: As pastas `backend/` e `frontend/` serão criadas durante a fase de implementação (Portfólio II).

## 🔒 Segurança e Conformidade

O sistema será projetado e implementado seguindo as seguintes diretrizes de segurança e conformidade:

### LGPD (Lei Geral de Proteção de Dados)

O sistema será projetado para conformidade com a LGPD, incluindo:

- **Consentimento explícito** para coleta e tratamento de dados
- **Minimização de dados**: coleta apenas do necessário
- **Anonimização e pseudonimização** sempre que possível
- **Mecanismos de exclusão** de dados mediante solicitação
- **Transparência** sobre finalidade do tratamento
- **Direitos dos titulares**: acesso, correção, exclusão, portabilidade

### Segurança

- Criptografia em trânsito (HTTPS/TLS)
- Controles de acesso (autenticação e autorização)
- Validação rigorosa de entrada
- Proteção contra injeção SQL
- Logs estruturados para auditoria

### Princípios de IA Responsável

- **Transparência e Explicabilidade**: explicações claras sobre o cálculo do score
- **Justiça e Não Discriminação**: mitigação de vieses
- **Responsabilidade Humana**: o sistema apoia decisões, não as substitui
- **Privacidade**: privacy by design

## ⚠️ Limitações

- Focado em **conversas textuais em português (PT-BR)**
- Não avalia conteúdo temático profundo (veracidade, qualidade argumentativa)
- A qualidade do score depende da quantidade e qualidade dos dados disponíveis
- Versão inicial como **protótipo funcional**, não otimizado para alta escala
- Abordagem inicial **heurística**, com possibilidade de evolução para modelo supervisionado

## 📊 Métricas de Sucesso Planejadas

As seguintes métricas serão utilizadas para validar o sistema:

- **Qualidade do Score**: concordância com avaliação humana, coerência relativa entre diálogos
- **Desempenho Técnico**: tempo de resposta ≤ 3 segundos, confiabilidade básica
- **Usabilidade**: satisfação dos usuários, percepção de valor e transparência
- **Conformidade**: ausência de incidentes de privacidade, funcionamento correto do fluxo de exclusão de dados

## 📝 Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo `LICENSE` para mais detalhes.

## 👤 Autor

**Gabriel de Oliveira**  
Curso: Engenharia de Software  
Data de Entrega: 02/12/2025

## 📚 Referências

- [LGPD - Lei nº 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [OECD AI Principles](https://oecd.ai/en/ai-principles)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [UNESCO - Ética da IA](https://unesdoc.unesco.org/ark:/48223/pf0000380455)

## 📄 Documentação

Para documentação técnica completa, incluindo requisitos funcionais e não funcionais, diagramas de arquitetura, casos de uso, considerações de segurança e conformidade com LGPD, consulte:

**`Documents/Compatibilidade Conversacional com IA.md`**

Este documento contém toda a especificação técnica do projeto, incluindo:
- Requisitos de software (RF01-RF12 e RNF01-RNF08)
- Diagramas C4 Model (4 níveis)
- Diagramas de casos de uso
- Stack tecnológica detalhada
- Considerações de segurança e conformidade
- Próximos passos (Portfólio I e II)