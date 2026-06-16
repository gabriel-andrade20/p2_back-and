import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, Base, get_db

TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/ecommerce_test"


@pytest.fixture(scope="function")
def client():
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def produto_existente(client):
    payload = {"nome": "Produto Teste", "preco": 29.90, "estoque": 10, "ativo": True}
    response = client.post("/produtos", json=payload)
    assert response.status_code == 201
    return response.json()
