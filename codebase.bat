@echo off
setlocal EnableDelayedExpansion

REM ========================================
REM CONTACT360 ADMIN (DJANGO) - CODEBASE STATE CHECK
REM ========================================
REM Run from admin folder: double-click or run codebase.bat from this directory.
REM
REM Pipeline (mirrors contact360.io\app\codebase.bat structure, Django tooling):
REM   0 Optional static/CSS inventory
REM   1 pip install (dependencies)
REM   2 Migration graph check (makemigrations --check --dry-run)
REM   3 Syntax / bytecode compile (compileall on apps, config, docsai)
REM   4 Format check (optional; project has no black/ruff in requirements yet)
REM   5 Django system check
REM   6 Pytest (apps/core/tests per CI)
REM   6b Coverage if RUN_TEST_COVERAGE=1 and pytest-cov available
REM   7 Deploy-oriented check (manage.py check --deploy) or skip
REM   8 Final format (optional npm-style parity; usually skip)
REM   9 Static collection / build parity (collectstatic --noinput in production env)
REM
REM Optional environment variables:
REM SKIP_STATIC_INVENTORY=1   Skip step 0
REM SKIP_PIP_INSTALL=1        Skip step 1 pip install
REM SKIP_MIGRATION_CHECK=1    Skip step 2
REM SKIP_COMPILEALL=1         Skip step 3
REM SKIP_FORMAT=1             Skip step 4 (default behavior when no format tool)
REM SKIP_DEPLOY_CHECK=1       Skip step 7 (or use DEPLOY_CHECK_NO_FAIL=1)
REM DEPLOY_CHECK_NO_FAIL=1    check --deploy failures count as warning only
REM RUN_TEST_COVERAGE=1       Run pytest with --cov if pytest-cov installed
REM SKIP_COLLECTSTATIC=1      Skip step 9
REM SKIP_PRETTIER=1           Skip step 4b Prettier (templates/static/JSON/CSS)
REM
REM For step 7/9 deploy-style checks, these match .github/workflows/django-ci.yml:
REM   DJANGO_ENV=production
REM   SECRET_KEY=... (at least 32 chars)
REM   ALLOWED_HOSTS=localhost,127.0.0.1
REM ========================================

set "ADMIN_DIR=%~dp0"
set "ERROR_COUNT=0"
set "WARNING_COUNT=0"
set "START_TIME=%TIME%"
set "SECTION6_COVERAGE_STATUS=SKIPPED"

REM Enable ANSI color support - Windows 10 or newer
for /f %%A in ('echo prompt $E ^| cmd') do set "ESC=%%A"

set "GREEN=%ESC%[92m"
set "RED=%ESC%[91m"
set "YELLOW=%ESC%[93m"
set "BLUE=%ESC%[94m"
set "CYAN=%ESC%[96m"
set "RESET=%ESC%[0m"

goto :main

:color_echo
setlocal EnableDelayedExpansion
set "color_code=%~1"
set "text=%~2"
echo !color_code!!text!
endlocal
goto :eof

:main
echo.
call :color_echo "%CYAN%" "========================================"
call :color_echo "%CYAN%" "  CONTACT360 ADMIN (DJANGO) STATE CHECK"
call :color_echo "%CYAN%" "========================================"
echo.

if not exist "%ADMIN_DIR%manage.py" (
    call :color_echo "%RED%" "ERROR: manage.py not found under: %ADMIN_DIR%"
    exit /b 1
)

cd /d "%ADMIN_DIR%"
call :color_echo "%BLUE%" "Current directory: %CD%"
set "PY=python"
if exist "venv\Scripts\python.exe" (
  set "PY=%CD%\venv\Scripts\python.exe"
  call :color_echo "%BLUE%" "Using venv Python: %PY%"
) else (
  call :color_echo "%YELLOW%" "No venv\\Scripts\\python.exe  -  using PATH python (create venv for isolated deps)"
)
echo.

set "SECTION1_STATUS=SKIPPED"
set "SECTION2_STATUS=SKIPPED"
set "SECTION3_STATUS=SKIPPED"
set "SECTION4_STATUS=SKIPPED"
set "SECTION5_STATUS=SKIPPED"
set "SECTION6_STATUS=SKIPPED"
set "SECTION7_STATUS=SKIPPED"
set "SECTION8_STATUS=SKIPPED"
set "SECTION9_STATUS=SKIPPED"
set "SECTION0_STATUS=SKIPPED"
set "SECTION4P_STATUS=SKIPPED"

if /i "%SKIP_STATIC_INVENTORY%"=="1" (
  call :color_echo "%YELLOW%" "[0] Static inventory skipped (SKIP_STATIC_INVENTORY=1)"
  set "SECTION0_STATUS=SKIPPED"
  echo.
) else (
  call :color_echo "%CYAN%" "[0] Static / CSS inventory..."
  echo ----------------------------------------
  call :color_echo "%BLUE%" "  Lists *.css under static\ (admin dashboard assets)."
  if not exist "reports" mkdir reports
  call :color_echo "%BLUE%" "  Output: reports\admin-static-inventory.txt"
  (
    echo CONTACT360 Admin static CSS inventory
    echo Generated: %DATE% %TIME%
    echo.
    dir /s /b static\*.css 2>nul
    if errorlevel 1 echo No CSS files found under static\
  ) > "reports\admin-static-inventory.txt" 2>&1
  call :color_echo "%GREEN%" "  OK Inventory written to reports\admin-static-inventory.txt"
  set "SECTION0_STATUS=PASSED"
  echo.
)

call :color_echo "%CYAN%" "[1/10] Dependencies (pip)..."
echo ----------------------------------------
if /i "%SKIP_PIP_INSTALL%"=="1" (
  call :color_echo "%YELLOW%" "  Skipped (SKIP_PIP_INSTALL=1)"
  set "SECTION1_STATUS=SKIPPED"
) else (
  call :color_echo "%YELLOW%" "  Running: %PY% -m pip install --upgrade pip"
  call "%PY%" -m pip install --upgrade pip
  if errorlevel 1 (
    set /a WARNING_COUNT+=1
    call :color_echo "%YELLOW%" "  ! pip self-upgrade failed (continuing)"
  )
  call :color_echo "%YELLOW%" "  Running: %PY% -m pip install -r requirements.txt"
  call "%PY%" -m pip install -r requirements.txt
  if errorlevel 1 (
    set /a ERROR_COUNT+=1
    set "SECTION1_STATUS=FAILED"
    call :color_echo "%RED%" "  X pip install failed"
    goto :summary
  ) else (
    set "SECTION1_STATUS=PASSED"
    call :color_echo "%GREEN%" "  OK Dependencies installed"
  )
)
echo.

call :color_echo "%CYAN%" "[2/10] Migration consistency check..."
echo ----------------------------------------
if /i "%SKIP_MIGRATION_CHECK%"=="1" (
  call :color_echo "%YELLOW%" "  Skipped (SKIP_MIGRATION_CHECK=1)"
  set "SECTION2_STATUS=SKIPPED"
) else (
  call :color_echo "%BLUE%" "  Running: %PY% manage.py makemigrations --check --dry-run"
  call "%PY%" manage.py makemigrations --check --dry-run
  if errorlevel 1 (
    set /a ERROR_COUNT+=1
    set "SECTION2_STATUS=FAILED"
    call :color_echo "%RED%" "  X Pending model changes  -  run makemigrations"
  ) else (
    set "SECTION2_STATUS=PASSED"
    call :color_echo "%GREEN%" "  OK No missing migrations"
  )
)
echo.

call :color_echo "%CYAN%" "[3/10] Python syntax (compileall)..."
echo ----------------------------------------
if /i "%SKIP_COMPILEALL%"=="1" (
  call :color_echo "%YELLOW%" "  Skipped (SKIP_COMPILEALL=1)"
  set "SECTION3_STATUS=SKIPPED"
) else (
  call :color_echo "%YELLOW%" "  Running: %PY% -m compileall -q apps config docsai"
  call "%PY%" -m compileall -q apps config docsai
  if errorlevel 1 (
    set /a ERROR_COUNT+=1
    set "SECTION3_STATUS=FAILED"
    call :color_echo "%RED%" "  X Syntax / compile errors"
  ) else (
    set "SECTION3_STATUS=PASSED"
    call :color_echo "%GREEN%" "  OK compileall passed"
  )
)
echo.

call :color_echo "%CYAN%" "[4/10] Formatting checks..."
echo ----------------------------------------
if /i "%SKIP_FORMAT%"=="1" (
  call :color_echo "%YELLOW%" "  Skipped (SKIP_FORMAT=1). Add ruff/black to requirements to enable."
  set "SECTION4_STATUS=SKIPPED"
) else (
  call "%PY%" -m ruff --version >nul 2>&1
  if errorlevel 1 (
    set /a WARNING_COUNT+=1
    set "SECTION4_STATUS=WARNING"
    call :color_echo "%YELLOW%" "  ! ruff not installed  -  pip install ruff or set SKIP_FORMAT=1"
  ) else (
    call :color_echo "%YELLOW%" "  Running: %PY% -m ruff format --check ."
    call "%PY%" -m ruff format --check .
    if errorlevel 1 (
      set /a WARNING_COUNT+=1
      set "SECTION4_STATUS=WARNING"
      call :color_echo "%YELLOW%" "  ! Format check failed  -  run: ruff format ."
    ) else (
      set "SECTION4_STATUS=PASSED"
      call :color_echo "%GREEN%" "  OK Format check passed"
    )
  )
)
echo.

call :color_echo "%CYAN%" "[4b/10] Prettier (templates, static, JSON, CSS)..."
echo ----------------------------------------
if /i "%SKIP_PRETTIER%"=="1" (
  call :color_echo "%YELLOW%" "  Skipped (SKIP_PRETTIER=1)"
  set "SECTION4P_STATUS=SKIPPED"
) else (
  where npx >nul 2>&1
  if errorlevel 1 (
    set /a WARNING_COUNT+=1
    set "SECTION4P_STATUS=WARNING"
    call :color_echo "%YELLOW%" "  ! npx not on PATH  -  install Node.js or set SKIP_PRETTIER=1"
  ) else (
    call :color_echo "%BLUE%" "  Prettier for HTML/CSS/JSON (not Python  -  ruff handles .py in step 4)"
    call :color_echo "%YELLOW%" "  Running: npx prettier --check ."
    call npx prettier --check .
    if errorlevel 1 (
      set /a WARNING_COUNT+=1
      set "SECTION4P_STATUS=WARNING"
      call :color_echo "%YELLOW%" "  Prettier issues  -  running: npx prettier --write ."
      call npx prettier --write .
      if errorlevel 1 (
        set /a WARNING_COUNT+=1
        set "SECTION4P_STATUS=WARNING"
        call :color_echo "%YELLOW%" "  ! Prettier --write had issues"
      ) else (
        call npx prettier --check .
        if errorlevel 1 (
          set /a WARNING_COUNT+=1
          set "SECTION4P_STATUS=WARNING"
        ) else (
          set "SECTION4P_STATUS=WARNING_FIXED"
          call :color_echo "%GREEN%" "  OK Prettier formatted (templates/static/config)"
        )
      )
    ) else (
      set "SECTION4P_STATUS=PASSED"
      call :color_echo "%GREEN%" "  OK Prettier check passed"
    )
  )
)
echo.

call :color_echo "%CYAN%" "[5/10] Django system check..."
echo ----------------------------------------
call :color_echo "%YELLOW%" "  Running: %PY% manage.py check"
call "%PY%" manage.py check
if errorlevel 1 (
  set /a ERROR_COUNT+=1
  set "SECTION5_STATUS=FAILED"
  call :color_echo "%RED%" "  X manage.py check failed"
) else (
  set "SECTION5_STATUS=PASSED"
  call :color_echo "%GREEN%" "  OK System check passed"
)
echo.

call :color_echo "%CYAN%" "[6/10] Running tests (pytest)..."
echo ----------------------------------------
set "PREV_DJANGO_ENV=%DJANGO_ENV%"
set DJANGO_ENV=testing
call :color_echo "%YELLOW%" "  DJANGO_ENV=testing (restored after tests)"
call :color_echo "%YELLOW%" "  Running: %PY% -m pytest apps/core/tests/ -q"
call "%PY%" -m pytest apps/core/tests/ -q
if errorlevel 1 (
  set /a ERROR_COUNT+=1
  set "SECTION6_STATUS=FAILED"
  call :color_echo "%RED%" "  X Tests failed"
) else (
  set "SECTION6_STATUS=PASSED"
  call :color_echo "%GREEN%" "  OK Tests passed"
)
if defined PREV_DJANGO_ENV (set "DJANGO_ENV=%PREV_DJANGO_ENV%") else (set "DJANGO_ENV=")
echo.

if /i "%RUN_TEST_COVERAGE%"=="1" (
  call :color_echo "%CYAN%" "[6b] Pytest coverage (RUN_TEST_COVERAGE=1)..."
  echo ----------------------------------------
  set DJANGO_ENV=testing
  call :color_echo "%YELLOW%" "  Running: %PY% -m pytest apps/core/tests/ --cov --cov-report=term-missing"
  call "%PY%" -m pytest apps/core/tests/ --cov --cov-report=term-missing
  if errorlevel 1 (
    set /a WARNING_COUNT+=1
    set "SECTION6_COVERAGE_STATUS=WARNING"
    call :color_echo "%YELLOW%" "  Warning: Coverage run failed or pytest-cov missing  -  pip install pytest-cov"
  ) else (
    set "SECTION6_COVERAGE_STATUS=PASSED"
    call :color_echo "%GREEN%" "  OK Coverage run completed"
  )
  if defined PREV_DJANGO_ENV (set "DJANGO_ENV=%PREV_DJANGO_ENV%") else (set "DJANGO_ENV=")
  echo.
) else (
  call :color_echo "%BLUE%" "[6b] Coverage skipped (set RUN_TEST_COVERAGE=1; requires pytest-cov)"
  echo.
)

if /i "%SKIP_DEPLOY_CHECK%"=="1" (
  call :color_echo "%YELLOW%" "[7/10] Deploy check skipped (SKIP_DEPLOY_CHECK=1)"
  set "SECTION7_STATUS=SKIPPED"
  echo.
) else (
  call :color_echo "%CYAN%" "[7/10] Django deploy check (production settings)..."
  echo ----------------------------------------
  call :color_echo "%BLUE%" "  Matches CI: DJANGO_ENV=production, SECRET_KEY, ALLOWED_HOSTS"
  set "SAVE_DJANGO_ENV=%DJANGO_ENV%"
  set DJANGO_ENV=production
  if not defined SECRET_KEY set "SECRET_KEY=ci-check-deploy-placeholder-not-for-production-0123456789-abcdefghij-unique-chars"
  if not defined ALLOWED_HOSTS set "ALLOWED_HOSTS=localhost,127.0.0.1"
  call :color_echo "%YELLOW%" "  Running: %PY% manage.py check --deploy"
  call "%PY%" manage.py check --deploy
  if errorlevel 1 (
    if /i "%DEPLOY_CHECK_NO_FAIL%"=="1" (
      set /a WARNING_COUNT+=1
      set "SECTION7_STATUS=WARNING"
      call :color_echo "%YELLOW%" "  ! Deploy check issues (DEPLOY_CHECK_NO_FAIL=1)"
    ) else (
      set /a ERROR_COUNT+=1
      set "SECTION7_STATUS=FAILED"
      call :color_echo "%RED%" "  X check --deploy failed"
    )
  ) else (
    set "SECTION7_STATUS=PASSED"
    call :color_echo "%GREEN%" "  OK Deploy check passed"
  )
  if defined SAVE_DJANGO_ENV (set "DJANGO_ENV=%SAVE_DJANGO_ENV%") else (set "DJANGO_ENV=")
  echo.
)

call :color_echo "%CYAN%" "[8/10] Final format (parity with app pipeline)..."
echo ----------------------------------------
call :color_echo "%YELLOW%" "  Skipped for Django admin (no npm). Use ruff format . manually if ruff installed."
set "SECTION8_STATUS=SKIPPED"
echo.

call :color_echo "%CYAN%" "[9/10] Collect static (production build parity)..."
echo ----------------------------------------
if /i "%SKIP_COLLECTSTATIC%"=="1" (
  call :color_echo "%YELLOW%" "  Skipped (SKIP_COLLECTSTATIC=1)"
  set "SECTION9_STATUS=SKIPPED"
) else (
  set "SAVE_DJANGO_ENV2=%DJANGO_ENV%"
  set DJANGO_ENV=production
  if not defined SECRET_KEY set "SECRET_KEY=ci-check-deploy-placeholder-not-for-production-0123456789-abcdefghij-unique-chars"
  if not defined ALLOWED_HOSTS set "ALLOWED_HOSTS=localhost,127.0.0.1"
  call :color_echo "%YELLOW%" "  Running: %PY% manage.py collectstatic --noinput"
  call "%PY%" manage.py collectstatic --noinput
  if errorlevel 1 (
    set /a ERROR_COUNT+=1
    set "SECTION9_STATUS=FAILED"
    call :color_echo "%RED%" "  X collectstatic failed"
  ) else (
    if exist "staticfiles" (
      set "SECTION9_STATUS=PASSED"
      call :color_echo "%GREEN%" "  OK staticfiles collected"
    ) else (
      set /a WARNING_COUNT+=1
      set "SECTION9_STATUS=WARNING"
      call :color_echo "%YELLOW%" "  ! staticfiles dir not found (check STATIC_ROOT)"
    )
  )
  if defined SAVE_DJANGO_ENV2 (set "DJANGO_ENV=%SAVE_DJANGO_ENV2%") else (set "DJANGO_ENV=")
)
echo.

:summary
echo.
call :color_echo "%CYAN%" "========================================"
call :color_echo "%CYAN%" "  SUMMARY"
call :color_echo "%CYAN%" "========================================"
echo.
set "END_TIME=%TIME%"
call :color_echo "%BLUE%" "Section Status:"
echo   [0] Static/CSS inventory:           !SECTION0_STATUS!
echo   [1] Pip dependencies:               !SECTION1_STATUS!
echo   [2] Migrations check:               !SECTION2_STATUS!
echo   [3] compileall (syntax):            !SECTION3_STATUS!
echo   [4] Format check (ruff):           !SECTION4_STATUS!
echo   [4b] Prettier (web assets):         !SECTION4P_STATUS!
echo   [5] Django check:                  !SECTION5_STATUS!
echo   [6] Pytest:                        !SECTION6_STATUS!
echo   [6b] Pytest coverage:              !SECTION6_COVERAGE_STATUS!
echo   [7] check --deploy:                !SECTION7_STATUS!
echo   [8] Final format:                  !SECTION8_STATUS!
echo   [9] collectstatic:                 !SECTION9_STATUS!
echo.

if %ERROR_COUNT% EQU 0 (
    call :color_echo "%GREEN%" "  OK All blocking checks passed!"
    if %WARNING_COUNT% GTR 0 call :color_echo "%YELLOW%" "  Found %WARNING_COUNT% warning(s)"
    echo.
    call :color_echo "%CYAN%" "  Start development server? (Y/N)"
    choice /C YN /N /M ""
    if errorlevel 2 goto :end
    if errorlevel 1 goto :dev_server
) else (
    call :color_echo "%RED%" "  X Found %ERROR_COUNT% error(s)"
    if %WARNING_COUNT% GTR 0 call :color_echo "%YELLOW%" "  Found %WARNING_COUNT% warning(s)"
    echo.
    call :color_echo "%YELLOW%" "  Please fix the errors before proceeding."
)
goto :end

:dev_server
echo.
call :color_echo "%CYAN%" "[10/10] Starting Django development server..."
call :color_echo "%BLUE%" "  Press Ctrl+C to stop the server"
echo.
call python manage.py runserver

:end
echo.
call :color_echo "%CYAN%" "========================================"
call :color_echo "%CYAN%" "  CHECK COMPLETE"
call :color_echo "%CYAN%" "========================================"
echo.
if %ERROR_COUNT% GTR 0 (exit /b 1) else (exit /b 0)
