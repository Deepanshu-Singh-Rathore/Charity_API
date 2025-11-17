from django.shortcuts import render
from django.views import View


class HomeView(View):
    """Homepage view displaying charity statistics and featured content"""
    def get(self, request):
        return render(request, 'charity/home.html')


class OrganizationsView(View):
    """View displaying all organizations"""
    def get(self, request):
        return render(request, 'charity/organizations.html')


class CampaignsView(View):
    """View displaying all campaigns"""
    def get(self, request):
        return render(request, 'charity/campaigns.html')


class BeneficiariesView(View):
    """View displaying all beneficiaries"""
    def get(self, request):
        return render(request, 'charity/beneficiaries.html')


class CharitiesView(View):
    """Single screen that lists charities from the API"""
    def get(self, request):
        return render(request, 'charity/charity_list.html')
