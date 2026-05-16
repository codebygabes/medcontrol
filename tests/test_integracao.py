"""Teste de integração com a API pública OpenFDA."""

from unittest.mock import patch, Mock
import pytest
from medcontrol.app import consultar_api


def _mock_resposta(json_data, status_code=200):
    """Cria um mock de resposta HTTP."""
    mock = Mock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    return mock


# ────────────────────────────────────────────────────────
# Testes de integração (com mock da API)
# ────────────────────────────────────────────────────────

def test_consultar_api_retorna_dados_validos():
    """Integração: API retorna dados e função os processa corretamente."""
    payload = {
        "results": [{
            "openfda": {
                "generic_name": ["Losartan Potassium"],
                "manufacturer_name": ["Merck Sharp & Dohme"],
            },
            "indications_and_usage": ["Used to treat high blood pressure."],
            "warnings": ["Do not use if allergic to losartan."],
        }]
    }
    with patch("medcontrol.app.requests.get", return_value=_mock_resposta(payload)):
        resultado = consultar_api("Losartan")

    assert "erro" not in resultado
    assert resultado["nome_generico"] == "Losartan Potassium"
    assert resultado["fabricante"] == "Merck Sharp & Dohme"


def test_consultar_api_sem_resultados():
    """Integração: API retorna lista vazia, função informa corretamente."""
    payload = {"results": []}
    with patch("medcontrol.app.requests.get", return_value=_mock_resposta(payload)):
        resultado = consultar_api("MedicamentoInexistente")

    assert "erro" in resultado
    assert "MedicamentoInexistente" in resultado["erro"]


def test_consultar_api_status_erro():
    """Integração: API retorna status 500, função trata o erro."""
    with patch("medcontrol.app.requests.get", return_value=_mock_resposta({}, status_code=500)):
        resultado = consultar_api("Qualquer")

    assert "erro" in resultado
    assert "500" in resultado["erro"]


def test_consultar_api_timeout():
    """Integração: timeout de conexão é tratado com mensagem amigável."""
    import requests as req_lib
    with patch("medcontrol.app.requests.get", side_effect=req_lib.exceptions.Timeout):
        resultado = consultar_api("Losartan")

    assert "erro" in resultado
    assert "esgotado" in resultado["erro"].lower()


def test_consultar_api_sem_conexao():
    """Integração: erro de conexão é tratado com mensagem amigável."""
    import requests as req_lib
    with patch("medcontrol.app.requests.get", side_effect=req_lib.exceptions.ConnectionError):
        resultado = consultar_api("Losartan")

    assert "erro" in resultado
    assert "internet" in resultado["erro"].lower()
