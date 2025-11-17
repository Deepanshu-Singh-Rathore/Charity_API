from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet, CampaignViewSet, BeneficiaryViewSet, CharityListCreateView
from .api_root import api_root

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'campaigns', CampaignViewSet, basename='campaign')
router.register(r'beneficiaries', BeneficiaryViewSet, basename='beneficiary')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', api_root, name='api-root'),
    path('charities/', CharityListCreateView.as_view(), name='charity-list'),
    path('', include(router.urls)),
]
