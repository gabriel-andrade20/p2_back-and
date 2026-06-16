# p2_back-and

API de gerenciamento de produtos com FastAPI, PostgreSQL e Docker.

## Como rodar

Suba o banco de teste:
```
docker-compose up -d db_test
```

Instale as dependências:
```
pip install -r requirements.txt
```

Rode os testes:
```
pytest --cov=main -v
```

## Saída esperada

```
====================== test session starts =======================
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
Name      Stmts   Miss   Cover
-------------------------------
main.py      47      1    97%

====================== 17 passed in 4.32s ========================
```

## Isolamento entre testes

Cada teste cria o banco do zero e destrói tudo no final. Isso garante que nenhum teste interfere no outro, independente da ordem que rodar.
