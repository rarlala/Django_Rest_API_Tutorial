from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Snippet
from ..serializers import SnippetSerializer

# apis모듈을 apis패키지로 만들고,
# apis.api_view 모듈에 이 파일에 있는 내용을 옮기기
# snippets.urls에서 APIView들을 가져오는 경로를 적절히 수정

# apis.py(기존)
# apis/
#   __init__.py
#   api_view.py <- 여기


class SnippetListCreateAPIView (APIView):
    def get(self, request):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self,pk):
        return get_object_or_404(Snippet, pk=pk)

    def get(self, request, pk):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def patch(self, request, pk):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
