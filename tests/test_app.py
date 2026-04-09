"""Testes automatizados para o MedControl."""

import pytest
import json
import os
import tempfile

# Ajusta o DATA_FILE para usar arquivo temporário nos testes
import medcontrol.app as app_module


@pytest.fixture(autouse=True)
def usar_arquivo_temp(tmp_path):
    """Usa um arquivo temporário para os testes, isolando os dados reais."""
    arquivo_temp = tmp_path / "medicamentos_test.json"
    original = app_module.DATA_FILE
    app_module.DATA_FILE = str(arquivo_temp)
    yield
    app_module.DATA_FILE = original


# ────────────────────────────────────────────────────────
# Testes de adicionar
# ────────────────────────────────────────────────────────

def test_adicionar_medicamento_valido():
    """Caminho feliz: adiciona um medicamento com dados corretos."""
    med = app_module.adicionar_medicamento("Losartana", "08:00", "1 comprimido")
    assert med["nome"] == "Losartana"
    assert med["horario"] == "08:00"
    assert med["dose"] == "1 comprimido"
    assert med["id"] == 1


def test_adicionar_dois_medicamentos_ids_distintos():
    """Dois medicamentos devem ter IDs diferentes."""
    m1 = app_module.adicionar_medicamento("Losartana", "08:00", "1 comprimido")
    m2 = app_module.adicionar_medicamento("Metformina", "12:00", "2 comprimidos")
    assert m1["id"] != m2["id"]


def test_adicionar_nome_vazio_levanta_erro():
    """Entrada inválida: nome vazio deve levantar ValueError."""
    with pytest.raises(ValueError, match="Nome"):
        app_module.adicionar_medicamento("", "08:00", "1 comprimido")


def test_adicionar_horario_vazio_levanta_erro():
    """Entrada inválida: horário vazio deve levantar ValueError."""
    with pytest.raises(ValueError, match="Horário"):
        app_module.adicionar_medicamento("Losartana", "", "1 comprimido")


def test_adicionar_dose_vazia_levanta_erro():
    """Entrada inválida: dose vazia deve levantar ValueError."""
    with pytest.raises(ValueError, match="Dose"):
        app_module.adicionar_medicamento("Losartana", "08:00", "")


def test_adicionar_nome_apenas_espacos_levanta_erro():
    """Caso limite: nome com apenas espaços deve ser rejeitado."""
    with pytest.raises(ValueError):
        app_module.adicionar_medicamento("   ", "08:00", "1 comprimido")


# ────────────────────────────────────────────────────────
# Testes de listar
# ────────────────────────────────────────────────────────

def test_listar_retorna_lista_vazia_inicialmente():
    """Lista começa vazia quando não há medicamentos."""
    assert app_module.listar_medicamentos() == []


def test_listar_apos_adicionar():
    """Lista deve conter o medicamento recém-adicionado."""
    app_module.adicionar_medicamento("Atenolol", "07:00", "1 comprimido")
    lista = app_module.listar_medicamentos()
    assert len(lista) == 1
    assert lista[0]["nome"] == "Atenolol"


# ────────────────────────────────────────────────────────
# Testes de remover
# ────────────────────────────────────────────────────────

def test_remover_medicamento_existente():
    """Caminho feliz: remove um medicamento existente e retorna True."""
    med = app_module.adicionar_medicamento("Sinvastatina", "22:00", "1 comprimido")
    resultado = app_module.remover_medicamento(med["id"])
    assert resultado is True
    assert app_module.listar_medicamentos() == []


def test_remover_medicamento_inexistente_retorna_false():
    """Caso limite: tentar remover ID inexistente retorna False."""
    resultado = app_module.remover_medicamento(999)
    assert resultado is False


# ────────────────────────────────────────────────────────
# Testes de buscar
# ────────────────────────────────────────────────────────

def test_buscar_medicamento_encontrado():
    """Busca retorna o medicamento correto."""
    app_module.adicionar_medicamento("Omeprazol", "07:30", "1 cápsula")
    resultados = app_module.buscar_medicamento("omeprazol")
    assert len(resultados) == 1
    assert resultados[0]["nome"] == "Omeprazol"


def test_buscar_case_insensitive():
    """Busca não deve diferenciar maiúsculas de minúsculas."""
    app_module.adicionar_medicamento("Losartana", "08:00", "1 comprimido")
    assert len(app_module.buscar_medicamento("LOSARTANA")) == 1
    assert len(app_module.buscar_medicamento("losartana")) == 1


def test_buscar_medicamento_nao_encontrado():
    """Busca retorna lista vazia quando não há correspondência."""
    app_module.adicionar_medicamento("Losartana", "08:00", "1 comprimido")
    resultados = app_module.buscar_medicamento("aspirina")
    assert resultados == []


def test_buscar_retorna_multiplos_resultados():
    """Busca parcial retorna todos os medicamentos correspondentes."""
    app_module.adicionar_medicamento("Losartana", "08:00", "1 comprimido")
    app_module.adicionar_medicamento("Losartana Potássica", "20:00", "1 comprimido")
    resultados = app_module.buscar_medicamento("losart")
    assert len(resultados) == 2
