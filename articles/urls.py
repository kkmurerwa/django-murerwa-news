from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles),
    path('search/', views.search_article),
    path('<int:id>', views.article),
]