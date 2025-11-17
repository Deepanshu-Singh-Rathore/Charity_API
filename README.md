# Charity REST API

A comprehensive REST API for managing charity organizations, campaigns, and beneficiaries built with Django and Django REST Framework.

## Features

- **Organizations Management**: Create, view, update, and track charity organizations
- **Campaigns Management**: Manage charity campaigns with goal tracking and status monitoring
- **Beneficiaries Management**: Track beneficiaries and their needs across campaigns
- **Charity Directory**: Public, read-only charities endpoint and a single UI screen
- **Search & Filtering**: Advanced search and filtering capabilities across all models
- **Pagination**: Built-in pagination for all list endpoints
- **Admin Interface**: Django admin panel for easy management

## Models

### Organization
- Name, description, contact information
- Registration number and establishment date
- Active status tracking
- Automatic timestamps

### Campaign
- Associated with an organization
- Title, description, and location
- Goal amount and raised amount tracking
- Status (Planning, Active, Completed, Cancelled)
- Start and end dates
- Progress percentage calculation

### Beneficiary
- Associated with a campaign
- Personal information and contact details
- Needs description
- Amount received tracking
- Active status

## API Endpoints

### Organizations
- `GET /api/organizations/` - List all organizations
- `POST /api/organizations/` - Create a new organization
- `GET /api/organizations/{id}/` - Retrieve an organization
- `PUT /api/organizations/{id}/` - Update an organization
- `PATCH /api/organizations/{id}/` - Partial update
- `DELETE /api/organizations/{id}/` - Delete an organization
- `GET /api/organizations/active/` - List active organizations
- `GET /api/organizations/{id}/campaigns/` - Get campaigns for an organization

### Campaigns
- `GET /api/campaigns/` - List all campaigns
- `POST /api/campaigns/` - Create a new campaign
- `GET /api/campaigns/{id}/` - Retrieve a campaign
- `PUT /api/campaigns/{id}/` - Update a campaign
- `PATCH /api/campaigns/{id}/` - Partial update
- `DELETE /api/campaigns/{id}/` - Delete a campaign
- `GET /api/campaigns/active/` - List active campaigns
- `GET /api/campaigns/{id}/beneficiaries/` - Get beneficiaries for a campaign
- `POST /api/campaigns/{id}/update_raised_amount/` - Update raised amount

### Beneficiaries
- `GET /api/beneficiaries/` - List all beneficiaries
- `POST /api/beneficiaries/` - Create a new beneficiary
- `GET /api/beneficiaries/{id}/` - Retrieve a beneficiary
- `PUT /api/beneficiaries/{id}/` - Update a beneficiary
- `PATCH /api/beneficiaries/{id}/` - Partial update
- `DELETE /api/beneficiaries/{id}/` - Delete a beneficiary
- `GET /api/beneficiaries/active/` - List active beneficiaries
- `POST /api/beneficiaries/{id}/update_amount_received/` - Update amount received

## Query Parameters

### Search
Add `?search=keyword` to search across relevant fields:
- Organizations: name, description, email, registration number
- Campaigns: title, description, location, organization name
- Beneficiaries: first name, last name, email, needs description, campaign title

### Filtering
Add filter parameters to narrow down results:
- Organizations: `?is_active=true`, `?established_date=2023-01-01`
- Campaigns: `?status=active`, `?organization=1`, `?start_date=2023-01-01`
- Beneficiaries: `?campaign=1`, `?is_active=true`

### Ordering
Add `?ordering=field_name` or `?ordering=-field_name` (descending):
- Organizations: name, created_at, established_date
- Campaigns: title, created_at, start_date, end_date, goal_amount, raised_amount
- Beneficiaries: first_name, last_name, created_at, amount_received

### Pagination
- Results are paginated with 10 items per page by default
- Use `?page=2` to get the next page
- Response includes `count`, `next`, and `previous` fields

## Setup Instructions

### 1. Create a virtual environment (Already done!)
The virtual environment is already created at `.venv`

### 2. Activate the virtual environment
```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies (Already done!)
Dependencies are already installed. If needed:
```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables (Optional)
Copy `.env.example` to `.env` and update values if needed:
```powershell
copy .env.example .env
```

### 5. Run migrations (Already done!)
Migrations are already applied. If needed:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (for admin access)
**Make sure virtual environment is activated first!**
```powershell
python manage.py createsuperuser
```
Or use the full path:
```powershell
.venv\Scripts\python.exe manage.py createsuperuser
```

### 7. Run the development server
```powershell
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`

## Admin Interface

Access the Django admin panel at `http://127.0.0.1:8000/admin/` to manage data through a web interface.

## Example API Usage

### Create an Organization
```bash
curl -X POST http://127.0.0.1:8000/api/organizations/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hope Foundation",
    "description": "Helping communities in need",
    "email": "contact@hopefoundation.org",
    "phone": "123-456-7890"
  }'
```

### Create a Campaign
```bash
curl -X POST http://127.0.0.1:8000/api/campaigns/ \
  -H "Content-Type: application/json" \
  -d '{
    "organization": 1,
    "title": "Food Drive 2024",
    "description": "Providing meals to families",
    "goal_amount": 10000.00,
    "status": "active",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
  }'
```

### Search Campaigns
```bash
curl http://127.0.0.1:8000/api/campaigns/?search=food
```

### Filter by Status
```bash
curl http://127.0.0.1:8000/api/campaigns/?status=active
```

## Charity Section

This section adds a public charities directory with one frontend page and an API endpoint. Records are created via the Django Admin only.

- UI: `GET /charities/` (single screen, dynamically loads from API)
- API: `GET /api/charities/` (paginated list, supports `search`, `category`, `location`)
- API: `POST /api/charities/` (admin-only; supports `multipart/form-data` for logo uploads)
- Admin: Manage under `Admin > Charities`

### Model
- `name` (CharField 200)
- `category` (choices: `education`, `health`, `women_support`, `other`)
- `location` (CharField 200, optional)
- `logo` (ImageField, optional; uploads to `charity_logos/`)
- `link` (URLField, optional)
- `created_at` (auto_now_add)

### Example API Response
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Hope Foundation",
      "category": "education",
      "location": "New York, USA",
      "logo": "http://127.0.0.1:8000/media/charity_logos/hope.png",
      "link": "https://hope.org",
      "created_at": "2025-11-17T10:00:00Z"
    },
    {
      "id": 2,
      "name": "Health for All",
      "category": "health",
      "location": "Berlin, DE",
      "logo": null,
      "link": null,
      "created_at": "2025-11-16T08:30:00Z"
    }
  ]
}
```

### Example POST (multipart/form-data, admin only)
```bash
curl -X POST http://127.0.0.1:8000/api/charities/ \
  -H "Authorization: Token <ADMIN_TOKEN_OR_SESSION>" \
  -H "Accept: application/json" \
  -F "name=Hope Foundation" \
  -F "category=education" \
  -F "location=New York, USA" \
  -F "link=https://hope.org" \
  -F "logo=@/path/to/logo.png"
```

### MEDIA Setup (Development)
Already configured in this project. Ensure the following:
- In `settings.py`: `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / 'media'`
- In `urls.py` (project-level): `urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` when `DEBUG=True`

### Adding Items via Admin
1. Create a superuser if not done:
```powershell
python manage.py createsuperuser
```
2. Log in at `http://127.0.0.1:8000/admin/`
3. Add entries under `Charities`

### Frontend Screen
- Access at: `http://127.0.0.1:8000/charities/`
- Shows logo, name, category, location, and two buttons: "Know More" and "Donate" (open the `link` in a new tab)

### Screenshot
Add a screenshot here: `docs/images/charities_screen.png` (placeholder)

## Technologies Used

- Django 4.2.7
- Django REST Framework 3.14.0
- django-filter 23.3
- python-decouple 3.8
- SQLite (default database)

## License

This project is open source and available for educational purposes.
