# Assistente Acadêmico Multiagente

Um sistema inteligente que demonstra a integração prática de **arquitetura multiagente**, **RAG (Retrieval-Augmented Generation)**, **embeddings vetoriais** e **modelos de linguagem locais**.

## Visão Geral

Este projeto implementa um assistente acadêmico baseado em **múltiplos agentes especializados** que trabalham em coordenação para responder perguntas e fornecer orientações sobre tópicos acadêmicos.

### Objetivos Alcançados

**Arquitetura Multiagente**: 4 agentes especializados (Planejador, Recuperador, Executor, Revisor)  
**RAG com Embeddings**: Sistema de recuperação de informações com busca semântica  
**Modelos Locais**: Integração com Ollama para execução local de LLaMA  
**Tools e MCP**: Ferramentas acionáveis pelos agentes  
**Interface Terminal**: Menu interativo para uso do sistema  
**Base de Conhecimento**: 6 documentos acadêmicos indexados  

## Arquitetura

### Agentes Especializados

```
┌─────────────────────────────────────────────────────────────┐
│                    CONSULTA DO USUÁRIO                       │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. PLANEJADOR - Decomposição de Tarefas                     │
│    Entrada: Consulta                                         │
│    Saída: Plano estruturado                                  │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. RECUPERADOR (RAG) - Busca de Informações                 │
│    Entrada: Consulta                                         │
│    Saída: Documentos relevantes + Contexto                   │
│    Tecnologia: ChromaDB + Sentence Transformers              │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. EXECUTOR - Geração de Resposta com Contexto              │
│    Entrada: Consulta + Contexto recuperado                   │
│    Saída: Resposta estruturada                               │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. REVISOR - Validação de Qualidade                         │
│    Entrada: Resposta gerada                                  │
│    Saída: Avaliação e sugestões de melhoria                  │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
        RESPOSTA FINAL
```

### Componentes Principais

1. **Agentes LLM** (`agents.py`)
   - PlannerAgent: Decompõe problemas em etapas
   - RecoveryAgent: Recupera informações via RAG
   - ExecutorAgent: Gera respostas com contexto
   - ReviewerAgent: Valida qualidade das respostas

2. **Sistema de RAG** (`rag.py`)
   - Embeddings: Sentence Transformers (All-MiniLM-L6-v2)
   - Armazenamento: ChromaDB com busca vetorial
   - Indexação: Todos os documentos da base de conhecimento
   - Recuperação: Top-k com scoring de relevância

3. **Ferramentas** (`tools.py`)
   - `search_knowledge_base`: Busca semântica em documentos
   - `get_context_for_query`: Recupera contexto formatado
   - `search_by_category`: Filtro por categorias
   - `validate_query`: Validação de entrada do usuário
   - `summarize_results`: Sumarização de resultados

4. **Base de Conhecimento** (`knowledge_base.py`)
   - 6 documentos sobre tópicos acadêmicos
   - Categorias: mathematics, programming, ai, tools, data_science, study_tips
   - Estrutura: id, title, content, category

## Tecnologias Utilizadas

- **LangChain**: Framework para aplicações com LLMs
- **LangGraph**: Orquestração de agentes
- **Ollama**: Execução local de modelos LLaMA
- **ChromaDB**: Banco de dados vetorial
- **Sentence Transformers**: Geração de embeddings
- **Python 3.10+**: Linguagem de programação

## Instalação

### Pré-requisitos

1. **Python 3.10+**
2. **Ollama** (download em https://ollama.ai)
3. **Modelo llama2** (download via `ollama pull llama2`)


### Configuração do Ollama

```bash
# Verificar se Ollama está instalado
ollama --version

# Baixar o modelo llama2 (primeira execução)
ollama pull llama2

# Iniciar servidor Ollama
ollama serve
# Servidor rodará em http://localhost:11434
```


### Configuração do Projeto

```bash

# Entrar no diretório
cd exemplo-app-multiagente

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou: venv\Scripts\activate  # Windows


# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor Ollama (em outro terminal)
ollama serve

# Executar o servidor MCP
python -m multiagente.mcp.mcp_server

# Executar a aplicação
python -m multiagente
```

