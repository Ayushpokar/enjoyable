from django.urls import path
from . import views


urlpatterns = [
     path('register/', views.register, name="register"),
    path('login/', views.handlelogin, name="login"),
    path('logout/', views.logout_view, name="logout"),

    path('', views.index, name='index'),
      path('home', views.index, name='home'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('searchtrain',views.searchtrain,name="searchtrain"),
    path('Train schedules/', views.schedules, name="Train schedules"),
   
    path("PNR status/",views.pnr_status,name="PNR status"),
    path("cancel ticket/",views.cancel_ticket,name="cancel ticket"),
    path("feedback/",views.feedback,name="feedback"),
    path("about us/",views.about,name='about us'),
    # for admin purpose 
    path("addtrains/",views.addtrains,name= "add trains"),
    path("addstation/",views.addstation,name="add station"),
    
    
    
]