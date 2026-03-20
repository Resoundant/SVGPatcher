@echo off
SETLOCAL

:: Defining variables
SET "VENV=.venv_build"
SET "PY=%VENV%\Scripts\python.exe"

:: Removing existing build venv
IF EXIST "%VENV%" (
    echo Removing existing build venv
    rmdir /s /q "%VENV%"
)

:: Creating build venv
echo Creating build venv
python -m venv "%VENV%"
echo Upgrading pip
"%PY%" -m pip install --no-cache-dir --upgrade pip
echo Installing build requirements
"%PY%" -m pip install --no-cache-dir -r .\build\requirements.txt

:: Running build steps
echo Generating build info
"%PY%" .\build\generate_build_info.py
echo Building package
"%PY%" -m build
echo SVGPatcher build done!
ENDLOCAL