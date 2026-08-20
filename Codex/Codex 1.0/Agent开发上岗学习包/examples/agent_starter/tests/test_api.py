from fastapi.testclient import TestClient
from app.main import app
def test_health(): assert TestClient(app).get("/health").json()=={"ok":True}
def test_chat_validates_tenant(): assert TestClient(app).post("/chat",json={"message":"x","tenant_id":"forbidden"}).status_code==403
