# API Quick Reference

## Base URL
```
http://127.0.0.1:8000/api/
```

## Organizations Endpoints

### List all organizations
```
GET /api/organizations/
```

### Create an organization
```
POST /api/organizations/
Content-Type: application/json

{
  "name": "Hope Foundation",
  "description": "Helping communities",
  "email": "contact@hopefoundation.org",
  "phone": "123-456-7890",
  "address": "123 Charity St",
  "website": "https://hopefoundation.org",
  "registration_number": "REG123",
  "established_date": "2020-01-01",
  "is_active": true
}
```

### Get specific organization with all campaigns
```
GET /api/organizations/{id}/
```

### Update organization
```
PUT /api/organizations/{id}/
PATCH /api/organizations/{id}/  (partial update)
```

### Delete organization
```
DELETE /api/organizations/{id}/
```

### Get active organizations only
```
GET /api/organizations/active/
```

### Get campaigns for an organization
```
GET /api/organizations/{id}/campaigns/
```

## Campaigns Endpoints

### List all campaigns
```
GET /api/campaigns/
```

### Create a campaign
```
POST /api/campaigns/
Content-Type: application/json

{
  "organization": 1,
  "title": "Winter Relief 2024",
  "description": "Providing winter essentials",
  "goal_amount": "50000.00",
  "raised_amount": "15000.00",
  "status": "active",
  "start_date": "2024-11-01",
  "end_date": "2024-12-31",
  "location": "Northern Region"
}
```

### Get specific campaign with all beneficiaries
```
GET /api/campaigns/{id}/
```

### Update campaign
```
PUT /api/campaigns/{id}/
PATCH /api/campaigns/{id}/  (partial update)
```

### Delete campaign
```
DELETE /api/campaigns/{id}/
```

### Get active campaigns only
```
GET /api/campaigns/active/
```

### Get beneficiaries for a campaign
```
GET /api/campaigns/{id}/beneficiaries/
```

### Update raised amount for a campaign
```
POST /api/campaigns/{id}/update_raised_amount/
Content-Type: application/json

{
  "amount": 1000.00
}
```

## Beneficiaries Endpoints

### List all beneficiaries
```
GET /api/beneficiaries/
```

### Create a beneficiary
```
POST /api/beneficiaries/
Content-Type: application/json

{
  "campaign": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "555-1234",
  "address": "456 Help St",
  "date_of_birth": "1990-01-01",
  "needs_description": "Requires food and clothing",
  "amount_received": "500.00",
  "is_active": true
}
```

### Get specific beneficiary
```
GET /api/beneficiaries/{id}/
```

### Update beneficiary
```
PUT /api/beneficiaries/{id}/
PATCH /api/beneficiaries/{id}/  (partial update)
```

### Delete beneficiary
```
DELETE /api/beneficiaries/{id}/
```

### Get active beneficiaries only
```
GET /api/beneficiaries/active/
```

### Update amount received by beneficiary
```
POST /api/beneficiaries/{id}/update_amount_received/
Content-Type: application/json

{
  "amount": 250.00
}
```

## Query Parameters

### Search
Search across multiple fields:
```
GET /api/organizations/?search=hope
GET /api/campaigns/?search=winter
GET /api/beneficiaries/?search=john
```

### Filtering
Filter by specific fields:
```
GET /api/organizations/?is_active=true
GET /api/campaigns/?status=active
GET /api/campaigns/?organization=1
GET /api/beneficiaries/?campaign=1
GET /api/beneficiaries/?is_active=true
```

### Ordering
Order results by field (prefix with `-` for descending):
```
GET /api/organizations/?ordering=name
GET /api/organizations/?ordering=-created_at
GET /api/campaigns/?ordering=-start_date
GET /api/beneficiaries/?ordering=last_name
```

### Pagination
Navigate through paginated results:
```
GET /api/organizations/?page=2
GET /api/campaigns/?page=3
```

### Combining Parameters
Combine multiple parameters:
```
GET /api/campaigns/?status=active&search=winter&ordering=-start_date&page=1
```

## Campaign Status Values
- `planning` - Campaign is being planned
- `active` - Campaign is currently active
- `completed` - Campaign has been completed
- `cancelled` - Campaign was cancelled

## Response Format

### List Response
```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/campaigns/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Campaign Title",
      ...
    }
  ]
}
```

### Error Response
```json
{
  "error": "Error message here"
}
```

## Using curl

### GET request
```bash
curl http://127.0.0.1:8000/api/organizations/
```

### POST request
```bash
curl -X POST http://127.0.0.1:8000/api/organizations/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Org", "email": "test@org.com"}'
```

### PUT request
```bash
curl -X PUT http://127.0.0.1:8000/api/organizations/1/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name", "email": "updated@org.com"}'
```

### DELETE request
```bash
curl -X DELETE http://127.0.0.1:8000/api/organizations/1/
```

## Using PowerShell (Windows)

### GET request
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/organizations/" -Method GET
```

### POST request
```powershell
$body = @{
    name = "Test Org"
    email = "test@org.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/organizations/" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

## Browsable API

You can also interact with the API using your web browser:
- Navigate to `http://127.0.0.1:8000/api/`
- Django REST Framework provides a browsable interface
- You can make GET, POST, PUT, DELETE requests directly from the browser
