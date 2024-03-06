from django.urls import path
from . import views


urlpatterns = [
     path('register/', views.register, name="register"),
    path('login/', views.handlelogin, name="login"),
    path('logout/', views.logout_view, name="logout"),

    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('search',views.searchtrains,name="search"),  # search train by source and destination
    path('Train schedules/', views.schedules, name="Train schedules"),
    #path("add_train/",views.add_train,name="Add Train"),
    path("PNR status/",views.pnr_status,name="PNR status"),
    path("cancel ticket/",views.cancel_ticket,name="cancel ticket"),
    path("feedback/",views.feedback,name="feedback"),
    
    # for admin purpose 
    path("addtrains/",views.addtrains,name= "add trains"),
    path("addstation/",views.addstation,name="add station"),
    
    
    
]