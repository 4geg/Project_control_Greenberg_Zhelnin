@echo off

echo ==========================================
echo Starting Project Management System
echo ==========================================

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Applying database migrations...
python manage.py migrate

echo Creating demo admin user...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')"

echo Opening browser...
start http://127.0.0.1:8000/

echo Starting Django server...
python manage.py runserver

pause