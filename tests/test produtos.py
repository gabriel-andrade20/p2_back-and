import pytest


def test_listar_produtos_banco_vazio(client):
    """Lista produtos quando o banco está vazio — deve retornar lista vazia."""
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []


def test_criar_produto_verifica_persistencia(client):
    """Cria produto e verifica que foi persistido no banco."""
    payload = {"nome": "Notebook Pro", "preco": 4999.99, "estoque": 5, "ativo": True}
    response = client.post("/produtos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["nome"] == "Notebook Pro"
    assert data["preco"] == 4999.99
    assert data["estoque"] == 5
    assert data["ativo"] is True


def test_criar_produto_aparece_na_listagem(client):
    """Cria produto e verifica que ele aparece no GET /produtos."""
    payload = {"nome": "Mouse Gamer", "preco": 199.90, "estoque": 20, "ativo": True}
    client.post("/produtos", json=payload)

    response = client.get("/produtos")
    assert response.status_code == 200
    produtos = response.json()
    assert len(produtos) == 1
    assert produtos[0]["nome"] == "Mouse Gamer"


def test_buscar_produto_por_id_sucesso(client, produto_existente):
    """Busca produto por id — caso de sucesso."""
    produto_id = produto_existente["id"]
    response = client.get(f"/produtos/{produto_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == produto_existente["nome"]


def test_buscar_produto_id_inexistente_retorna_404(client):
    """Busca produto com id inexistente — deve retornar 404."""
    response = client.get("/produtos/99999")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"].lower()


def test_deletar_produto_retorna_204(client, produto_existente):
    """Deleta produto — deve retornar 204."""
    produto_id = produto_existente["id"]
    response = client.delete(f"/produtos/{produto_id}")
    assert response.status_code == 204


def test_deletar_produto_confirma_remocao_com_get(client, produto_existente):
    """Deleta produto e confirma remoção com GET subsequente."""
    produto_id = produto_existente["id"]
    client.delete(f"/produtos/{produto_id}")

    response = client.get(f"/produtos/{produto_id}")
    assert response.status_code == 404


def test_deletar_produto_inexistente_retorna_404(client):
    """Deleta produto inexistente — deve retornar 404."""
    response = client.delete("/produtos/99999")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"nome": "", "preco": 10.0},          # nome vazio
        {"nome": "   ", "preco": 10.0},       # nome só espaços
        {"nome": "Produto", "preco": 0.0},    # preço zero
        {"nome": "Produto", "preco": -5.0},   # preço negativo
        {"preco": 10.0},                       # sem nome
        {"nome": "Produto"},                   # sem preço
    ],
)
def test_criar_produto_payload_invalido_retorna_422(client, payload):
    """Payloads inválidos devem retornar 422."""
    response = client.post("/produtos", json=payload)
    assert response.status_code == 422


def test_banco_isolado_entre_testes(client):
    """Verifica que o banco está isolado — começa vazio a cada teste."""
    # Se houvesse vazamento de estado de outros testes, esta lista não seria vazia
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == [], "O banco deveria estar vazio no início de cada teste"


def test_criar_multiplos_produtos(client):
    """Cria múltiplos produtos e verifica a listagem completa."""
    produtos = [
        {"nome": "Teclado Mecânico", "preco": 350.0, "estoque": 15},
        {"nome": "Monitor 4K", "preco": 2500.0, "estoque": 3},
        {"nome": "Headset", "preco": 450.0, "estoque": 8},
    ]
    for p in produtos:
        r = client.post("/produtos", json=p)
        assert r.status_code == 201

    response = client.get("/produtos")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_produto_valores_padrao(client):
    """Cria produto sem estoque/ativo e verifica valores padrão."""
    payload = {"nome": "Produto Simples", "preco": 99.0}
    response = client.post("/produtos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["estoque"] == 0
    assert data["ativo"] is True
