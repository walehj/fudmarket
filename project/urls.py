"""fudmarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls'))

    # password reset
    path('password-reset', auth_views.password_reset, name="password_reset"),
    path('password-reset/done', auth_views.password_reset_done,
         name="password_reset_done"),
    url(r'^password-reset/confirm/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/$',
        auth_views.password_reset_confirm, name="password_reset_confirm"),
    path('password-reset/complete', auth_views.password_reset_complete,
         name="password_reset_complete"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Customizing admin texts
admin.site.site_header = 'Fudmarket'
admin.site.index_title = 'Welcome to fudmarket project'
admin.site.site_title = 'Control Panel'
