from app import app

def test_status_endpoint():
    client = app.test_client()
    response = client.get("/status")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
