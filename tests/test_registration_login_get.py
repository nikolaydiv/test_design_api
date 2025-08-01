import pytest
import requests
from utils import random_username, random_email, random_password, random_age

test_cases = [
    # boundary values and equivalents
    ("us", "random", "random", "random", 422),  # too short username
    ("a" * 21, "random", "random", "random", 422),  # too long username
    ("random", "random", 0, "random", 422),   # too little age
    ("random", "random", 101, "random", 422), # too big age
    ("random", "random", "random", "good", 422), # too short password
    ("random", "random", "random", "a" * 21, 422), # too long password
    ("", "random", "random", "random", 422),  # no username
    ("random", "random", "", "random", 422),  # no email
    ("random", "random", None, "random", 422),  # no age
    ("random", "random", "random", "", 422),  # no password
    ("", "", None, "", 422),  # empty fields

    # pairwise testing
    ("random", "testmailcom", "random", "random", 422),  # invalid email
    ("random", "random", "random", "", 422),  # empty password

    # negative format
    (12345, "random", "random", "random", 422),  # incorrect username type
    ("random", True, "random", "random", 422), # incorrect email type
    ("random", "random", "random", ["pass123"], 422),  # incorrect password type

    # logic's restrictions
    ("AdmIn123", "random", "random", "random", 400),  # admin in username
    ("random", "random", "random", "123456", 400), # weak password

    # positive cases
    ("random", "test@mail.com", "random", "GoodPassword", 200),
    ("use", "random", "random", "random", 200),  # 3-symbol username
    ("u" * 20, "random", "random", "random", 200),  # 20-symbol username
    ("random", "random", "random", "GoodPa", 200),  # 6-symbol password
    ("random", "random", "random", "VeryGoodPasswordISwe", 200),  # 20-symbol password
    ("TheK1nG!", "random", "random", "random", 200),  # different symbols username

    # already registered email
    ("random", "test@mail.com", "random", "random", 400)  # email already registered
]

@pytest.mark.parametrize("username, email, age, password, expected_status", test_cases)
def test_user_registration(base_url, username, email, age, password, expected_status):
    if username == "random":
        username = random_username()
    if email == "random":
        email = random_email()
    if age == "random":
        age = random_age()
    if password == "random":
        password = random_password()

    payload = {
        "username": username,
        "email": email,
        "age": age,
        "password": password
    }
    print(payload)

    response = requests.post(f"{base_url}/register", json=payload)
    assert response.status_code == expected_status
    if response.status_code != 200:
        assert "detail" in response.json()
        print(response.json())
        print(response.status_code)
    if response.status_code == 200:
        assert response.json() == {"message": "User registered successfully"}

@pytest.mark.parametrize("email, password, expected_status", [
    ("test@mail.com", "GoodPassword", 200),  # successful login
    ("notregistered@mail.com", "GoodPassword", 400),  # not registered email
    ("test@mail.com", "GoodPassword123", 401)  # invalid password
])
def test_login(base_url, email, password, expected_status):
    response = requests.post(f'{base_url}/login', json={
        "email": email,
        "password": password
    })
    assert response.status_code == expected_status

@pytest.mark.parametrize("email, expected_status", [
    ("test@mail.com", 200),  # email is registered
    ("testt@mail.com", 400)  # email is not registered
])
def test_user_is_registered(base_url, email, expected_status):
    response = requests.get(f'{base_url}/user/{email}', json={
        "email": email
    })
    assert response.status_code == expected_status
