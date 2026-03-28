@echo off
echo Активация виртуального окружения проекта...
call .venv\Scripts\activate.bat
echo.
echo Версия Python в виртуальном окружении:
python --version
echo.
echo Путь к Python:
where python
echo.
echo Виртуальное окружение активировано!
echo Для деактивации введите: deactivate
pause