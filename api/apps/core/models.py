import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

# Define choices for UserStory status
class UserStoryStatus(models.TextChoices):
    BACKLOG = 'backlog', _('Backlog')
    IN_PROGRESS = 'in_progress', _('In Progress')
    REVIEW = 'review', _('Review')
    DONE = 'done', _('Done')

class Project(models.Model):
    """Represents a high-level project container."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class UserStory(models.Model):
    """Represents a user story linked to a project."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, related_name='user_stories', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    acceptance_criteria = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=UserStoryStatus.choices,
        default=UserStoryStatus.BACKLOG
    )
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Story"
        verbose_name_plural = "User Stories"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.status.lower()}] {self.title}"

class Task(models.Model):
    """Represents a concrete task derived from a user story."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_story = models.ForeignKey(UserStory, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
