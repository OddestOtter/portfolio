import pytest
from rest_framework import status
from django.contrib.auth.models import User

# Note: We rely on the fixtures defined in conftest.py
# We use the unauthenticated_client fixture for these tests.

def test_successful_user_registration(unauthenticated_client, user_factory):
    """
    Tests successful user registration.
    Validates that the response contains both access and refresh tokens.
    """
    # Use the user_factory to generate credentials for the test
    data = {
        'username': user_factory.username,
        'email': user_factory.email,
        'password': 'TestPassword123!'
    }
    
    response = unauthenticated_client.post(
        '/api/v1/auth/register/', 
        data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access' in response.data
    assert 'refresh' in response.data

def test_registration_with_missing_fields(unauthenticated_client):
    """
    Tests registration failure when required fields are missing.
    Expects a 400 Bad Request response.
    """
    data = {'username': 'testuser', 'email': 'test@example.com'} # Missing password
    
    response = unauthenticated_client.post(
        '/api/v1/auth/register/', 
        data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Missing required fields" in response.data['error']

def test_registration_with_duplicate_username(unauthenticated_client, user_factory):
    """
    Tests registration failure when a user with the same email/username already exists.
    Expects a 409 Conflict response.
    """
    # Attempt to register with the existing user's email
    data = {
        'username': 'duplicate_user',
        'email': user_factory.email,
        'password': 'NewPassword123!'
    }
    
    response = unauthenticated_client.post(
        '/api/v1/auth/register/', 
        data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.data['error']


def test_token_obtain_success(unauthenticated_client, user_factory):
    """
    Tests obtaining tokens with valid credentials.
    Validates that the response contains both access and refresh tokens.
    """
    # Use the user_factory credentials
    data = {
        'username': user_factory.username,
        'password': 'TestPassword123!'
    }
    
    response = unauthenticated_client.post(
        '/api/v1/auth/token/', 
        data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

def test_token_obtain_invalid_credentials(unauthenticated_client):
    """
    Tests obtaining tokens with invalid credentials.
    Expects a 401 Unauthorized response.
    """
    data = {
        'username': 'nonexistentuser',
        'password': 'wrongpassword'
    }
    
    response = unauthenticated_client.post(
        '/api/v1/auth/token/', 
        data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Could not authenticate" in response.data['detail']

def test_accessing_protected_endpoint_without_token(unauthenticated_client):
    """
    Tests accessing a protected endpoint (e.g., projects list) without providing a token.
    Expects a 401 Unauthorized response.
    """
    # Use the unauthenticated client and hit a protected endpoint
    response = unauthenticated_client.get('/api/v1/projects/')
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Authentication credentials were not provided" in response.data['detail']
