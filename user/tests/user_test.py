import pytest
from rest_framework.test import APIClient

client = APIClient()

@pytest.mark.django_db
def test_register_user():
    payload = dict(
        first_name="Harry",
        last_name="Potter",
        username="harry",
        email="harry@hogwarts.com",
        password="timeforsometesting"
    )

    response = client.post("/api/users/",payload)
    data = response.data['data']

    assert data["first_name"] == payload["first_name"]
    assert data['last_name'] == payload['last_name']
    assert 'password' not in data
    assert data["email"] == payload["email"]



def test_login_user(new_user1):
    payload = dict(
        email="test@gmail.com",
        password="test"
    )

    response = client.post("/api/auth/",payload)
    data = response.data['data']

    assert data['email'] == payload['email']
    assert response.status_code == 200

def test_user_update(user_token):
    payload = dict(
        first_name="test",
        last_name="test"
    )
    token = 'Bearer' +' '+ user_token['access']
    


    response = client.patch("/api/update_profile/",payload,HTTP_AUTHORIZATION=token)
    data = response.data['data']

    assert data['first_name'] == payload['first_name']
    assert data['last_name'] == payload['last_name']
    assert response.status_code == 200


# def test_user_delete(new_user1,user_token):
#     token = 'Bearer ' + user_token['access']
#     print(token)
#     response = client.delete("/api/users/{}/".format(new_user1.id),HTTP_AUTHORIZATION=token)
#     assert response.status_code == 200