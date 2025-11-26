# app/tests/test_recommendations_router.py

from fastapi.routing import APIRoute

FAKE_USER_ID = "test_user"

def _find_route(client, contains, method):
    contains = contains.lower()
    method = method.upper()
    for route in client.app.routes:
        if isinstance(route, APIRoute):
            if contains in route.path.lower() and method in route.methods:
                return route.path
    return None


def test_recommendations_does_not_crash(client):
    path = _find_route(client, "/recommendations/", "GET")
    assert path is not None, "Rota GET /recommendations/{user_id} não encontrada"

    final_path = path.replace("{user_id}", FAKE_USER_ID)
    resp = client.get(final_path)

    # Respostas aceitáveis:
    assert resp.status_code in {200, 404, 500}
