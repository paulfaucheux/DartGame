"""dart_game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from darts.views import HomeView, GameView, AboutView, ContactView, cancelLastDart_FV

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view()),
    url(r'^game/$', GameView.as_view()),
    url(r'^game_back/$', cancelLastDart_FV),
    url(r'^about/$', AboutView.as_view()),
    url(r'^home/$', HomeView.as_view()),
    url(r'^contact/$', ContactView.as_view()),
]
