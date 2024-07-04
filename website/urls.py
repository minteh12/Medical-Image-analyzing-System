"""core URL Configuration

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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import index
from .views import contact
from .views import about
from.views import home
from .views import index1
from .views import index2
from .views import login
from .views import add_patient
from .views import view_patients
from .views import logout
from .views import download_patients_with_images
urlpatterns = [
    path("", login, name="login"),
    path("login", login, name="login"),
    path("admin/", admin.site.urls),
    path("contact/", contact, name="contact"),
    path("brain/", index, name="index"),
    path("about/", about, name="about"),
    path("home/", home, name="home"),
    path("lungcancer/", index1, name="index1"),
    path("lungdisease/", index2, name="index2"),
    path("add/", add_patient, name="add_patient"),
    path("viewdata/", view_patients, name="view_patients"),
    path("download_patients_with_images", download_patients_with_images, name="download_patients_with_images"),
    path('logout/', logout, name='logout')

]

if settings.DEBUG:
    # setting this to view media files from admin panel
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
