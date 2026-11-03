@REM  @echo off
@REM  set "PYTHONPATH=%PYTHONPATH%;%CD%\src"
@REM  echo PYTHONPATH=%PYTHONPATH%

@echo off
set "SRC_PATH=%CD%\src"

echo %PYTHONPATH% | findstr /L /I /C:"%SRC_PATH%" >nul

if errorlevel 1 (
    set "PYTHONPATH=%PYTHONPATH%;%SRC_PATH%"
    echo Added to PYTHONPATH: %SRC_PATH%
) else (
    echo Already in PYTHONPATH: %SRC_PATH%
)

echo.
echo PYTHONPATH=%PYTHONPATH%

python -m quizzer.main