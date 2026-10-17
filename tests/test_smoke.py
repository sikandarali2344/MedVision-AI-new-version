from fastapi.testclient import TestClient
from backend.main import app
client = TestClient(app)
def test_health():
    response = client.get('/api/health')
    assert response.status_code == 200 and response.json()['status'] == 'ok'
def test_frontend():
    response = client.get('/')
    assert response.status_code == 200 and 'MedVision AI' in response.text
