from django.urls import path
from . import views


urlpatterns = [
     path('register/', views.register, name="register"),
    path('login/', views.handlelogin, name="login"),
    path('logout/', views.logout_view, name="logout"),

    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('search',views.searchtrain,name="search"),
    path('displaytn/',views.displaytn ,name="displaytn")  ,
    path('book',views.addpass,name="addpass"),
    path('reviewdetails',views.reviewdetails,name="reviewdetails"),
    path('payment',views.payment,name="payment"),
    path('Train schedules', views.schedules, name="Train schedules"),
    path('booking',views.booking,name="booking"),
   
    path("PNR status/",views.pnr_status,name="PNR status"),
    path("cancel ticket/",views.cancel_ticket,name="cancel ticket"),
    path("feedback/",views.feedback,name="feedback"),
    path("about us/",views.about,name='about us'),
    # for admin purpose 
    path('adminpanel',views.admin_panel,name="adminpanel"),
    path("addtrains/",views.addtrains,name= "add trains"),
    path("addstation/",views.addstation,name="add station"),
    path("addroutestn/",views.addroutestn,name="add route"),
    
    
    
]