from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from forums.views import custom_logout



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forums.urls')),  # or your actual app name
    # Add the following for authentication:
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', custom_logout, name='logout'),] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
