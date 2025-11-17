from rest_framework import serializers
from .models import Organization, Campaign, Beneficiary, Charity


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for Organization model
    """
    campaign_count = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'description',
            'email',
            'phone',
            'address',
            'website',
            'registration_number',
            'established_date',
            'is_active',
            'campaign_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_campaign_count(self, obj):
        """Get the total number of campaigns for this organization"""
        return obj.campaigns.count()


class CampaignSerializer(serializers.ModelSerializer):
    """
    Serializer for Campaign model
    """
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    beneficiary_count = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id',
            'organization',
            'organization_name',
            'title',
            'description',
            'goal_amount',
            'raised_amount',
            'progress_percentage',
            'status',
            'start_date',
            'end_date',
            'location',
            'beneficiary_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'progress_percentage']

    def get_beneficiary_count(self, obj):
        """Get the total number of beneficiaries for this campaign"""
        return obj.beneficiaries.count()

    def validate(self, data):
        """
        Validate that end_date is after start_date
        """
        if 'start_date' in data and 'end_date' in data:
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError(
                    "End date must be after start date."
                )
        return data


class BeneficiarySerializer(serializers.ModelSerializer):
    """
    Serializer for Beneficiary model
    """
    campaign_title = serializers.CharField(source='campaign.title', read_only=True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Beneficiary
        fields = [
            'id',
            'campaign',
            'campaign_title',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'address',
            'date_of_birth',
            'needs_description',
            'amount_received',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'full_name']


# Detailed serializers with nested data
class CampaignDetailSerializer(CampaignSerializer):
    """
    Detailed serializer for Campaign with nested beneficiaries
    """
    beneficiaries = BeneficiarySerializer(many=True, read_only=True)

    class Meta(CampaignSerializer.Meta):
        fields = CampaignSerializer.Meta.fields + ['beneficiaries']


class OrganizationDetailSerializer(OrganizationSerializer):
    """
    Detailed serializer for Organization with nested campaigns
    """
    campaigns = CampaignSerializer(many=True, read_only=True)

    class Meta(OrganizationSerializer.Meta):
        fields = OrganizationSerializer.Meta.fields + ['campaigns']


class CharitySerializer(serializers.ModelSerializer):
    """
    Serializer for Charity model supporting logo uploads and read-only created_at
    """
    class Meta:
        model = Charity
        fields = [
            'id',
            'name',
            'category',
            'location',
            'logo',
            'link',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
