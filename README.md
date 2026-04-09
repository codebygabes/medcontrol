# 💊 MedControl

> Controle de medicamentos para idosos via linha de comando (CLI).

![CI](https://github.com/SEU_USUARIO/medcontrol/actions/workflows/ci.yml/badge.svg)
![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)

---

## 🎯 Problema Real

Idosos frequentemente precisam tomar múltiplos medicamentos em horários diferentes ao longo do dia. Esquecer um remédio ou tomar a dose errada pode causar sérios problemas de saúde. Cuidadores e familiares também têm dificuldade de acompanhar essa rotina.

## 💡 Proposta da Solução

O **MedControl** é uma aplicação de linha de comando simples que permite **cadastrar, listar, buscar e remover medicamentos** com seus respectivos horários e doses. O objetivo é oferecer um registro rápido e acessível para o próprio idoso, familiar ou cuidador.

## 👥 Público-Alvo

- Idosos que gerenciam seus próprios medicamentos
- Cuidadores e familiares responsáveis pela saúde de idosos
- Profissionais de saúde em contexto domiciliar

## ✨ Funcionalidades

- ➕ Adicionar medicamento com nome, horário e dose
- 📋 Listar todos os medicamentos cadastrados
- 🔍 Buscar medicamento por nome (busca parcial e case-insensitive)
- 🗑️ Remover medicamento pelo ID
- 💾 Persistência dos dados em arquivo JSON local

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **pytest** — testes automatizados
- **ruff** — linting e análise estática
- **GitHub Actions** — integração contínua (CI)
- **JSON** — armazenamento local dos dados

## 📁 Estrutura do Projeto

```
medcontrol/
├── medcontrol/
│   ├── __init__.py
│   └── app.py          # Lógica principal e CLI
├── tests/
│   ├── __init__.py
│   └── test_app.py     # Testes automatizados
├── data/               # Criado automaticamente
│   └── medicamentos.json
├── .github/
│   └── workflows/
│       └── ci.yml      # Pipeline de CI
├── pyproject.toml      # Dependências e configuração
└── README.md
```

## ⚙️ Instalação

**Pré-requisito:** Python 3.10 ou superior instalado.

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/medcontrol.git
cd medcontrol

# Instale o projeto com dependências de desenvolvimento
pip install -e ".[dev]"
```

## ▶️ Execução

```bash
# Pelo script instalado
medcontrol

# Ou diretamente
python -m medcontrol.app
```

**Exemplo de uso:**

```
╔══════════════════════════════════╗
║   💊 MedControl v1.0.0           ║
║   Controle de Medicamentos        ║
╚══════════════════════════════════╝
1. Adicionar medicamento
2. Listar medicamentos
3. Buscar medicamento
4. Remover medicamento
0. Sair
────────────────────────────────────
Escolha uma opção: 1
Nome do medicamento: Losartana
Horário (ex: 08:00): 08:00
Dose (ex: 1 comprimido): 1 comprimido

✅ Medicamento 'Losartana' adicionado com sucesso!
```

## 🧪 Executar os Testes

```bash
pytest
```

Saída esperada:

```
tests/test_app.py ...............                             [100%]
15 passed in 0.12s
```

## 🔍 Executar o Lint

```bash
ruff check medcontrol/ tests/
```

Saída esperada (sem erros):

```
All checks passed!
```

## 📦 Versão

**1.0.0** — Versão inicial com funcionalidades CRUD básicas.

Segue o padrão [Semantic Versioning](https://semver.org/lang/pt-BR/):
- **MAJOR**: mudanças incompatíveis
- **MINOR**: novas funcionalidades compatíveis
- **PATCH**: correções menores

## 👤 Autor

**João Gabriel dos Santos Felipe*  
Disciplina: Bootcamp  
Repositório: https://github.com/codebygabes/medcontrol

## 📄 Licença

Este projeto está sob a licença MIT.
