from rest_framework import generics

from ..models import Snippet
from ..serializers import SnippetSerializer

class SnippetListCreateAPIView(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

class SnippetRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
