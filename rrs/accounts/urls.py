from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.handlelogin, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('dashboard/',views.dashboard, name="dashboard"),
]