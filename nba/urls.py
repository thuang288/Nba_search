from django.urls import path
from .views import PostDetailView
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('delete/<player_name>/', views.delete, name='delete')
]