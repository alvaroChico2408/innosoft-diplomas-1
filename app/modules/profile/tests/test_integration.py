import pytest
from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from flask_login import current_user

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add specific data for integration testing.
    """
    test_client.application.config['SERVER_NAME'] = 'localhost'
    test_client.application.config['WTF_CSRF_ENABLED'] = False
    
    # Create a test user
    user = User(email="user1@example.com")
    user.set_password("123")  # Assuming `set_password` hashes the password
    db.session.add(user)
    db.session.commit()

# Create a test profile
    profile = UserProfile(
        user_id=user.id,
        name="Name",
        surname="Surname",
        email="user1@example.com",  # Add the email field
        password="123"  # Add the password field
    )
    db.session.add(profile)
    db.session.commit()

    yield test_client
def test_get_profile(test_client):
    """
    Test retrieving a user profile via GET request.
    """
    # Log in the test user
    login_response = login(test_client, "user@example.com", "123")
    assert login_response.status_code == 200, "Login was unsuccessful."
    logout(test_client)

def test_edit_profile(test_client):
    """
    Test editing a user profile via POST request.
    """
    # Log in the test user
    login_response = login(test_client, "user1@example.com", "123")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    # Edit the profile
    response = test_client.post("/profile/edit", data={
        "name": "New Name",
        "surname": "New Surname",
        "email": "user1@example.com"
    }, follow_redirects=True)
    assert response.status_code == 200, "The profile could not be edited."
    
    # Check that the profile was edited
    with test_client.application.app_context():
        profile = UserProfile.query.filter_by(email="user1@example.com").first()
        assert profile.name == "New Name", "The profile was not edited."
        assert profile.surname == "New Surname", "The profile was not edited."

    logout(test_client)


def test_change_password(test_client):
    """
    Test changing a user's password via POST request.
    """
    # Log in the test user
    login_response = login(test_client, "user1@example.com", "123")
    assert login_response.status_code == 200, "Login was unsuccessful."

    # Change the password
    response = test_client.post("/profile/change_password", data={
        "password": "new_password",
        "confirm_password": "new_password"
    }, follow_redirects=True)
    assert response.status_code == 200, "The password could not be changed."

    # Check that the password was changed
    with test_client.application.app_context():
        profile = UserProfile.query.filter_by(email="user1@example.com").first()
        assert profile.password == "00b9e6622317a2fb628d5514b866d4e7c52b5b149027825645ae3fd72827e84e", "The password was not changed."
        