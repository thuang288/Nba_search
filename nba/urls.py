from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:pk>/', views.post_detail, name='post-detail'),
    path('delete/<player_name>/', views.delete, name='delete')
]