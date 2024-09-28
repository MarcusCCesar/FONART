@echo off
cd /d C:\Projeto_Estacio_2024-Fono\Projeto_Fonart
if %errorlevel% neq 0 (
    echo Diretório não encontrado!
    exit /b
)
pythonw firebase_setup.py      # Usa pythonw para não abrir o terminal
exit
