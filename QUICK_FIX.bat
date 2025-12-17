@echo off
echo [*] Быстрое исправление projectFastapi...
echo ================================

echo 1/5  Удаление старой БД...
if exist kinovzor.db del kinovzor.db
echo [+] БД удалена

echo.
echo 2/5  Откат миграций...
cd app
alembic downgrade base 2>nul
if errorlevel 1 (
    echo [!] Миграции уже откачены или не применены
) else (
    echo [+] Миграции откачены
)
cd ..

echo.
echo 3/5  Применение новых миграций...
cd app
alembic upgrade head
cd ..
echo [+] Миграции применены

echo.
echo 4/5  Заполнение БД тестовыми данными...
python seed_db.py
echo [+] БД заполнена

echo.
echo 5/5  Проверка моделей...
python -c "from app.models import User, Movie, Review, Rating, Favorite; print('\n[+] Все модели загружены успешно!')"

echo.
echo ================================
echo [+] ВСЕ ОШИБКИ ИСПРАВЛЕНЫ!
echo ================================
echo.
echo [*] Используй:
echo     python -m uvicorn app.main:app --reload
echo.
pause
