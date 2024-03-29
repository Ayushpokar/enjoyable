from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('about us/', views.about, name='about us'),
    path('contact us/', views.contact, name='contact us'),
    path('Train schedules/', views.schedules, name='Train schedules'),
    path('PNR status/', views.pnr_status, name='PNR status'),
    path('cancel ticket/', views.cancel_ticket, name='cancel ticket'),
    path('feedback', views.feedback, name='feedback'),
    path('login', views.handlelogin, name="login"),
    path('register/', views.register, name="register"),
    path('dashboard', views.dashboard, name='dashboard')
    
    
]
