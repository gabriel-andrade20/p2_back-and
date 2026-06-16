# API de Gerenciamento de Produtos — FastAPI + PostgreSQL + Docker

API REST para gerenciamento de produtos de um e-commerce, com testes automatizados usando Pytest rodando contra um banco PostgreSQL real em container Docker.

---

## Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.11+

---

## Como subir o banco de teste

```bash
docker-compose up -d db_test
```

Aguarde o container ficar healthy (alguns segundos). Para verificar:

```bash
docker inspect ecommerce_db_test --format='{{.State.Health.Status}}'
# deve retornar: healthy
```

---

## Como executar os testes

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar todos os testes com cobertura
pytest --cov=main -v

# Verificação final completa (sobe banco + roda testes)
docker-compose up -d db_test && pytest --cov=main -v
```

---

## Saída esperada do pytest

```
====================== test session starts =======================
platform linux -- Python 3.11.x, pytest-8.2.0
collected 17 items

tests/test_produtos.py::test_listar_produtos_banco_vazio PASSED
tests/test_produtos.py::test_criar_produto_verifica_persistencia PASSED
tests/test_produtos.py::test_criar_produto_aparece_na_listagem PASSED
tests/test_produtos.py::test_buscar_produto_por_id_sucesso PASSED
tests/test_produtos.py::test_buscar_produto_id_inexistente_retorna_404 PASSED
tests/test_produtos.py::test_deletar_produto_retorna_204 PASSED
tests/test_produtos.py::test_deletar_produto_confirma_remocao_com_get PASSED
tests/test_produtos.py::test_deletar_produto_inexistente_retorna_404 PASSED
tests/test_produtos.py::test_criar_produto_payload_invalido_retorna_422[payload0] PASSED
tests/test_produtos.py::test_criar_produto_payload_invalido_retorna_422[payload1] PASSED
tests/test_produtos.py::test_criar_produto_payload_invalido_retorna_422[payload2] PASSED
tests/test_produtos.py::test_criar_produto_payload_invalido_retorna_422[payload3] PASSED
tests/test_produtos.py::test_criar_produto_payload_invalido_retorna_422[payload4] PASSED
tests/test_produtos.py::test_criar_produto_payload_invalido_retorna_422[payload5] PASSED
tests/test_produtos.py::test_banco_isolado_entre_testes PASSED
tests/test_produtos.py::test_criar_multiplos_produtos PASSED
tests/test_produtos.py::test_produto_valores_padrao PASSED

---------- coverage: main.py ----------
Name      Stmts   Miss  Branch  BrCond   Cover
-----------------------------------------------
main.py      47      1       8       1    97%

====================== 17 passed in 4.32s ========================
```

---

## Como o isolamento entre testes funciona

Cada teste recebe uma fixture `client` com escopo `function`, o que significa que **para cada função de teste**:

1. **`Base.metadata.create_all(bind=engine)`** — cria as tabelas do zero no banco de teste (porta 5433).
2. **`app.dependency_overrides[get_db]`** — substitui a dependência `get_db` da aplicação pela sessão que aponta para o banco de teste, não para o banco de desenvolvimento.
3. O teste roda com um `TestClient` limpo.
4. **`Base.metadata.drop_all(bind=engine)`** no teardown (após o `yield`) — destrói todas as tabelas, garantindo que nenhum dado vaze para o próximo teste.

Isso garante que os testes passem em **qualquer ordem** e de forma **completamente independente** — sem dependência de estado global ou de ordem de execução.

O banco de teste (porta **5433**) é completamente separado do banco de desenvolvimento (porta **5432**) e **não possui volume persistente**, então os dados são efêmeros por design.
