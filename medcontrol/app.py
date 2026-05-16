"""MedControl - Controle de Medicamentos para Idosos."""

import json
import os
from datetime import datetime

import requests

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "medicamentos.json")
OPENFDA_URL = "https://api.fda.gov/drug/label.json"


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


def consultar_api(nome: str) -> dict:
    """Consulta informações de um medicamento na API pública OpenFDA.

    Retorna um dicionário com as informações encontradas ou mensagem de erro.
    """
    try:
        response = requests.get(
            OPENFDA_URL,
            params={"search": f"openfda.brand_name:{nome}", "limit": 1},
            timeout=5,
        )
        if response.status_code != 200:
            return {"erro": f"API retornou status {response.status_code}."}

        data = response.json()
        resultados = data.get("results", [])
        if not resultados:
            return {"erro": f"Nenhuma informação encontrada para '{nome}' na OpenFDA."}

        resultado = resultados[0]
        openfda = resultado.get("openfda", {})

        return {
            "nome_generico": openfda.get("generic_name", ["N/A"])[0],
            "fabricante": openfda.get("manufacturer_name", ["N/A"])[0],
            "uso": resultado.get("indications_and_usage", ["N/A"])[0][:300] + "...",
            "advertencias": resultado.get("warnings", ["N/A"])[0][:300] + "...",
        }
    except requests.exceptions.Timeout:
        return {"erro": "Tempo de conexão esgotado. Verifique sua internet."}
    except requests.exceptions.ConnectionError:
        return {"erro": "Sem conexão com a internet."}
    except Exception as e:
        return {"erro": f"Erro inesperado: {e}"}


def buscar_medicamento(nome: str) -> list:
    """Busca medicamentos pelo nome (case-insensitive)."""
    medicamentos = carregar_dados()
    return [m for m in medicamentos if nome.lower() in m["nome"].lower()]


def menu():
    """Exibe o menu principal da aplicação."""
    print("\n╔══════════════════════════════════╗")
    print("║   💊 MedControl v1.1.0           ║")
    print("║   Controle de Medicamentos        ║")
    print("╚══════════════════════════════════╝")
    print("1. Adicionar medicamento")
    print("2. Listar medicamentos")
    print("3. Buscar medicamento")
    print("4. Remover medicamento")
    print("5. Consultar informações na OpenFDA")
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

        elif opcao == "5":
            nome = input("Digite o nome do medicamento para consultar na OpenFDA: ")
            print("\n🌐 Consultando API OpenFDA...")
            info = consultar_api(nome)
            if "erro" in info:
                print(f"\n❌ {info['erro']}")
            else:
                print("\n📋 Informações encontradas:")
                print("─" * 50)
                print(f"  Nome genérico : {info['nome_generico']}")
                print(f"  Fabricante    : {info['fabricante']}")
                print(f"  Indicações    : {info['uso']}")
                print(f"  Advertências  : {info['advertencias']}")

        elif opcao == "0":
            print("\n👋 Até logo!")
            break

        else:
            print("\n⚠️  Opção inválida. Tente novamente.")


if __name__ == "__main__":
    run()
