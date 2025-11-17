from django.contrib import admin
from .models import Organization, Campaign, Beneficiary, Charity


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'registration_number')
    ordering = ('-created_at',)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'status', 'goal_amount', 'raised_amount', 'start_date', 'end_date')
    list_filter = ('status', 'start_date', 'organization')
    search_fields = ('title', 'description', 'organization__name')
    ordering = ('-created_at',)
    date_hierarchy = 'start_date'


@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'campaign', 'amount_received', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'campaign')
    search_fields = ('first_name', 'last_name', 'email', 'campaign__title')
    ordering = ('-created_at',)


@admin.register(Charity)
class CharityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'location', 'category')
    ordering = ('-created_at',)
