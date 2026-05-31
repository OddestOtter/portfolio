from rest_framework import serializers
from .models import Project, UserStory, Task

# --- Project Serializer ---
class ProjectSerializer(serializers.ModelSerializer):
    # Read-only field for nested count of user stories
    user_story_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'user_story_count']

    def get_user_story_count(self, obj):
        return obj.user_stories.count()

# --- UserStory Serializer ---
class UserStorySerializer(serializers.ModelSerializer):
    # Read-only field for nested list of tasks
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = UserStory
        fields = ['id', 'project', 'title', 'description', 'acceptance_criteria', 'status', 'priority', 'created_at', 'updated_at', 'tasks']

    def get_tasks(self, obj):
        # Return a list of serialized task data
        task_data = []
        for task in obj.tasks.all():
            task_data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'is_complete': task.is_complete,
                'created_at': task.created_at,
                'updated_at': task.updated_at,
            })
        return task_data

    def validate_acceptance_criteria(self, value):
        """Validate that acceptance_criteria is not empty."""
        if not value or value.strip() == "":
            raise serializers.ValidationError("Acceptance criteria cannot be empty.")
        return value

# --- Task Serializer ---
class TaskSerializer(serializers.ModelSerializer):
    # Read-only display of parent user story title
    user_story_title = serializers.CharField(source='user_story.title', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'user_story', 'title', 'description', 'is_complete', 'created_at', 'updated_at', 'user_story_title']
