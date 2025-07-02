from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/trees/', views.tree_list, name='tree_list'),
]
