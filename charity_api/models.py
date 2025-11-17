from django.db import models
from django.core.validators import MinValueValidator, EmailValidator


class Organization(models.Model):
    """
    Model representing a charity organization
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    registration_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    established_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name


class Campaign(models.Model):
    """
    Model representing a charity campaign
    """
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='campaigns'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    raised_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planning'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'

    def __str__(self):
        return f"{self.title} - {self.organization.name}"

    @property
    def progress_percentage(self):
        """Calculate the percentage of goal achieved"""
        if self.goal_amount > 0:
            return (self.raised_amount / self.goal_amount) * 100
        return 0


class Beneficiary(models.Model):
    """
    Model representing a beneficiary receiving help from campaigns
    """
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='beneficiaries'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, validators=[EmailValidator()])
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    needs_description = models.TextField(
        help_text="Description of what help the beneficiary needs"
    )
    amount_received = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Beneficiary'
        verbose_name_plural = 'Beneficiaries'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.campaign.title}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Charity(models.Model):
    """
    Charity entity to showcase on the site and via API
    """
    CATEGORY_CHOICES = [
        ("education", "Education"),
        ("health", "Health"),
        ("women_support", "Women Support"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to="charity_logos/", blank=True, null=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
            models.Index(fields=["location"]),
        ]

    def __str__(self):
        return self.name
