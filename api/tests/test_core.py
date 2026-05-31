from django.test import TestCase
from apps.core.models import CoreModel

class CoreModelTest(TestCase):
    """Tests for the CoreModel."""

    def test_core_model_creation(self):
        """Test that a CoreModel instance can be created successfully."""
        model = CoreModel.objects.create(name="Test Project", description="A test description.")
        self.assertEqual(model.name, "Test Project")
        self.assertTrue(model.pk)

    def test_core_model_uniqueness(self):
        """Test that the name field enforces uniqueness."""
        CoreModel.objects.create(name="UniqueName", description="First one")
        with self.assertRaises(Exception): # Django ORM exception handling
            CoreModel.objects.create(name="UniqueName", description="Second one")
