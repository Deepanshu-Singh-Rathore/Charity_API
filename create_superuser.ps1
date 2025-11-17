# Activate virtual environment and create superuser

Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1

Write-Host "`nCreating superuser..." -ForegroundColor Green
python manage.py createsuperuser
