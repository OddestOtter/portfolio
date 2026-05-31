from rest_framework import viewsets
from .models import CoreModel
from .serializers import CoreModelSerializer

class CoreModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CoreModel instances to be viewed or edited.
    """
    queryset = CoreModel.objects.all()
    serializer_class = CoreModelSerializer
