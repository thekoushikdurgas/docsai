@echo off
REM Save as UTF-8 without BOM. A leading BOM makes CMD fail on the first line (mojibake before @echo).
setlocal EnableDelayedExpansion

REM ========================================
REM CONTACT360 ADMIN - CODEBASE STATE CHECK
REM ========================================
REM Run from admin folder: double-click or: codebase.bat
REM Dev server listens on port 3001 (see package.json).
REM
REM Pipeline (lean vs dashboard app codebase.bat):
REM   optional [0] API health smoke, [1] clean+install, [2] codegen, [3] typecheck,
REM   [4] lint, [5] build, then optional dev on :3001.
REM
REM npm run ci is: lint, typecheck, build (no clean, install, or codegen).
REM For CI parity only: SKIP_CLEAN=1 SKIP_INSTALL=1 SKIP_CODEGEN=1 then npm run ci.
REM
REM Optional environment variables:
REM RUN_HEALTH_SMOKE=1      Run scripts\health-smoke.mjs before other steps
REM API_HEALTH_URL=...      Override health URL (default from NEXT_PUBLIC_API_URL or api.contact360.io)
REM SKIP_CLEAN=1            Skip npm run clean
REM SKIP_INSTALL=1          Skip npm install (use when node_modules already fresh)
REM SKIP_CODEGEN=1          Skip GraphQL codegen
REM SKIP_BUILD=1            Skip production build (typecheck+lint only)
REM
REM Codegen needs reachable schema; on failure retries codegen:local (http://127.0.0.1:8001/graphql).
REM Start contact360.io/api on :8001 before a full local audit if you need fresh types.
REM ========================================

set "ADMIN_DIR=%~dp0"
set "ERROR_COUNT=0"
set "WARNING_COUNT=0"
set "START_TIME=%TIME%"
set "TOTAL_SECTIONS=6"

set "ESC="
for /f "delims=" %%A in ('powershell -NoProfile -Command "Write-Output ([char]27)" 2^>nul') do set "ESC=%%A"
set "GREEN=%ESC%[92m"
set "RED=%ESC%[91m"
set "YELLOW=%ESC%[93m"
set "BLUE=%ESC%[94m"
set "CYAN=%ESC%[96m"

goto :main

:color_echo
setlocal EnableDelayedExpansion
set "_ce_c=%~1"
set "_ce_t=x%~2"
set "_ce_t=!_ce_t:~1!"
echo !_ce_c!!_ce_t!
endlocal
goto :eof

:main
echo.
call :color_echo "%CYAN%" "========================================"
call :color_echo "%CYAN%" "  CONTACT360 ADMIN STATE CHECK"
call :color_echo "%CYAN%" "========================================"
echo.

if not exist "%ADMIN_DIR%" (
    call :color_echo "%RED%" "ERROR: Admin directory not found: %ADMIN_DIR%"
    exit /b 1
)

cd /d "%ADMIN_DIR%"
call :color_echo "%BLUE%" "Current directory: %CD%"
call :color_echo "%BLUE%" "Dev port: 3001  |  PM2 name: contact360-admin"
echo.

set "SECTION0_STATUS=SKIPPED"
set "SECTION1_STATUS=SKIPPED"
set "SECTION2_STATUS=SKIPPED"
set "SECTION3_STATUS=SKIPPED"
set "SECTION4_STATUS=SKIPPED"
set "SECTION5_STATUS=SKIPPED"

if /i "%RUN_HEALTH_SMOKE%"=="1" (
  call :color_echo "%CYAN%" "[0] API health smoke (RUN_HEALTH_SMOKE=1)..."
  echo ----------------------------------------
  if exist "scripts\health-smoke.mjs" (
    call npm run health:smoke
    if errorlevel 1 (
      set /a WARNING_COUNT+=1
      set "SECTION0_STATUS=WARNING"
      call :color_echo "%YELLOW%" "  ! Health smoke failed  -  API may be down; continuing"
    ) else (
      set "SECTION0_STATUS=PASSED"
      call :color_echo "%GREEN%" "  OK API health check passed"
    )
  ) else (
    set /a WARNING_COUNT+=1
    set "SECTION0_STATUS=WARNING"
    call :color_echo "%YELLOW%" "  ! scripts\health-smoke.mjs not found"
  )
  echo.
) else (
  call :color_echo "%BLUE%" "[0] Health smoke skipped (set RUN_HEALTH_SMOKE=1 to run npm run health:smoke)"
  echo.
)

call :color_echo "%CYAN%" "[1/6] Cleaning and preparing..."
echo ----------------------------------------
if /i "%SKIP_CLEAN%"=="1" (
  call :color_echo "%YELLOW%" "  Clean skipped (SKIP_CLEAN=1)"
) else (
  call :color_echo "%YELLOW%" "  Running: npm run clean:all"
  call npm run clean:all
  if errorlevel 1 (
    set /a ERROR_COUNT+=1
    set "SECTION1_STATUS=FAILED"
    call :color_echo "%RED%" "  X Clean failed"
  ) else (
    call :color_echo "%GREEN%" "  OK Clean completed"
  )
)
echo.
if /i "%SKIP_INSTALL%"=="1" (
  call :color_echo "%YELLOW%" "  Install skipped (SKIP_INSTALL=1)"
  if not "!SECTION1_STATUS!"=="FAILED" set "SECTION1_STATUS=PASSED"
) else (
  call :color_echo "%YELLOW%" "  Running: npm install --legacy-peer-deps"
  call npm install --legacy-peer-deps
  if errorlevel 1 (
    set /a ERROR_COUNT+=1
    set "SECTION1_STATUS=FAILED"
    call :color_echo "%RED%" "  X npm install failed"
    goto :summary
  ) else (
    set "SECTION1_STATUS=PASSED"
    call :color_echo "%GREEN%" "  OK Dependencies installed"
  )
)
echo.

if /i "%SKIP_CODEGEN%"=="1" (
  call :color_echo "%YELLOW%" "[2/6] GraphQL codegen skipped (SKIP_CODEGEN=1)"
  set "SECTION2_STATUS=SKIPPED"
  echo.
) else (
  call :color_echo "%CYAN%" "[2/6] GraphQL Codegen..."
  echo ----------------------------------------
  call :color_echo "%BLUE%" "  Regenerates src/graphql/generated/types.ts from the API schema."
  call :color_echo "%BLUE%" "  Local API default: http://127.0.0.1:8001/graphql (see codegen.local.ts)."
  call :color_echo "%YELLOW%" "  Running: npm run codegen"
  call npm run codegen
  if errorlevel 1 (
    call :color_echo "%YELLOW%" "  Retrying: npm run codegen:local (http://127.0.0.1:8001/graphql)..."
    call npm run codegen:local
  )
  if errorlevel 1 (
    set /a WARNING_COUNT+=1
    set "SECTION2_STATUS=WARNING"
    call :color_echo "%YELLOW%" "  ! Codegen failed  -  API may be down; continuing with existing types if any"
    call :color_echo "%YELLOW%" "  Tip: start API on :8001 or set CODEGEN_SCHEMA_URL in .env.local"
  ) else (
    set "SECTION2_STATUS=PASSED"
    call :color_echo "%GREEN%" "  OK GraphQL types regenerated"
  )
  echo.
)

call :color_echo "%CYAN%" "[3/6] Type checking..."
echo ----------------------------------------
call :color_echo "%YELLOW%" "  Running: npm run typecheck"
call npm run typecheck
if errorlevel 1 (
    set /a ERROR_COUNT+=1
    set "SECTION3_STATUS=FAILED"
    call :color_echo "%RED%" "  X Type check failed"
) else (
    set "SECTION3_STATUS=PASSED"
    call :color_echo "%GREEN%" "  OK Type check passed"
)
echo.

call :color_echo "%CYAN%" "[4/6] Linting..."
echo ----------------------------------------
call :color_echo "%YELLOW%" "  Running: npm run lint"
call npm run lint
if errorlevel 1 (
    set /a ERROR_COUNT+=1
    set "SECTION4_STATUS=FAILED"
    call :color_echo "%RED%" "  X Linting errors found"
    call npm run lint:fix
    if not errorlevel 1 (
        call npm run lint
        if not errorlevel 1 (
            set /a ERROR_COUNT-=1
            set "SECTION4_STATUS=WARNING_FIXED"
            call :color_echo "%GREEN%" "  OK Linting issues resolved"
        )
    )
) else (
    set "SECTION4_STATUS=PASSED"
    call :color_echo "%GREEN%" "  OK No linting errors"
)
echo.

if /i "%SKIP_BUILD%"=="1" (
  call :color_echo "%YELLOW%" "[5/6] Build skipped (SKIP_BUILD=1)"
  set "SECTION5_STATUS=SKIPPED"
  echo.
) else (
  call :color_echo "%CYAN%" "[5/6] Production build check..."
  echo ----------------------------------------
  call :color_echo "%YELLOW%" "  Running: npm run build"
  call npm run build
  if errorlevel 1 (
    set /a ERROR_COUNT+=1
    set "SECTION5_STATUS=FAILED"
    call :color_echo "%RED%" "  X Build failed"
  ) else (
    if exist ".next" (
        set "SECTION5_STATUS=PASSED"
        call :color_echo "%GREEN%" "  OK Build successful"
    ) else (
        set /a ERROR_COUNT+=1
        set "SECTION5_STATUS=FAILED"
        call :color_echo "%RED%" "  X .next directory not found"
    )
  )
  echo.
)

:summary
echo.
call :color_echo "%CYAN%" "========================================"
call :color_echo "%CYAN%" "  SUMMARY"
call :color_echo "%CYAN%" "========================================"
echo.
set "END_TIME=%TIME%"
call :color_echo "%BLUE%" "Section Status:"
echo   [0] API health smoke:             !SECTION0_STATUS!
echo   [1] Cleanup and Preparation:      !SECTION1_STATUS!
echo   [2] GraphQL Codegen:                !SECTION2_STATUS!
echo   [3] Type Checking:                  !SECTION3_STATUS!
echo   [4] Linting:                        !SECTION4_STATUS!
echo   [5] Build Verification:             !SECTION5_STATUS!
echo.
call :color_echo "%BLUE%" "CI parity: npm run ci  (lint + typecheck + build, no install/codegen)"
echo.

if %ERROR_COUNT% EQU 0 (
    call :color_echo "%GREEN%" "  OK All checks passed!"
    if %WARNING_COUNT% GTR 0 call :color_echo "%YELLOW%" "  Found %WARNING_COUNT% warning(s)"
    echo.
    call :color_echo "%CYAN%" "  Start development server on :3001? (Y/N)"
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
call :color_echo "%CYAN%" "[6/6] Starting development server (port 3001)..."
call :color_echo "%BLUE%" "  Press Ctrl+C to stop the server"
call :color_echo "%BLUE%" "  Ensure API ALLOWED_ORIGINS includes http://localhost:3001"
echo.
call npm run dev

:end
echo.
call :color_echo "%CYAN%" "========================================"
call :color_echo "%CYAN%" "  CHECK COMPLETE"
call :color_echo "%CYAN%" "========================================"
echo.
if %ERROR_COUNT% GTR 0 (exit /b 1) else (exit /b 0)
