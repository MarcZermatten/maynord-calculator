@echo off
chcp 65001 >nul
title Maynord Calculator

:: Check if virtual environment exists
if exist venv\Scripts\python.exe (
    goto :run
)

:: First time setup - Install everything
echo.
echo ═══════════════════════════════════════════════════════
echo   MAYNORD CALCULATOR - Installation automatique
echo ═══════════════════════════════════════════════════════
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python n'est pas installe.
    echo.
    echo     Veuillez installer Python 3.11+ depuis:
    echo     https://www.python.org/downloads/
    echo.
    echo     IMPORTANT: Cochez "Add Python to PATH" !
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python trouve
python --version
echo.
echo Installation en cours, veuillez patienter...
echo.

:: Create virtual environment silently
python -m venv venv >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Erreur creation environnement
    pause
    exit /b 1
)
echo [OK] Environnement cree

:: Install dependencies
call venv\Scripts\activate.bat
pip install --upgrade pip -q >nul 2>&1
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo [!] Erreur installation dependances
    pause
    exit /b 1
)
echo [OK] Dependances installees
echo.
echo ═══════════════════════════════════════════════════════
echo   Installation terminee - Lancement de l'application
echo ═══════════════════════════════════════════════════════
echo.

:run
:: Run the application
call venv\Scripts\activate.bat
python src\main.py
