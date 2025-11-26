# app/tests/test_auth_router.py

from fastapi.routing import APIRoute

def _find_route(client, contains: str, method: str):
    contains = contains.lower()
    method = method.upper()
    for route in client.app.routes:
        if isinstance(route, APIRoute):
            if contains in route.path.lower() and method in route.methods:
                return route.path
    return None


def test_login_returns_400_with_invalid_credentials(client):
    path = _find_route(client, "/login", "POST")
    assert path is not None, "Rota /auth/login não encontrada"

    resp = client.post(path, json={
        "email": "naoexiste@teste.com",
        "password": "senhaerrada"
    })

    # Firebase SEMPRE responde erro 400 quando login falha
    assert resp.status_code == 400


def test_register_returns_400_when_invalid_email(client):
    path = _find_route(client, "/register", "POST")
    assert path is not None, "Rota /auth/register não encontrada"

    resp = client.post(path, json={
        "email": "email_invalido",
        "password": "123456"
    })

    # EmailStr vai explodir 422 se JSON for inválido
    assert resp.status_code in {400, 422}
