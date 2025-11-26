# app/tests/test_game_router.py

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


def test_list_games_does_not_crash(client):
    path = _find_route(client, "/games/", "GET")
    assert path is not None, "Rota GET /games/{user_id} não encontrada"

    final_path = path.replace("{user_id}", FAKE_USER_ID)
    resp = client.get(final_path)

    # Pode ser 200, 404, 401… mas NÃO pode ser 500
    assert resp.status_code != 500


def test_add_game_allows_empty_payload_and_does_not_crash(client):
    path = _find_route(client, "/games/", "POST")
    assert path is not None, "Rota POST /games/{user_id} não encontrada"

    final_path = path.replace("{user_id}", FAKE_USER_ID)
    resp = client.post(final_path, json={})

    assert resp.status_code in {200, 400}
