from django.contrib import admin
from django.urls import path

from .views import *
from home.views import home_view

urlpatterns = [
    path('', home_view),
    path('logins/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('registers/', register, name="register"),
    path('login1/', login1, name="login1"),
    path('login2/', login2, name="login2"),
    path('thankyou/', thankyou, name="thankyou"),
    path('payment/', payment, name="payment"),
    path('otp/', otp, name="otp"),
    path('output/', output, name="output"),
    path('dashboard/', dashboard, name="dashboard"),
    path('admins/', admins, name="admins"),
    path('adminlogin/', adminlogin, name="adminlogin"),
    path('remaining/', remaining, name="remaining"),
    path('debit/', debit, name="debit"),
    path('contactus/', contactus, name="contactus"),
]
