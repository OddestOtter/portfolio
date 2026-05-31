import pytest
from rest_framework import status
from apps.core.models import Task

# Note: We rely on the fixtures defined in conftest.py
# We use the auth_client fixture for authenticated tests.

def test_authenticated_user_can_create_task(auth_client, task_factory):
    """
    Tests that an authenticated user can successfully create a new task.
    """
    # task_factory already provides a user_story, so we use its ID
    task_data = {
        'user_story': task_factory.user_story.id,
        'title': 'New Task Title',
        'description': 'A concrete task derived from a story.',
        'is_complete': False
    }
    
    response = auth_client.post(
        '/api/v1/tasks/', 
        task_data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'New Task Title'
    
    # Verify creation in DB
    created_task = Task.objects.get(title='New Task Title')
    assert created_task.user_story == task_factory.user_story

def test_filter_by_user_story_id_returns_correct_tasks(auth_client, task_factory):
    """
    Tests filtering the list of tasks by a specific user_story ID.
    """
    # Create a task linked to a different story
    other_story = UserStory.objects.create(
        project=None, title='Other Story', description='Other', priority=1, status='To Do', acceptance_criteria='AC'
    )
    Task.objects.create(
        user_story=other_story,
        title='Other Task', 
        description='Other', 
        is_complete=False
    )
    
    # Filter by the original story's ID
    response = auth_client.get(f'/api/v1/tasks/?user_story={task_factory.user_story.id}')
    
    assert response.status_code == status.HTTP_200_OK
    tasks = [item['title'] for item in response.data]
    assert len(tasks) == 1
    assert tasks[0] == task_factory.title

def test_filter_by_is_complete_returns_correct_tasks(auth_client, task_factory):
    """
    Tests filtering the list of tasks by completion status (is_complete=True).
    """
    # Create a completed task
    completed_task = Task.objects.create(
        user_story=task_factory.user_story,
        title='Completed Task', 
        description='Done', 
        is_complete=True
    )
    
    # Filter by True
    response = auth_client.get('/api/v1/tasks/?is_complete=True')
    
    assert response.status_code == status.HTTP_200_OK
    tasks = [item['title'] for item in response.data]
    assert len(tasks) >= 1
    assert 'Completed Task' in tasks

def test_marking_task_complete_updates_is_complete_correctly(auth_client, task_factory):
    """
    Tests updating a task to mark it as complete.
    """
    # 1. Get the task ID
    task_id = task_factory.id
    
    # 2. Update the task via PATCH request
    update_data = {'is_complete': True}
    response = auth_client.patch(
        f'/api/v1/tasks/{task_id}/', 
        update_data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['is_complete'] == True
    
    # 3. Verify update in DB
    task_factory.refresh_from_db()
    assert task_factory.is_complete == True

def test_unauthenticated_user_cannot_access_any_endpoint(unauthenticated_client):
    """
    Tests that unauthenticated users receive 401 Unauthorized when accessing task endpoints.
    """
    # Test GET (List)
    response_get = unauthenticated_client.get('/api/v1/tasks/')
    assert response_get.status_code == status.HTTP_401_UNAUTHORIZED

    # Test POST (Create)
    response_post = unauthenticated_client.post(
        '/api/v1/tasks/', 
        {'user_story': 1, 'title': 'Test', 'description': 'Test', 'is_complete': False}, 
        format='json'
    )
    assert response_post.status_code == status.HTTP_401_UNAUTHORIZED
