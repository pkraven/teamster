import requests
import pytest


def test_create_schedule_201(url_prefix):
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
    user_id = user.json()['id']

    schedule = requests.post(
        f"{url_prefix}/user/{user_id}/schedule/",
        json={
            "str_type": "start",
            "time_start": "10:00:00",
            "time_end": "18:30:00"
        },
        headers={"Content-Type": "application/json"}
    )

    assert schedule.status_code == 201


def test_create_schedule_no_user_404(url_prefix):
    schedule = requests.post(
        f"{url_prefix}/user/2/schedule/",
        json={
            "str_type": "start",
            "time_start": "10:00:00",
            "time_end": "18:30:00"
        },
        headers={"Content-Type": "application/json"}
    )

    assert schedule.status_code == 404


@pytest.mark.parametrize("body", [
    '{"str_type": "start"}}}',
    ''
])
def test_create_schedule_wrong_body_400(url_prefix, body):
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
    user_id = user.json()['id']

    user = requests.post(
        f"{url_prefix}/user/2/schedule/",
        data=body,
        headers={"Content-Type": "application/json"}
    )

    assert user.status_code == 400


@pytest.mark.parametrize("body", [
    {},
    {"str_type": "start", "time_start": "10:00:00"},
    {"str_type": "start", "time_end": "18:30:00"},
    {"time_start": "10:00:00", "time_end": "18:30:00"},

    {"str_type": "start1", "time_start": "10:00:00", "time_end": "18:30:00"},
    {"str_type": "start", "time_start": "10dasdas", "time_end": "18:30:00"},
    {"str_type": "start", "time_start": "10:00:00", "time_end": "18dsadas"}
])
def test_create_schedule_wrong_params_422(url_prefix, body):
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
    user_id = user.json()['id']

    user = requests.post(
        f"{url_prefix}/user/{user_id}/schedule/",
        json=body,
        headers={"Content-Type": "application/json"}
    )

    assert user.status_code == 422


def test_create_schedule_repeat_start_end_200(url_prefix):
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
    user_id = user.json()['id']

    schedule = requests.post(
        f"{url_prefix}/user/{user_id}/schedule/",
        json={
            "str_type": "start",
            "time_start": "10:00:00",
            "time_end": "00:00:00"
        },
        headers={"Content-Type": "application/json"}
    )

    schedule = requests.post(
        f"{url_prefix}/user/{user_id}/schedule/",
        json={
            "str_type": "end",
            "time_start": "10:00:00",
            "time_end": "00:00:00"
        },
        headers={"Content-Type": "application/json"}
    )

    schedule = requests.post(
        f"{url_prefix}/user/{user_id}/schedule/",
        json={
            "str_type": "start",
            "time_start": "12:00:00",
            "time_end": "00:00:00"
        },
        headers={"Content-Type": "application/json"}
    )

    user = requests.get(f"{url_prefix}/user/{user_id}")

    assert user.json()['schedule'][0]['time_start'] == "12:00:00"
