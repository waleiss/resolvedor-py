# Resolvedor de Lógica
## Informações do Projeto

**Disciplina**: Tópicos em Sistemas Tutores Inteligentes  
**Professor**: Dr. Evandro de Barros Costa  
**Curso**: Ciência da Computação  
**Universidade**: Universidade Federal de Alagoas (UFAL)  

### Alunos Responsáveis
- **Daniel José da Silva**
- **Wallace Lins Casado de Sousa**
- **Itallo Ramon Veiga Paranhos**

---

## Objetivo do Projeto

Este projeto implementa um sistema educacional para ensino e aprendizado de lógica, oferecendo duas funcionalidades principais:

1. **Resolvedor Automático**: Resolve problemas de inferência lógica automaticamente, demonstrando os passos necessários para chegar à conclusão
2. **Avaliador de Soluções**: Avalia soluções propostas por estudantes, identificando erros e fornecendo feedback educativo

O sistema combina técnicas de inteligência artificial com abordagens pedagógicas para criar uma ferramenta completa de ensino de lógica formal.

## Propósito

O projeto tem como finalidade:

- **Auxiliar estudantes** no aprendizado de lógica através de resolução automática de problemas
- **Avaliar conhecimento** dos alunos através da análise de suas soluções
- **Fornecer feedback educativo** personalizado usando LLM (Large Language Model)
- **Demonstrar aplicação prática** de sistemas baseados em conhecimento na educação

## Arquitetura do Sistema

### Módulos Implementados

#### 1. Módulo Especialista
- **Base de Conhecimento**: Implementa 18 regras de inferência da lógica
- **Engenho de Inferência**: Controlador que aplica as regras sequencialmente para resolver problemas
- **Regras disponíveis**:
  - Modus Ponens, Modus Tollens
  - Silogismo Disjuntivo, Silogismo Hipotético
  - Adição, Simplificação, Conjunção
  - De Morgan, Dupla Negação, Transposição
  - Implicação Material, Associatividade, Comutatividade
  - Distributividade, Dilema Construtivo, Exportação
  - Introdução/Dissociação da Bi-implicação

#### 2. Modelo Pedagógico
- **Sistema de Feedback**: Utiliza LLM (Gemini) para gerar feedback educativo personalizado
- **Análise de Erros**: Identifica automaticamente erros nas soluções dos estudantes
- **Feedback Estruturado**: Apresenta erro principal, conceito a revisar e como corrigir

#### 3. Modelo do Estudante
- **Avaliador de Desempenho**: Contabiliza acertos e erros nas soluções
- **Estatísticas**: Calcula taxa de sucesso e identifica padrões de erro
- **Potencial para Adaptação**: Base para implementar sistemas adaptativos baseados no desempenho

#### 4. Estrutura de Tópicos e Questões
- **Questões de Teste**: Conjunto de problemas armazenados para teste manual
- **Diferentes Níveis**: Problemas de complexidade variada para diferentes níveis de aprendizado

## Como Usar

### Interface Web (Recomendado)

1. **Resolvedor Automático**:
   - Acesse a interface web
   - Adicione premissas uma por uma
   - Digite a conclusão desejada
   - Clique em "Resolver" para ver a solução passo a passo

2. **Avaliador de Soluções**:
   - Vá para a aba "Avaliador"
   - Digite as premissas e conclusão
   - Adicione sua solução passo a passo
   - Clique em "Avaliar solução" para receber feedback

### API REST

#### Endpoint: `/solvejson` (POST)
Resolve problemas automaticamente:

```json
{
  "sentences": ["P → Q", "P"],
  "conclusion": "Q"
}
```

#### Endpoint: `/evaluatejson` (POST)
Avalia soluções de estudantes:

```json
{
  "premises": ["P → Q", "P"],
  "conclusion": "Q",
  "inferences": [
    "(1)  Q  Modus Ponens  1, 2"
  ]
}
```

### Linha de Comando

Execute o arquivo `run_solver.py` para interface interativa:

```bash
python run_solver.py
```

## Exemplos de Uso

### Exemplo 1: Modus Ponens Básico
**Premissas**: P → Q, P
**Conclusão**: Q
**Solução**: Q (Modus Ponens, 1, 2)

### Exemplo 2: Modus Tollens
**Premissas**: P → Q, ¬Q
**Conclusão**: ¬P
**Solução**: ¬P (Modus Tollens, 1, 2)

### Exemplo 3: Silogismo Hipotético
**Premissas**: P → Q, Q → R
**Conclusão**: P → R
**Solução**: P → R (Silogismo Hipotético, 1, 2)

### Exemplo 4: Problema Complexo
**Premissas**: (P ∨ Q) → R, P, ¬R
**Conclusão**: ¬Q
**Solução automática**:
1. P ∨ Q (Adição, 2)
2. R (Modus Ponens, 1, 4)
3. Contradição detectada, aplicar Modus Tollens
4. ¬(P ∨ Q) (Modus Tollens, 1, 3)
5. ¬P ∧ ¬Q (De Morgan, 5)
6. ¬Q (Simplificação, 6)

## Feedback Educativo

O sistema fornece feedback automático quando detecta erros nas soluções:

### Exemplo de Solução Incorreta
```json
{
  "premises": ["P → Q", "¬Q"],
  "conclusion": "¬P",
  "inferences": [
    "(1)  ¬P  Modus Ponens  1, 2"
  ]
}
```

**Feedback gerado**:
```
ERRO PRINCIPAL:
- Modus Ponens usado incorretamente
- Modus Ponens requer P → Q e P para concluir Q, mas você tem ¬Q

CONCEITO A REVISAR:
- Modus Tollens
- Quando temos P → Q e ¬Q, podemos concluir ¬P

COMO CORRIGIR:
- Use Modus Tollens em vez de Modus Ponens
- Aplicação: De "P → Q" e "¬Q", conclua "¬P"
```

### Exemplo de Solução Correta
```json
{
  "premises": ["P → Q", "P"],
  "conclusion": "Q",
  "inferences": [
    "(1)  Q  Modus Ponens  1, 2"
  ]
}
```

**Resultado**: ✅ Todas as inferências estão corretas! Parabéns!

## Tecnologias Utilizadas

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **IA**: Google Gemini API para feedback educativo
- **Lógica**: Sistema de regras customizado
- **API**: RESTful endpoints para integração

## Configuração

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure a API key do Gemini no arquivo `config.py`
4. Execute o servidor: `python app.py`
5. Acesse `http://localhost:5000` para usar a interface web

## Contribuições

O projeto está aberto para contribuições, especialmente nas áreas de:
- Implementação de mais regras de inferência
- Melhorias na interface do usuário
- Expansão do sistema de feedback
- Implementação de estatísticas avançadas do modelo do estudante

## Conclusão

Este sistema representa uma implementação prática de um tutor inteligente para lógica, combinando técnicas clássicas de IA simbólica com tecnologias modernas de processamento de linguagem natural. A ferramenta serve tanto como auxílio educacional quanto como demonstração das possibilidades da aplicação de IA na educação formal.

O projeto pode ser expandido para incluir lógica de predicados, sistemas de recomendação adaptativos e integração com plataformas educacionais existentes.
