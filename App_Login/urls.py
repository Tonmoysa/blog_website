from django.urls import path
from . import views


app_name='App_Login'
urlpatterns = [
   path('signup/',views.sign_up,name='signup'),
   path('login/',views.login_page,name='login'),
   path('logout/',views.logout_user,name='logout'),
   path('profile/',views.profile,name='profile'),
   path('change-profile/',views.user_change,name='user_change'),
   path('password/',views.change_password,name='change_password'),
   path('add-picture/',views.add_profile_picture,name='add_picture'),
   path('change-picture/',views.change_pro_pic,name='change_pro_pic'),
     
]

