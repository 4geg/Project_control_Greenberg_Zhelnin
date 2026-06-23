@echo off
chcp 65001 > nul

echo ==========================================
echo Запуск информационной системы управления проектами
echo ==========================================

if not exist ".venv" (
    echo Создание виртуального окружения...
    python -m venv .venv
)

echo Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo Установка зависимостей...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Выполнение миграций базы данных...
python manage.py migrate

echo Создание демонстрационного администратора...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')"

echo Открытие приложения в браузере...
start http://127.0.0.1:8000/

echo Запуск сервера...
python manage.py runserver

pause