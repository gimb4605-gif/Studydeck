import pytest
from fastapi.testclient import TestClient
from app import main

@pytest.fixture
def client(tmp_path):
    main.DB_PATH = tmp_path / "test.db"
    main.init_db()
    return TestClient(main.app)

def test_first_page_requests_nickname(client):
    response = client.get("/")
    assert response.status_code == 200
    assert 'id="nickname"' in response.text
    assert "/login" not in response.text

def test_todos_are_separated_by_nickname(client):
    client.post("/todos", data={"nickname": "alice", "title": "reading"})
    assert "reading" in client.get("/?nickname=alice").text
    assert "reading" not in client.get("/?nickname=bob").text

def test_attendance_is_recorded_once_per_nickname(client):
    client.post("/attendance", data={"nickname": "alice"})
    client.post("/attendance", data={"nickname": "alice"})
    client.post("/attendance", data={"nickname": "bob"})
    with main.db() as conn:
        assert conn.execute("SELECT COUNT(*) FROM attendance WHERE nickname = 'alice'").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM attendance WHERE nickname = 'bob'").fetchone()[0] == 1
