"""
URL configuration for charity_project project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from charity_api.web_views import HomeView, OrganizationsView, CampaignsView, BeneficiariesView, CharitiesView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('organizations/', OrganizationsView.as_view(), name='organizations'),
    path('campaigns/', CampaignsView.as_view(), name='campaigns'),
    path('beneficiaries/', BeneficiariesView.as_view(), name='beneficiaries'),
    path('charities/', CharitiesView.as_view(), name='charities'),
    path('admin/', admin.site.urls),
    path('api/', include('charity_api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site
admin.site.site_header = "🤝 Charity API Administration"
admin.site.site_title = "Charity API Admin"
admin.site.index_title = "Welcome to Charity API Administration"
