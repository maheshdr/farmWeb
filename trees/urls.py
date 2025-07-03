from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/trees/', views.tree_list, name='tree_list'),
    path('api/trees/<int:pk>/', views.tree_detail, name='tree_detail'),
    path('dashboard/trees/', views.tree_admin_list, name='tree_admin_list'),
    path('dashboard/trees/create/', views.tree_create, name='tree_create'),
    path('dashboard/trees/<int:pk>/update/', views.tree_update, name='tree_update'),
    path('dashboard/trees/<int:pk>/delete/', views.tree_delete, name='tree_delete'),
]
