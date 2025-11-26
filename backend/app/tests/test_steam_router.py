# app/tests/test_steam_router.py

from fastapi.routing import APIRoute

FAKE_USER = "test_user"
FAKE_STEAM = "12345678900000000"

def _find_route(client, contains, method):
    contains = contains.lower()
    method = method.upper()
    for route in client.app.routes:
        if isinstance(route, APIRoute):
            if contains in route.path.lower() and method in route.methods:
                return route.path
    return None


def test_steam_sync_not_crashing(client):
    path = _find_route(client, "/steam/sync", "POST")
    assert path is not None, "Rota POST /steam/sync/{user_id}/{steam_id} não encontrada"

    final_path = path.replace("{user_id}", FAKE_USER).replace("{steam_id}", FAKE_STEAM)
    resp = client.post(final_path)

    # Aceitamos qualquer código, EXCETO 500 sem tratamento
    assert resp.status_code != 500
