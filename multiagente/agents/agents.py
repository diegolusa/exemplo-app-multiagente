"""Definição dos agentes e fluxo de coordenação com LangGraph."""

from typing import Any, Dict, Optional
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from multiagente.config.config import Config
from multiagente.mcp.mcp_client import MCPClient
from multiagente.mcp.tools import ToolRegistry
import asyncio

class PlannerAgent:
    """Agente Planejador - decomposição de tarefas e planejamento."""

    def __init__(self):
        """Inicializa o agente planejador."""
        model_config = Config.get_model_config()
        self.llm = ChatOllama(
            model=model_config["model"],
            base_url=model_config["base_url"],
            temperature=0.3,
        )
        self.name = "Planejador"

    def plan(self, user_query: str) -> Dict[str, Any]:
        """
        Decompõe uma tarefa em etapas.

        Args:
            user_query: consulta do usuário

        Returns:
            plano estruturado com passos
        """
        prompt = f"""Você é um agente especializado em planejamento de tarefas acadêmicas.

                Sua tarefa é analisar a seguinte consulta e criar um plano estruturado:

                CONSULTA: `{user_query}`

                Analise a consulta e forneça:
                1. Uma descrição breve do que o usuário quer
                2. Uma lista de 3-5 etapas para resolver a tarefa
                3. Quais ferramentas podem ser úteis (search_knowledge_base, get_context_for_query, etc)
                4. Prioridade de execução

                Responda em formato estruturado."""

        messages = [HumanMessage(content=prompt)]

        try:
            response = self.llm.invoke(messages)
            return {
                "status": "success",
                "agent": self.name,
                "plan": response.content,
                "query": user_query
            }
        except Exception as e:
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e)
            }


class RecoveryAgent:
    """Agente Recuperador - recuperação de informações com RAG."""

    def __init__(self):
        """Inicializa o agente recuperador."""
        self.mcp_client = MCPClient()
        self.name = "Recuperador"

    def retrieve(self, query: str, strategy: str = "search") -> Dict[str, Any]:
        """
        Recupera informações relevantes.

        Args:
            query: consulta para recuperação
            strategy: estratégia de recuperação (search, context, category)

        Returns:
            informações recuperadas
        """
        if strategy == "search":
            result = asyncio.run( self.mcp_client.call_tool('search_knowledge_base',query=query, top_k=5))
        elif strategy == "context":
            result = asyncio.run(self.mcp_client.call_tool('get_context_for_query', query=query))

        elif strategy == "category":
            result = asyncio.run(self.mcp_client.call_tool('search_by_category', query=query))
        else:
            result = asyncio.run(self.mcp_client.call_tool('search_knowledge_base', query=query))


        return {
            "status": result.get("status"),
            "agent": self.name,
            "strategy": strategy,
            "result": result,
            "nr_documents": result.get("nr_documents", 0) if result.get("status") == "success" else 0
        }


class ExecutorAgent:
    """Agente Executor - execução com contexto recuperado."""

    def __init__(self):
        """Inicializa o agente executor."""
        model_config = Config.get_model_config()
        self.llm = ChatOllama(
            model=model_config["model"],
            base_url=model_config["base_url"],
            temperature=0.5,
        )

        self.__mcp_client = MCPClient()
        self.name = "Executor"

    def execute(self, query: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Executa a tarefa com contexto recuperado.

        Args:
            query: consulta a executar
            context: contexto opcional já recuperado

        Returns:
            resultado da execução
        """
        if context is None:
            context = asyncio.run(self.__mcp_client.call_tool('get_context_for_query', query=query)).get("context", "Contexto não disponível")

        prompt = f"""Você é um agente especializado em responder questões acadêmicas de usuários com base nos regulamentos oficiais providos como contexto.

                    1 - CONSULTA DO USUÁRIO: 
                    ###
                        {query}
                    ###

                    2- CONTEXTO RELEVANTE DA BASE DE CONHECIMENTO:
                    
                    ###
                    {context}
                    ###
                    
                    3 - INVARIANTES
                    - CONSIDERE que ### são delimitadores e tudo entre eles é parte do contexto ou da consulta.
                    - CONSIDERANDO SOMENTE o contexto fornecido para responder a consulta do usuário
                    - ELABORE uma resposta clara e estruturada para a consulta, indicando as referências utilizadas.
                    - NÃO UTILIZE INFORMAÇÕES FORA DO CONTEXTO ao responder.
                    - NÃO FAÇA SUPOSICÕES OU INFERÊNCIAS.
                    - SE NÃO HOUVER RESPOSTA, INFORME APENAS `Desculpe, não tenho informações suficientes para responder a essa consulta com base no contexto fornecido.`
                """

        messages = [HumanMessage(content=prompt)]

        try:
            response = self.llm.invoke(messages)
            return {
                "status": "success",
                "agent": self.name,
                "response": response.content,
                "query": query,
                "context_used": len(context) > 0
            }
        except Exception as e:
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e)
            }


class ReviewerAgent:
    """Agente Revisor - validação e melhoria de respostas."""

    def __init__(self):
        """Inicializa o agente revisor."""
        model_config = Config.get_model_config()
        self.llm = ChatOllama(
            model=model_config["model"],
            base_url=model_config["base_url"],
            temperature=0.3,
        )
        self.name = "Revisor"

    def review(self, response: str, original_query: str) -> Dict[str, Any]:
        """
        Revisa uma resposta para qualidade.

        Args:
            response: resposta a revisar
            original_query: consulta original

        Returns:
            avaliação e sugestões
        """
        prompt = f"""Você é um agente especializado em revisar respostas acadêmicas.

                    CONSULTA ORIGINAL: `{original_query}`

                    RESPOSTA A REVISAR:
                    `{response}`

                    Avalie a resposta considerando:
                    1. Clareza e compreensibilidade
                    2. Correção técnica
                    3. Completude (responde totalmente à consulta?)
                    4. Estrutura e organização
                    5. Oportunidades de melhoria

                    Forneça:
                    - Uma avaliação global (excelente/bom/razoável/pobre)
                    - Pontos fortes
                    - Áreas para melhoria
                    - Sugestões específicas de revisão, se necessário"""

        messages = [HumanMessage(content=prompt)]

        try:
            response_review = self.llm.invoke(messages)
            return {
                "status": "success",
                "agent": self.name,
                "review": response_review.content,
                "query": original_query
            }
        except Exception as e:
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e)
            }


class MultiAgentOrchestrator:
    """Orquestrador de agentes - coordena fluxo entre agentes."""

    def __init__(self):
        """Inicializa os agentes."""
        self.planner = PlannerAgent()
        self.recovery = RecoveryAgent()
        self.executor = ExecutorAgent()
        self.reviewer = ReviewerAgent()
        self.__mcp_client = MCPClient()


    def process_query(self, user_query: str, verbose: bool = False) -> Dict[str, Any]:
        """
        Processa uma consulta através do pipeline de agentes.

        Args:
            user_query: consulta do usuário
            verbose: se True, mostra etapas intermediárias

        Returns:
            resposta final estruturada
        """
        if verbose:
            print("\n" + "=" * 60)
            print(f"CONSULTA: {user_query}")
            print("=" * 60)

        # Validar consulta
        validation = asyncio.run(self.__mcp_client.call_tool('validate_query',query = user_query))
        if validation["status"] == "invalid":
            return {
                "status": "error",
                "message": "Consulta inválida",
                "issues": validation["issues"]
            }

        # Etapa 1: Planejamento
        if verbose:
            print("\n[1/4] PLANEJADOR - Decomposição da tarefa...")
        plan_result = self.planner.plan(user_query)

        if verbose and plan_result.get("status") == "success":
            print(f"✓ Plano gerado:\n{plan_result['plan'][:200]}...")

        # Etapa 2: Recuperação
        if verbose:
            print("\n[2/4] RECUPERADOR - Busca de informações relevantes...")
        recovery_result = self.recovery.retrieve(user_query, strategy="context")

        if verbose:
            print(f"{recovery_result['nr_documents']} documentos recuperados")

        # Obter contexto
        context = recovery_result.get("result", {}).get("context", "")

        # Etapa 3: Execução
        if verbose:
            print("\n[3/4] EXECUTOR - Processamento com contexto...")
        executor_result = self.executor.execute(user_query, context=context)

        if verbose and executor_result.get("status") == "success":
            print(f"Resposta gerada:\n{executor_result['response'][:200]}...")

        # Etapa 4: Revisão
        if verbose:
            print("\n[4/4] REVISOR - Validação de qualidade...")

        response_text = executor_result.get("response", "")
        review_result = self.reviewer.review(response_text, user_query)

        if verbose and review_result.get("status") == "success":
            print(f"Revisão concluída:\n{review_result['review'][:200]}...")

        # Compilar resultado final
        final_result = {
            "status": "success",
            "query": user_query,
            "stages": {
                "planning": plan_result,
                "recovery": recovery_result,
                "execution": executor_result,
                "review": review_result
            },
            "final_response": executor_result.get("response", ""),
            "quality_assessment": review_result.get("review", "")
        }

        return final_result
