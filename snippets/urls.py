from django.urls import path

from . import views

app_name = 'snippets'
urlpatterns = [
    path('snippets/', views.snippet_list)
]