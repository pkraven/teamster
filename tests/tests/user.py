import requests
import pytest


def test_create_user_201(url_prefix):
    user = requests.post(
        f"{url_prefix}/user/",
        json={
            "name": "Mark",
            "birthday": "1968-12-06",
            "phone": "+7 (888) 888-888-88",
            "email": "pk.raven@gmail.com"
        },
        headers={"Content-Type": "application/json"}
    )

    assert user.status_code == 200


@pytest.mark.parametrize("body", [
    '{"name": "Mark"}}}',
    ''
])
def test_create_user_wrong_body_400(url_prefix, body):
    user = requests.post(
        f"{url_prefix}/user/",
        data=body,
        headers={"Content-Type": "application/json"}
    )

    assert user.status_code == 400


@pytest.mark.parametrize("body", [
    {},
    {"birthday": "1968-12-06", "phone": "+7 (888) 888-888-88", "email": "pk.raven@gmail.com"},  # no name
    {"phone": "+7 (888) 888-888-88", "email": "pk.raven@gmail.com"},  # no name

    {"name": 999, "birthday": "1968-12-06", "phone": "+7 (888) 888-888-88", "email": "pk.raven@gmail.com"},
    {"name": "Mark", "birthday": "19681206", "phone": "+7 (888) 888-888-88", "email": "pk.raven@gmail.com"},
    {"name": "Mark", "birthday": "1968-12-06", "phone": "23423434234aa", "email": "pk.raven@gmail.com"},
    {"name": "Mark", "birthday": "1968-12-06", "phone": "+7 (888) 888-888-88", "email": "pk.raven@gmail11"},

])
def test_create_user_wrong_params_422(url_prefix, body):
    user = requests.post(
        f"{url_prefix}/user/",
        json=body,
        headers={"Content-Type": "application/json"}
    )

    assert user.status_code == 423


@pytest.mark.parametrize("phone,code", [
    ("+7 (888) 888-888-88", 200),
    ("888 888-888-88", 200),
    ("+7888888-888-88", 200),
    ("+788888888888", 200),
    ("88888888888", 200),
    ("aa88888888888", 422),
    ("bbcbxcv", 422)
])
def test_create_user_check_phone(url_prefix, phone, code):
    user = requests.post(
        f"{url_prefix}/user/",
        json={
            "name": "Mark",
            "birthday": "1968-12-06",
            "phone": phone,
            "email": "pk.raven@gmail.com"
        }
        ,
        headers={"Content-Type": "application/json"}
    )

    assert user.status_code == code


def test_get_user_200(url_prefix):
    user_data = {
        "name": "Mark",
        "birthday": "1968-12-06",
        "phone": "+7 (888) 888-888-88",
        "email": "pk.raven@gmail.com"
    }

    user = requests.post(
        f"{url_prefix}/user/",
        json=user_data,
        headers={"Content-Type": "application/json"}
    )
    assert user.status_code == 200

    user_id = user.json()['id']

    user = requests.get(f"{url_prefix}/user/{user_id}")

    assert user.status_code == 200
    assert user.json() == {
        'id': user_id,
        'schedule': [],
        **user_data
    }


def test_get_empty_users_list_200(url_prefix):
    user = requests.get(f"{url_prefix}/users/")

    assert user.status_code == 200
    assert user.json() == []


def test_get_users_list_200(url_prefix):
    user_data1 = {
        "name": "Mark",
        "birthday": "1968-12-06",
        "phone": "+7 (888) 888-888-88",
        "email": "pk.raven@gmail.com"
    }

    user_data2 = {
        "name": "Mark2",
        "birthday": "1968-12-08",
        "phone": "+7 (888) 888-888-80",
        "email": "pk.raven@gmail111.com"
    }

    user1 = requests.post(
        f"{url_prefix}/user/",
        json=user_data1,
        headers={"Content-Type": "application/json"}
    )
    assert user1.status_code == 200

    user_id1 = user1.json()['id']

    user2 = requests.post(
        f"{url_prefix}/user/",
        json=user_data2,
        headers={"Content-Type": "application/json"}
    )
    assert user2.status_code == 200

    user_id2 = user2.json()['id']

    users = requests.get(f"{url_prefix}/users/")

    assert users.status_code == 200
    assert users.json() != []
    assert users.json() == [{
        'id': user_id1,
        'schedule': [],
        **user_data1
    }, {
        'id': user_id2,
        'schedule': [],
        **user_data2
    }]
