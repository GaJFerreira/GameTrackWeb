# app/tests/test_user_router.py

from fastapi.routing import APIRoute

FAKE_USER = "test_user"

def _find_route(client, contains, method):
    contains = contains.lower()
    method = method.upper()
    for route in client.app.routes:
        if isinstance(route, APIRoute):
            if contains in route.path.lower() and method in route.methods:
                return route.path
    return None


def test_list_users_does_not_crash(client):
    path = _find_route(client, "/users", "GET")
    assert path is not None, "Rota GET /users não encontrada"

    resp = client.get(path)
    assert resp.status_code in {200, 404}


def test_get_user_does_not_crash(client):
    path = _find_route(client, "/users/", "GET")
    assert path is not None, "Rota GET /users/{user_id} não encontrada"

    final_path = path + FAKE_USER
    resp = client.get(final_path)

    # Pode ser 200 se existir, 404 se não existir
    assert resp.status_code in {200, 404}
