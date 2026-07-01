import pytest


# -------------------- HELPER FUNCTIONS --------------------

def create_test_user(client, name="Javeed", email="javeed@test.com", password="test123"):
    """Helper to create a user — reused across multiple tests."""
    response = client.post("/users", json={
        "name": name,
        "email": email,
        "password": password
    })
    return response


def login_test_user(client, email="javeed@test.com", password="test123"):
    """Helper to log in and return the auth token."""
    response = client.post("/login", data={
        "username": email,
        "password": password
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_test_application(client, headers):
    """Helper to create a sample application — reused across multiple tests."""
    response = client.post("/applications", json={
        "company_name": "Stripe",
        "role_title": "Forward Deployed Engineer",
        "status": "Applied",
        "notes": "Test application"
    }, headers=headers)
    return response


# -------------------- USER TESTS --------------------

def test_create_user(client):
    """Creating a new user should return 200 with correct fields."""
    response = create_test_user(client)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "javeed@test.com"
    assert data["name"] == "Javeed"
    assert "id" in data
    assert "password" not in data  # password must never be returned
    assert "hashed_password" not in data


def test_create_duplicate_user(client):
    """Registering the same email twice should return 400."""
    create_test_user(client)
    response = create_test_user(client)  # same email again
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_success(client):
    """Valid credentials should return a token."""
    create_test_user(client)
    response = client.post("/login", data={
        "username": "javeed@test.com",
        "password": "test123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Wrong password should return 401."""
    create_test_user(client)
    response = client.post("/login", data={
        "username": "javeed@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """Logging in with an email that doesn't exist should return 401."""
    response = client.post("/login", data={
        "username": "nobody@test.com",
        "password": "test123"
    })
    assert response.status_code == 401


# -------------------- APPLICATION TESTS --------------------

def test_create_application(client):
    """Authenticated user should be able to create an application."""
    create_test_user(client)
    headers = login_test_user(client)
    response = create_test_application(client, headers)
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "Stripe"
    assert data["role_title"] == "Forward Deployed Engineer"
    assert data["status"] == "Applied"
    assert "id" in data


def test_create_application_unauthenticated(client):
    """Creating an application without a token should return 401."""
    response = client.post("/applications", json={
        "company_name": "Google",
        "role_title": "SDE Intern",
        "status": "Applied"
    })
    assert response.status_code == 401


def test_get_applications(client):
    """Authenticated user should get back their list of applications."""
    create_test_user(client)
    headers = login_test_user(client)
    create_test_application(client, headers)
    response = client.get("/applications", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["company_name"] == "Stripe"


def test_get_applications_empty(client):
    """Freshly logged in user with no applications should get an empty list."""
    create_test_user(client)
    headers = login_test_user(client)
    response = client.get("/applications", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


def test_update_application(client):
    """Updating status should reflect in the response."""
    create_test_user(client)
    headers = login_test_user(client)
    app_id = create_test_application(client, headers).json()["id"]

    response = client.put(f"/applications/{app_id}", json={
        "status": "Interviewing"
    }, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Interviewing"
    assert data["company_name"] == "Stripe"  # unchanged fields stay intact


def test_delete_application(client):
    """Deleting an application should remove it from the list."""
    create_test_user(client)
    headers = login_test_user(client)
    app_id = create_test_application(client, headers).json()["id"]

    # Delete it
    response = client.delete(f"/applications/{app_id}", headers=headers)
    assert response.status_code == 200

    # Confirm it's gone
    response = client.get("/applications", headers=headers)
    assert response.json() == []


def test_delete_nonexistent_application(client):
    """Deleting an application that doesn't exist should return 404."""
    create_test_user(client)
    headers = login_test_user(client)
    response = client.delete("/applications/99999", headers=headers)
    assert response.status_code == 404


def test_user_cannot_access_other_users_applications(client):
    """User A should not be able to see or delete User B's applications."""
    # Create User A and their application
    create_test_user(client, name="User A", email="a@test.com")
    headers_a = login_test_user(client, email="a@test.com")
    app_id = create_test_application(client, headers_a).json()["id"]

    # Create User B
    create_test_user(client, name="User B", email="b@test.com")
    headers_b = login_test_user(client, email="b@test.com")

    # User B tries to delete User A's application
    response = client.delete(f"/applications/{app_id}", headers=headers_b)
    assert response.status_code == 404  # should not find it, not 200