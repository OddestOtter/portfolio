from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, UserStory, Task
from .serializers import ProjectSerializer, UserStorySerializer, TaskSerializer

# --- Project ViewSet ---
class ProjectViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Projects.
    List endpoint orders by creation date.
    """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().order_by('-created_at')

    def get_queryset(self):
        # Ensure the list endpoint always returns projects ordered by creation date
        return super().get_queryset()

    def perform_create(self, serializer):
        # Custom logic for creation if needed, but for now, just save
        serializer.save()

# --- UserStory ViewSet ---
class UserStoryViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for UserStories.
    Allows filtering by project and status.
    List endpoint orders by priority descending.
    """
    serializer_class = UserStorySerializer
    # Add DjangoFilterBackend to enable filtering
    filter_backends = [DjangoFilterBackend]
    # Define default filters
    filterset_fields = ['project', 'status']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply filtering based on request parameters
        return queryset.filter(
            # Filter by project ID if provided
            project_id=self.request.query_params.get('project')
        ).order_by('-priority')

    def perform_create(self, serializer):
        # Ensure the project is set correctly on creation
        project_id = self.request.data.get('project')
        if not project_id:
            raise serializers.ValidationError({"project": "Project field is required."})
        
        try:
            project = Project.objects.get(pk=project_id)
            serializer.save(project=project)
        except Project.DoesNotExist:
            raise serializers.ValidationError({"project": "Project does not exist."})


# --- Task ViewSet ---
class TaskViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Tasks.
    Allows filtering by user_story and completion status.
    """
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_story', 'is_complete']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user_story ID if provided
        if self.request.query_params.get('user_story'):
            return queryset.filter(user_story_id=self.request.query_params['user_story'])
        
        # Filter by completion status if provided
        if self.request.query_params.get('is_complete'):
            try:
                is_complete = self.request.query_params['is_complete'] == 'True'
                return queryset.filter(is_complete=is_complete)
            except ValueError:
                pass # Ignore if filter is invalid

        return queryset
