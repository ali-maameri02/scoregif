"""
URL configuration for football_predictions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from predictions import views
from django.conf.urls.static import static
# from django.conf.urls.i18n import i18n_patterns

from predictions.views import home
# urlpatterns = [
#     path("i18n/", include("django.conf.urls.i18n")),
# ]command 'pythonIndent.newlineAndIndent' not found
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('predictions.urls')),
    path('', views.home, name='home'),  # This is your home URL
    path('twitter/callback/', views.twitter_authenticate, name='twitter_callback'),  # Add this line
]

# Other URL patterns...

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
