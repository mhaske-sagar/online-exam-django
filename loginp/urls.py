"""loginp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path
from logapp import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,TokenVerifyView
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.homepage),
    path('login',views.login),
    path('register/',views.register),
    path('showregister/',views.showregister),
    path('ajax',views.ajax),
    path('add/',views.add),
    path('update/',views.update),
    path('delete/',views.delete),
    path('views',views.views),
    path('this/',views.this),
    path("next/",views.next),
    path("previous/",views.previous),
    path("cal/",views.cal),
    path("currentans/",views.currentans),
    path("showtime/",views.showtime),
    path("addUser",views.addUser),
    path("userUpdate",views.userUpdate),
    path("delete/<username>",views.userDelete),
    path("getuser/<username>",views.getuser),
    path("getalluser",views.getalluser),
    path("getuser1/<username>",views.getuser1),
    path("getalluser1",views.getalluser1),
    path("adduser1",views.adduser1),
    path('log',views.log),
    path("updateuser1",views.updateuser1),
    path("test",views.Abc.as_view()),
    path("qcontrol",views.Acb.as_view()),
    path("user",views.addd),
   
]
