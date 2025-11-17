from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET'])
def api_root(request, format=None):
    """
    # 🤝 Welcome to Charity REST API
    
    A comprehensive REST API for managing charity organizations, campaigns, and beneficiaries.
    
    ## 📚 Available Endpoints:
    
    Explore the endpoints below to interact with the API.
    """
    return Response({
        'organizations': reverse('organization-list', request=request, format=format),
        'campaigns': reverse('campaign-list', request=request, format=format),
        'beneficiaries': reverse('beneficiary-list', request=request, format=format),
        'admin': '/admin/',
        'documentation': {
            'description': 'API provides full CRUD operations with search, filtering, and pagination',
            'features': [
                'Search across multiple fields',
                'Filter by status, organization, campaign',
                'Pagination (10 items per page)',
                'Ordering by various fields'
            ],
            'query_parameters': {
                'search': '?search=keyword',
                'filter': '?status=active&is_active=true',
                'ordering': '?ordering=-created_at',
                'pagination': '?page=2'
            }
        },
        'quick_links': {
            'active_organizations': reverse('organization-active', request=request, format=format),
            'active_campaigns': reverse('campaign-active', request=request, format=format),
            'active_beneficiaries': reverse('beneficiary-active', request=request, format=format),
        }
    })
