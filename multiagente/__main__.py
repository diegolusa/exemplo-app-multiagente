#!/usr/bin/env python3
"""
Sistema Multiagente com LLMs - Assistente Acadêmico

Demonstração de uma arquitetura multiagente para suporte acadêmico usando:
- LangGraph e LangChain para orquestração
- RAG com ChromaDB e embeddings para recuperação de informações
- Modelos locais via Ollama
- Múltiplos agentes especializados
"""

import sys
from multiagente.agents.agents import MultiAgentOrchestrator


def print_header():
    print("\n" + "=" * 70)
    print(" " * 15 + "ASSISTENTE ACADÊMICO MULTIAGENTE")
    print("=" * 70)
    print("\nSistema inteligente com múltiplos agentes para apoio acadêmico")
    print("Arquitetura: Planejador → Recuperador → Executor → Revisor\n")


def print_menu():
    print("\n" + "-" * 70)
    print("OPÇÕES:")
    print("  1. Fazer uma pergunta (modo interativo)")
    print("  4. Sair")
    print("-" * 70)

def interactive_mode(orchestrator: MultiAgentOrchestrator):
    print("\n" + "=" * 70)
    print("MODO INTERATIVO - Faça suas perguntas acadêmicas")
    print("Digite 'sair' para voltar ao menu principal")
    print("=" * 70 + "\n")

    while True:
        try:
            query = input("Sua pergunta: ").strip()

            if query.lower() in ["sair", "exit", "quit"]:
                break

            if not query:
                print("Digite uma pergunta válida\n")
                continue

            print("\nProcessando sua pergunta...")
            result = orchestrator.process_query(query, verbose=True)

            print("\n" + "=" * 70)
            print("RESULTADO FINAL")
            print("=" * 70)

            if result.get("status") == "success":
                print("\nRESPOSTA:")
                print("-" * 70)
                print(result.get("final_response", "Sem resposta"))

                print("\nAVALIAÇÃO DE QUALIDADE:")
                print("-" * 70)
                print(result.get("quality_assessment", "Sem avaliação"))
            else:
                print(f"Erro: {result.get('message', 'Erro desconhecido')}")

            print()

        except KeyboardInterrupt:
            print("\n\nInterrompido pelo usuário")
            break
        except Exception as e:
            print(f"Erro: {str(e)}")
            print("Tente novamente\n")




def main():
    print_header()

    try:
        orchestrator = MultiAgentOrchestrator()
    except Exception as e:
        print(f"Erro ao inicializar: {str(e)}")
        sys.exit(1)

    while True:
        print_menu()
        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            interactive_mode(orchestrator)
        elif choice == "4":
            sys.exit(0)
        else:
            print("Opção inválida")


if __name__ == "__main__":
    main()
