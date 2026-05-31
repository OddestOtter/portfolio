import pytest
from rest_framework import status
from apps.core.models import UserStory

# Note: We rely on the fixtures defined in conftest.py
# We use the auth_client fixture for authenticated tests.

def test_authenticated_user_can_create_user_story(auth_client, project_factory, user_story_factory):
    """
    Tests that an authenticated user can successfully create a new user story.
    """
    # Create a new story instance for testing
    new_story_data = {
        'project': project_factory.id,
        'title': 'New Story Title',
        'description': 'A new story to be implemented.',
        'priority': 5,
        'status': 'To Do',
        'acceptance_criteria': 'Must pass all tests.'
    }
    
    response = auth_client.post(
        '/api/v1/stories/', 
        new_story_data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'New Story Title'
    
    # Verify creation in DB
    created_story = UserStory.objects.get(title='New Story Title')
    assert created_story.project == project_factory

def test_creation_fails_if_acceptance_criteria_is_empty(auth_client, project_factory):
    """
    Tests that creating a user story fails validation if acceptance_criteria is empty.
    """
    invalid_story_data = {
        'project': project_factory.id,
        'title': 'Bad Story',
        'description': 'No criteria.',
        'priority': 1,
        'status': 'To Do',
        'acceptance_criteria': '' # Empty criteria
    }
    
    response = auth_client.post(
        '/api/v1/stories/', 
        invalid_story_data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "acceptance_criteria" in response.data['non_field_errors']

def test_filter_by_project_id_returns_correct_stories(auth_client, project_factory, user_story_factory):
    """
    Tests filtering the list of stories by a specific project ID.
    """
    # Create a story in a different project to ensure filtering works
    other_project = Project.objects.create(name='Other', description='Other')
    UserStory.objects.create(
        project=other_project,
        title='Other Story', 
        description='Other', 
        priority=1, 
        status='Done', 
        acceptance_criteria='AC'
    )
    
    # Filter by the original project
    response = auth_client.get(f'/api/v1/stories/?project={project_factory.id}')
    
    assert response.status_code == status.HTTP_200_OK
    # Should only return stories belonging to project_factory
    stories = [item['title'] for item in response.data]
    assert len(stories) == 1
    assert stories[0] == user_story_factory.title

def test_filter_by_status_returns_correct_stories(auth_client, project_factory, user_story_factory):
    """
    Tests filtering the list of stories by a specific status.
    """
    # Create a story with a different status
    UserStory.objects.create(
        project=project_factory,
        title='Done Story', 
        description='Done', 
        priority=1, 
        status='Done', 
        acceptance_criteria='AC'
    )
    
    # Filter by 'Done' status
    response = auth_client.get(f'/api/v1/stories/?status=Done')
    
    assert response.status_code == status.HTTP_200_OK
    stories = [item['title'] for item in response.data]
    assert len(stories) >= 1

def test_list_returns_correct_ordering_by_priority_descending(auth_client, project_factory):
    """
    Tests that the list endpoint orders stories by priority descending.
    """
    # Create stories with varying priorities
    UserStory.objects.create(project=project_factory, title='P1 Story', description='D', priority=1, status='To Do', acceptance_criteria='AC')
    UserStory.objects.create(project=project_factory, title='P3 Story', description='D', priority=3, status='To Do', acceptance_criteria='AC')
    UserStory.objects.create(project=project_factory, title='P5 Story', description='D', priority=5, status='To Do', acceptance_criteria='AC')
    
    # Fetch and check order
    response = auth_client.get(f'/api/v1/stories/')
    
    assert response.status_code == status.HTTP_200_OK
    titles = [item['title'] for item in response.data]
    # Expected order: P5, P3, P1
    assert titles == ['P5 Story', 'P3 Story', 'P1 Story']

def test_unauthenticated_user_cannot_access_any_endpoint(unauthenticated_client):
    """
    Tests that unauthenticated users receive 401 Unauthorized when accessing story endpoints.
    """
    # Test GET (List)
    response_get = unauthenticated_client.get('/api/v1/stories/')
    assert response_get.status_code == status.HTTP_401_UNAUTHORIZED

    # Test POST (Create)
    response_post = unauthenticated_client.post(
        '/api/v1/stories/', 
        {'project': 1, 'title': 'Test', 'description': 'Test', 'priority': 1, 'status': 'To Do', 'acceptance_criteria': 'AC'}, 
        format='json'
    )
    assert response_post.status_code == status.HTTP_401_UNAUTHORIZED
