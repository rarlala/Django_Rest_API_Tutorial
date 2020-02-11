from django.urls import path

from . import apis

app_name = 'snippets'

urlpatterns = [
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>/', views.snippet_detail),

    # Class-based view를 사용하는 경우, as_view()함수를 호출
    path('snippets/', apis.SnippetListCreateAPIView.as_view()),
    path('snippets/<int:pk>/', apis.SnippetRetrieveUpdateDestroyAPIView.as_view()),
]
