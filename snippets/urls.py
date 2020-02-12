from django.urls import path, include

# from . import apis
from rest_framework.routers import DefaultRouter

from .apis import mixins, generic, viewsets

app_name = 'snippets'

router = DefaultRouter()
router.register(r'snippets', viewsets.SnippetViewSet)

urlpatterns_api_view = [
    path('snippets/', generic.SnippetListCreateAPIView.as_view()),
    path('snippets/<int:pk>/', generic.SnippetRetrieveUpdateDestroyAPIView.as_view()),
]

urlpatterns_viewset = [
    path('snippets/', viewsets.SnippetViewSet.as_view({
        'get':'list',
        'post':'create'
    })),
    path('snippets/<int:pk>/', viewsets.SnippetViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    })),
]

urlpatterns = [
    # Class-based view를 사용하는 경우, as_view()함수를 호출
    path('api-view/', include(urlpatterns_api_view)),
    path('viewset/', include(urlpatterns_viewset)),
    path('router/', include(router.urls)),
]