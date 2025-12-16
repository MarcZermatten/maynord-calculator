@echo off
chcp 65001 >nul
echo ========================================
echo   Maynord Calculator - Build EXE
echo ========================================
echo.

:: Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo [!] Environnement virtuel non trouvé.
    echo     Lancez d'abord INSTALL.bat
    pause
    exit /b 1
)

echo [1/2] Compilation en cours...
echo       Cela peut prendre quelques minutes...
echo.

pyinstaller --onefile --windowed --name="MaynordCalculator" ^
    --add-data "src/resources;resources" ^
    --hidden-import=PySide6.QtCore ^
    --hidden-import=PySide6.QtGui ^
    --hidden-import=PySide6.QtWidgets ^
    --hidden-import=matplotlib.backends.backend_qt5agg ^
    src/main.py

if %errorlevel% neq 0 (
    echo.
    echo [!] Erreur lors de la compilation
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Build terminé avec succès!
echo ========================================
echo.
echo L'exécutable se trouve dans:
echo   dist\MaynordCalculator.exe
echo.

:: Open dist folder
start dist

pause
