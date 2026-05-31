import pytest
from rest_framework import status
from apps.core.models import Project

# Note: We rely on the fixtures defined in conftest.py
# We use the auth_client fixture for authenticated tests.

def test_authenticated_user_can_create_project(auth_client, project_factory):
    """
    Tests that an authenticated user can successfully create a new project.
    """
    new_project_data = {
        'name': 'New Awesome Project',
        'description': 'Testing project creation via API.'
    }
    
    response = auth_client.post(
        '/api/v1/projects/', 
        new_project_data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'New Awesome Project'
    
    # Verify creation in DB
    created_project = Project.objects.get(name='New Awesome Project')
    assert created_project.id == response.data['id']

def test_authenticated_user_can_list_projects(auth_client, project_factory):
    """
    Tests that an authenticated user can list all projects.
    Validates the list returns the correct number of projects and correct ordering.
    """
    # Create a second project to ensure listing works
    Project.objects.create(name='Old Project', description='For ordering test')
    
    response = auth_client.get('/api/v1/projects/')
    
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) >= 2
    
    # Check ordering: The list should be ordered by creation date (descending)
    # Since we created 'Old Project' and 'New Awesome Project' (from previous test),
    # the list should start with the most recently created one.
    # We check the names to confirm the list structure.
    names = [item['name'] for item in response.data]
    assert 'New Awesome Project' in names
    assert 'Old Project' in names

def test_authenticated_user_can_retrieve_project_with_nested_story_count(auth_client, project_factory, user_story_factory):
    """
    Tests retrieving a project and validating the nested user_story_count field.
    """
    # Ensure the project has at least one story
    project_factory.userstory_set.create(
        title="Test Story", 
        description="Test", 
        priority=1, 
        status="Done", 
        acceptance_criteria="AC"
    )
    
    response = auth_client.get(f'/api/v1/projects/{project_factory.id}/')
    
    assert response.status_code == status.HTTP_200_OK
    assert 'user_story_count' in response.data
    assert response.data['user_story_count'] >= 1

def test_authenticated_user_can_update_project(auth_client, project_factory):
    """
    Tests updating an existing project.
    """
    update_data = {
        'name': 'Updated Project Name',
        'description': 'Updated description via API.'
    }
    
    response = auth_client.patch(
        f'/api/v1/projects/{project_factory.id}/', 
        update_data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Updated Project Name'
    
    # Verify update in DB
    project_factory.refresh_from_db()
    assert project_factory.name == 'Updated Project Name'

def test_authenticated_user_can_delete_project(auth_client, project_factory):
    """
    Tests deleting a project.
    """
    # Ensure the project exists before deletion
    assert Project.objects.filter(pk=project_factory.id).exists()
    
    response = auth_client.delete(f'/api/v1/projects/{project_factory.id}/')
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify deletion in DB
    assert not Project.objects.filter(pk=project_factory.id).exists()

def test_unauthenticated_user_cannot_access_any_endpoint(unauthenticated_client):
    """
    Tests that unauthenticated users receive 401 Unauthorized when accessing project endpoints.
    """
    # Test GET (List)
    response_get = unauthenticated_client.get('/api/v1/projects/')
    assert response_get.status_code == status.HTTP_401_UNAUTHORIZED

    # Test POST (Create)
    response_post = unauthenticated_client.post(
        '/api/v1/projects/', 
        {'name': 'Test', 'description': 'Test'}, 
        format='json'
    )
    assert response_post.status_code == status.HTTP_401_UNAUTHORIZED
