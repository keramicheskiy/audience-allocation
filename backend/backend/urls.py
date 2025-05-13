from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teachers', include('apps.teachers.urls')),
    path('', include('apps.authentication.urls')),
    path('administration', include('apps.administration.urls')),
    path('education', include('apps.education.urls')),
    path('moderation', include('apps.moderation.urls')),
]

