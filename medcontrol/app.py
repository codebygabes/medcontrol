"""MedControl - Controle de Medicamentos para Idosos."""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "medicamentos.json")


def carregar_dados() -> list:
    """Carrega os medicamentos do arquivo JSON."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def salvar_dados(medicamentos: list) -> None:
    """Salva os medicamentos no arquivo JSON."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(medicamentos, f, ensure_ascii=False, indent=2)


def adicionar_medicamento(nome: str, horario: str, dose: str) -> dict:
    """Adiciona um novo medicamento à lista."""
    if not nome or not nome.strip():
        raise ValueError("Nome do medicamento não pode ser vazio.")
    if not horario or not horario.strip():
        raise ValueError("Horário não pode ser vazio.")
    if not dose or not dose.strip():
        raise ValueError("Dose não pode ser vazia.")

    medicamentos = carregar_dados()
    medicamento = {
        "id": len(medicamentos) + 1,
        "nome": nome.strip(),
        "horario": horario.strip(),
        "dose": dose.strip(),
        "criado_em": datetime.now().isoformat(),
    }
    medicamentos.append(medicamento)
    salvar_dados(medicamentos)
    return medicamento


def listar_medicamentos() -> list:
    """Retorna a lista de todos os medicamentos."""
    return carregar_dados()


def remover_medicamento(med_id: int) -> bool:
    """Remove um medicamento pelo ID. Retorna True se removido."""
    medicamentos = carregar_dados()
    novos = [m for m in medicamentos if m["id"] != med_id]
    if len(novos) == len(medicamentos):
        return False
    salvar_dados(novos)
    return True


def buscar_medicamento(nome: str) -> list:
    """Busca medicamentos pelo nome (case-insensitive)."""
    medicamentos = carregar_dados()
    return [m for m in medicamentos if nome.lower() in m["nome"].lower()]


def menu():
    """Exibe o menu principal da aplicação."""
    print("\n╔══════════════════════════════════╗")
    print("║   💊 MedControl v1.0.0           ║")
    print("║   Controle de Medicamentos        ║")
    print("╚══════════════════════════════════╝")
    print("1. Adicionar medicamento")
    print("2. Listar medicamentos")
    print("3. Buscar medicamento")
    print("4. Remover medicamento")
    print("0. Sair")
    print("─" * 36)


def run():
    """Ponto de entrada principal da aplicação CLI."""
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do medicamento: ")
            horario = input("Horário (ex: 08:00): ")
            dose = input("Dose (ex: 1 comprimido): ")
            try:
                med = adicionar_medicamento(nome, horario, dose)
                print(f"\n✅ Medicamento '{med['nome']}' adicionado com sucesso!")
            except ValueError as e:
                print(f"\n❌ Erro: {e}")

        elif opcao == "2":
            medicamentos = listar_medicamentos()
            if not medicamentos:
                print("\n📋 Nenhum medicamento cadastrado.")
            else:
                print(f"\n📋 Medicamentos cadastrados ({len(medicamentos)}):")
                print("─" * 50)
                for m in medicamentos:
                    print(f"  [{m['id']}] {m['nome']} | {m['horario']} | {m['dose']}")

        elif opcao == "3":
            nome = input("Digite o nome para buscar: ")
            resultados = buscar_medicamento(nome)
            if not resultados:
                print(f"\n🔍 Nenhum medicamento encontrado para '{nome}'.")
            else:
                print(f"\n🔍 Encontrado(s) {len(resultados)} resultado(s):")
                for m in resultados:
                    print(f"  [{m['id']}] {m['nome']} | {m['horario']} | {m['dose']}")

        elif opcao == "4":
            try:
                med_id = int(input("Digite o ID do medicamento a remover: "))
                if remover_medicamento(med_id):
                    print(f"\n✅ Medicamento ID {med_id} removido com sucesso!")
                else:
                    print(f"\n❌ Medicamento ID {med_id} não encontrado.")
            except ValueError:
                print("\n❌ ID inválido. Digite um número.")

        elif opcao == "0":
            print("\n👋 Até logo!")
            break

        else:
            print("\n⚠️  Opção inválida. Tente novamente.")


if __name__ == "__main__":
    run()
