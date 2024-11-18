from django.contrib import admin
from django.urls import path, include
from core.views import signup_view  # Import the new home view

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', signup_view, name='signup'),  # Add the root path
    path('account/', include('core.urls')),  # This will still work for all other paths
]
