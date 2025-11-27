from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

FAKE_USER = "test_user"
FAKE_STEAM = "12345678900000000"


def _find_route(client, path, method):
    for route in client.app.routes:
        if route.path.startswith(
            path.replace("{user_id}", "").replace("{steam_id}", "")
        ) and method in route.methods:
            return route.path
    return None


def test_steam_sync_not_crashing(monkeypatch):
    # MOCK da função de sync para não chamar a API real
    def fake_sync(self, user_id, steam_id):
        return []  # Simula sucesso sem bater na Steam

    monkeypatch.setattr(
        "app.services.steam_services.SteamService.sync_library",
        fake_sync
    )

    path = _find_route(client, "/api/steam/sync", "POST")

    assert path is not None, "Rota POST /steam/sync/{user_id}/{steam_id} não encontrada"

    final_path = path.replace("{user_id}", FAKE_USER).replace("{steam_id}", FAKE_STEAM)
    resp = client.post(final_path)

    assert resp.status_code != 500
