import pytest
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from factory import Faker
from apps.core.models import Project, UserStory, Task

# --- Fixture Setup ---

@pytest.fixture(scope="session")
def db_setup():
    """
    Fixture to ensure a clean database state for testing.
    pytest-django handles most of this, but this fixture serves as a marker
    for comprehensive setup/teardown if needed.
    """
    # pytest-django handles transaction management, but we keep this fixture
    # to explicitly mark the test suite's dependency on a clean DB.
    yield
    # Teardown logic (if any custom cleanup was needed)

@pytest.fixture(scope="function")
def user_factory():
    """Factory for creating a standard authenticated user."""
    return User.objects.create_user(
        username=Faker('user_username'), 
        email=Faker('email'), 
        password=lambda: Faker('password')
    )

@pytest.fixture(scope="function")
def auth_client(user_factory):
    """
    Provides an authenticated test client using the user_factory.
    The client will be automatically logged in with a valid token.
    """
    # Simulate token obtain for the client
    token = RefreshToken.for_user(user_factory)
    return pytest.Client(HTTPHEADER_KEYS=['Authorization'], HTTPHEADER_VALUES=[f'Bearer {token.access_token}'])

@pytest.fixture(scope="function")
def unauthenticated_client():
    """Provides an unauthenticated test client."""
    return pytest.Client()

@pytest.fixture(scope="function")
def project_factory(db_setup):
    """Factory for creating a Project instance."""
    return Project.objects.create(
        name=Faker('catchphrase'),
        description=Faker('sentence')
    )

@pytest.fixture(scope="function")
def user_story_factory(project_factory):
    """Factory for creating a UserStory instance linked to a project."""
    return UserStory.objects.create(
        project=project_factory,
        title=Faker('catchphrase'),
        description=Faker('sentence'),
        priority=3,
        status='To Do',
        acceptance_criteria=Faker('sentence')
    )

@pytest.fixture(scope="function")
def task_factory(user_story_factory):
    """Factory for creating a Task instance linked to a user story."""
    return Task.objects.create(
        user_story=user_story_factory,
        title=Faker('catchphrase'),
        description=Faker('sentence'),
        is_complete=False
    )
