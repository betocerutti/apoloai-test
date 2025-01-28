import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Order
from app.database import get_db
from app.models import Base
from app.main import app

# Fixture to create an in-memory SQLite database
@pytest.fixture(scope="function")
def test_db():
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Insert initial data
    db_order = Order(
        id=1,
        products=[
            {"id": 1, "quantity": 1},
            {"id": 2, "quantity": 2}
        ],
        total_price=100.0,
        created_at=datetime.now()
        )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    yield db

    # Clean up
    db.close()

# Fixture to override the get_db dependency
@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

# Test the endpoint
def test_orders_list(client):
    response = client.get("/orders/")
    assert response.status_code == 200