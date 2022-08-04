from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.profile),
    path('create/', views.create_profile),
    path('update/<int:id>', views.update_profile),
]
