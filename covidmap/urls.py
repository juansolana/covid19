"""covidmap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.gis import admin
from django.urls import path, include
from c19map.views import symptons_view, signup_view, activate, activation_sent_view, login_view, logout_view
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('map/', include('c19map.urls')),
    path('add_case/', symptons_view, name='symptons_view' ),
    path('signup/', signup_view, name="signup"),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    # path('set_place/', include('c19map.urls'))
]
