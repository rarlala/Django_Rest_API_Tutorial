from django.urls import path

# from . import apis
from .apis import mixins

app_name = 'snippets'

urlpatterns = [
    # Class-based view를 사용하는 경우, as_view()함수를 호출
    path('snippets/', mixins.SnippetListCreateAPIView.as_view()),
    path('snippets/<int:pk>/', mixins.SnippetRetrieveUpdateDestroyAPIView.as_view()),
]
