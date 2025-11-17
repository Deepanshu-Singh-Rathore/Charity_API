from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Organization, Campaign, Beneficiary, Charity
from .serializers import (
    OrganizationSerializer,
    OrganizationDetailSerializer,
    CampaignSerializer,
    CampaignDetailSerializer,
    BeneficiarySerializer,
    CharitySerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    🏢 **Organization Management**
    
    Manage charity organizations with full CRUD operations.
    
    ## 📋 List Organizations
    `GET /api/organizations/`
    
    ## ➕ Create Organization
    `POST /api/organizations/`
    
    ## 🔍 Retrieve Organization
    `GET /api/organizations/{id}/`
    
    ## ✏️ Update Organization
    `PUT /api/organizations/{id}/` or `PATCH /api/organizations/{id}/`
    
    ## 🗑️ Delete Organization
    `DELETE /api/organizations/{id}/`
    
    ### 🔎 Search & Filter Options:
    - **Search**: `?search=foundation` (searches name, description, email, registration number)
    - **Filter Active**: `?is_active=true`
    - **Filter by Date**: `?established_date=2023-01-01`
    - **Order By**: `?ordering=-created_at` (use `-` for descending)
    
    ### 🔗 Special Endpoints:
    - Active Organizations: `/api/organizations/active/`
    - Organization Campaigns: `/api/organizations/{id}/campaigns/`
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Search fields
    search_fields = ['name', 'description', 'email', 'registration_number']
    
    # Filter fields
    filterset_fields = ['is_active', 'established_date']
    
    # Ordering fields
    ordering_fields = ['name', 'created_at', 'established_date']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return OrganizationDetailSerializer
        return OrganizationSerializer

    @action(detail=True, methods=['get'])
    def campaigns(self, request, pk=None):
        """
        Get all campaigns for a specific organization
        /api/organizations/{id}/campaigns/
        """
        organization = self.get_object()
        campaigns = organization.campaigns.all()
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get all active organizations
        /api/organizations/active/
        """
        active_orgs = self.queryset.filter(is_active=True)
        page = self.paginate_queryset(active_orgs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(active_orgs, many=True)
        return Response(serializer.data)


class CampaignViewSet(viewsets.ModelViewSet):
    """
    🎯 **Campaign Management**
    
    Manage charity campaigns with goal tracking and status monitoring.
    
    ## 📋 List Campaigns
    `GET /api/campaigns/`
    
    ## ➕ Create Campaign
    `POST /api/campaigns/`
    
    ## 🔍 Retrieve Campaign
    `GET /api/campaigns/{id}/`
    
    ## ✏️ Update Campaign
    `PUT /api/campaigns/{id}/` or `PATCH /api/campaigns/{id}/`
    
    ## 🗑️ Delete Campaign
    `DELETE /api/campaigns/{id}/`
    
    ### 🔎 Search & Filter Options:
    - **Search**: `?search=winter` (searches title, description, location, organization name)
    - **Filter by Status**: `?status=active` (planning, active, completed, cancelled)
    - **Filter by Organization**: `?organization=1`
    - **Filter by Date**: `?start_date=2024-01-01`
    - **Order By**: `?ordering=-start_date`
    
    ### 🔗 Special Endpoints:
    - Active Campaigns: `/api/campaigns/active/`
    - Campaign Beneficiaries: `/api/campaigns/{id}/beneficiaries/`
    - Update Raised Amount: `POST /api/campaigns/{id}/update_raised_amount/`
    """
    queryset = Campaign.objects.select_related('organization').all()
    serializer_class = CampaignSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Search fields
    search_fields = ['title', 'description', 'location', 'organization__name']
    
    # Filter fields
    filterset_fields = ['status', 'organization', 'start_date', 'end_date']
    
    # Ordering fields
    ordering_fields = ['title', 'created_at', 'start_date', 'end_date', 'goal_amount', 'raised_amount']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return CampaignDetailSerializer
        return CampaignSerializer

    @action(detail=True, methods=['get'])
    def beneficiaries(self, request, pk=None):
        """
        Get all beneficiaries for a specific campaign
        /api/campaigns/{id}/beneficiaries/
        """
        campaign = self.get_object()
        beneficiaries = campaign.beneficiaries.all()
        serializer = BeneficiarySerializer(beneficiaries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get all active campaigns
        /api/campaigns/active/
        """
        active_campaigns = self.queryset.filter(status='active')
        page = self.paginate_queryset(active_campaigns)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(active_campaigns, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_raised_amount(self, request, pk=None):
        """
        Update the raised amount for a campaign
        POST /api/campaigns/{id}/update_raised_amount/
        Body: {"amount": 1000.00}
        """
        campaign = self.get_object()
        amount = request.data.get('amount')
        
        if amount is None:
            return Response(
                {'error': 'Amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("Amount must be positive")
            
            campaign.raised_amount += amount
            campaign.save()
            serializer = self.get_serializer(campaign)
            return Response(serializer.data)
        except (ValueError, TypeError) as e:
            return Response(
                {'error': f'Invalid amount: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class BeneficiaryViewSet(viewsets.ModelViewSet):
    """
    👥 **Beneficiary Management**
    
    Manage beneficiaries who receive help from charity campaigns.
    
    ## 📋 List Beneficiaries
    `GET /api/beneficiaries/`
    
    ## ➕ Create Beneficiary
    `POST /api/beneficiaries/`
    
    ## 🔍 Retrieve Beneficiary
    `GET /api/beneficiaries/{id}/`
    
    ## ✏️ Update Beneficiary
    `PUT /api/beneficiaries/{id}/` or `PATCH /api/beneficiaries/{id}/`
    
    ## 🗑️ Delete Beneficiary
    `DELETE /api/beneficiaries/{id}/`
    
    ### 🔎 Search & Filter Options:
    - **Search**: `?search=john` (searches first name, last name, email, needs, campaign title)
    - **Filter by Campaign**: `?campaign=1`
    - **Filter Active**: `?is_active=true`
    - **Order By**: `?ordering=last_name`
    
    ### 🔗 Special Endpoints:
    - Active Beneficiaries: `/api/beneficiaries/active/`
    - Update Amount Received: `POST /api/beneficiaries/{id}/update_amount_received/`
    """
    queryset = Beneficiary.objects.select_related('campaign', 'campaign__organization').all()
    serializer_class = BeneficiarySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Search fields
    search_fields = ['first_name', 'last_name', 'email', 'needs_description', 'campaign__title']
    
    # Filter fields
    filterset_fields = ['campaign', 'is_active', 'date_of_birth']
    
    # Ordering fields
    ordering_fields = ['first_name', 'last_name', 'created_at', 'amount_received']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get all active beneficiaries
        /api/beneficiaries/active/
        """
        active_beneficiaries = self.queryset.filter(is_active=True)
        page = self.paginate_queryset(active_beneficiaries)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(active_beneficiaries, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_amount_received(self, request, pk=None):
        """
        Update the amount received by a beneficiary
        POST /api/beneficiaries/{id}/update_amount_received/
        Body: {"amount": 500.00}
        """
        beneficiary = self.get_object()
        amount = request.data.get('amount')
        
        if amount is None:
            return Response(
                {'error': 'Amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("Amount must be positive")
            
            beneficiary.amount_received += amount
            beneficiary.save()
            serializer = self.get_serializer(beneficiary)
            return Response(serializer.data)
        except (ValueError, TypeError) as e:
            return Response(
                {'error': f'Invalid amount: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class CharityListCreateView(generics.ListCreateAPIView):
    """
    🌍 Charity Directory

    - GET /api/charities/ — List charities (paginated, searchable)
    - POST /api/charities/ — Create charity (JSON or multipart)

    Search: ?search=term (name, category, location)
    Filter: ?category=education&location=City
    """
    queryset = Charity.objects.all()
    serializer_class = CharitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category', 'location']
    filterset_fields = ['category', 'location']
    ordering_fields = ['created_at', 'name', 'category']
    ordering = ['-created_at']
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        """Allow public GETs but restrict POSTs to admin users only"""
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]
