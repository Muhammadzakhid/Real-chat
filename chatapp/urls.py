from django.contrib import admin
from django.urls import path, re_path
from chat import views
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.LoginPage, name="login"),
]