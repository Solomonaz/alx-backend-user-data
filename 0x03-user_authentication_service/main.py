#!/usr/bin/env python3
""" End-to-end integration test"""

import requests

BASE_URL = "http://localhost:5000"

def register_user(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/register", json={"email": email, "password": password})
    assert response.status_code == 201, f"Register: Unexpected status code {response.status_code}"
    print("User registered successfully.")

def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    assert response.status_code == 401, f"Login with wrong password: Unexpected status code {response.status_code}"
    print("Login with wrong password failed as expected.")

def log_in(email: str, password: str) -> str:
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    assert response.status_code == 200, f"Login: Unexpected status code {response.status_code}"
    session_id = response.json().get("session_id")
    assert session_id, "Login: Session ID not found in response"
    print("Logged in successfully.")
    return session_id

def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 401, f"Profile (unlogged): Unexpected status code {response.status_code}"
    print("Profile (unlogged) failed as expected.")

def profile_logged(session_id: str) -> None:
    headers = {"Authorization": f"Bearer {session_id}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 200, f"Profile (logged): Unexpected status code {response.status_code}"
    print("Profile (logged) retrieved successfully.")

def log_out(session_id: str) -> None:
    headers = {"Authorization": f"Bearer {session_id}"}
    response = requests.get(f"{BASE_URL}/logout", headers=headers)
    assert response.status_code == 200, f"Logout: Unexpected status code {response.status_code}"
    print("Logged out successfully.")

def reset_password_token(email: str) -> str:
    response = requests.post(f"{BASE_URL}/reset_password", json={"email": email})
    assert response.status_code == 200, f"Reset password token: Unexpected status code {response.status_code}"
    reset_token = response.json().get("reset_token")
    assert reset_token, "Reset password token: Token not found in response"
    print("Reset password token retrieved successfully.")
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    data = {"email": email, "reset_token": reset_token, "new_password": new_password}
    response = requests.put(f"{BASE_URL}/update_password", json=data)
    assert response.status_code == 200, f"Update password: Unexpected status code {response.status_code}"
    print("Password updated successfully.")

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

