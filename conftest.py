import pytest
from user.models import User
from rest_framework.test import APIClient

client = APIClient()

@pytest.fixture
def new_user1(db):
    user = User.objects.create_user(username="test",email='test@gmail.com',password="test")
    return user

@pytest.fixture
def user_token(new_user1):
    payload = dict(
        email="test@gmail.com",
        password="test"
    )

    response = client.post("/api/auth/",payload)
    data = response.data['data']
    return data