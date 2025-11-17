"""
Quick Start Guide for Charity REST API

This script demonstrates how to use the API endpoints.
First, start the development server in another terminal with:
    python manage.py runserver

Then you can test the API using the examples below or run this script.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"


def print_response(response, title):
    """Helper function to print formatted responses"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    if response.status_code < 400:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")


def test_api():
    """Test the API endpoints"""
    
    # 1. Create an Organization
    print("\n1. Creating an Organization...")
    org_data = {
        "name": "Hope Foundation",
        "description": "Providing hope to communities in need",
        "email": "contact@hopefoundation.org",
        "phone": "123-456-7890",
        "address": "123 Charity St, Goodville",
        "website": "https://hopefoundation.org",
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/organizations/", json=org_data)
    print_response(response, "Create Organization")
    org_id = response.json().get('id') if response.status_code == 201 else None
    
    # 2. List Organizations
    print("\n2. Listing all Organizations...")
    response = requests.get(f"{BASE_URL}/organizations/")
    print_response(response, "List Organizations")
    
    # 3. Create a Campaign
    if org_id:
        print("\n3. Creating a Campaign...")
        campaign_data = {
            "organization": org_id,
            "title": "Winter Relief Campaign 2024",
            "description": "Providing warm clothing and food for winter",
            "goal_amount": "50000.00",
            "raised_amount": "15000.00",
            "status": "active",
            "start_date": "2024-11-01",
            "end_date": "2024-12-31",
            "location": "Northern Region"
        }
        response = requests.post(f"{BASE_URL}/campaigns/", json=campaign_data)
        print_response(response, "Create Campaign")
        campaign_id = response.json().get('id') if response.status_code == 201 else None
        
        # 4. Create a Beneficiary
        if campaign_id:
            print("\n4. Creating a Beneficiary...")
            beneficiary_data = {
                "campaign": campaign_id,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "555-1234",
                "address": "456 Help St, Needville",
                "needs_description": "Requires winter clothing and food supplies for family of 4",
                "amount_received": "500.00",
                "is_active": True
            }
            response = requests.post(f"{BASE_URL}/beneficiaries/", json=beneficiary_data)
            print_response(response, "Create Beneficiary")
    
    # 5. Search Campaigns
    print("\n5. Searching Campaigns with 'winter'...")
    response = requests.get(f"{BASE_URL}/campaigns/?search=winter")
    print_response(response, "Search Campaigns")
    
    # 6. Filter Active Campaigns
    print("\n6. Getting Active Campaigns...")
    response = requests.get(f"{BASE_URL}/campaigns/active/")
    print_response(response, "Active Campaigns")
    
    # 7. Get Organization with Campaigns
    if org_id:
        print(f"\n7. Getting Organization {org_id} with Campaigns...")
        response = requests.get(f"{BASE_URL}/organizations/{org_id}/")
        print_response(response, "Organization Details")


if __name__ == "__main__":
    print("="*60)
    print("Charity REST API - Test Script")
    print("="*60)
    print("\nMake sure the server is running with:")
    print("  python manage.py runserver")
    print("\nStarting API tests...")
    
    try:
        test_api()
        print("\n" + "="*60)
        print("Tests completed successfully!")
        print("="*60)
    except requests.exceptions.ConnectionError:
        print("\n" + "="*60)
        print("ERROR: Could not connect to the server!")
        print("Please start the server with: python manage.py runserver")
        print("="*60)
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
