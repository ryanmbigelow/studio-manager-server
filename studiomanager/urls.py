"""studiomanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from studiomanagerapi.views.auth import check_user, register_user
from studiomanagerapi.views import CategoryView, EngineerView, GearView, SessionEngineerView, SessionView

# each table has its own url
# connected to the corresponding viewset.
# when an api call is made,
# the viewset is called and completes the request
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryView, 'category')
router.register(r'engineers', EngineerView, 'engineer')
router.register(r'gear', GearView, 'gear')
router.register(r'session_engineers', SessionEngineerView, 'session_engineer')
router.register(r'sessions', SessionView, 'session')

# register and checkuser have their own url paths
# because they need to be called for authentication
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('checkuser', check_user),
]
