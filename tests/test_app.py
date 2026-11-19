import pytest

from app import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_accueil_message_par_defaut(client, monkeypatch):
    monkeypatch.delenv("MESSAGE", raising=False)
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Bonjour depuis AKS !"


def test_accueil_message_configurable(client, monkeypatch):
    monkeypatch.setenv("MESSAGE", "Message de test")
    assert client.get("/").get_json()["message"] == "Message de test"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_ready(client):
    assert client.get("/ready").status_code == 200
