@echo off

REM =============================================================================
REM Print starting messages and info
REM =============================================================================

// Print out the application header
@echo ===========================================================================================================
@echo SAIL Table Packager v1.0
@echo by Luis Miguel Huapaya
@echo Copyright (C) 2021 Secure AI Labs Inc., All Rights Reserved.
@echo -----------------------------------------------------------------------------------------------------------
@echo Building all sailtables
@echo Working folder is: %~dp0
@echo Date and time: %date% %time%

REM =============================================================================
REM Check to make sure that all the needed files are there
REM =============================================================================

IF NOT EXIST igr_001_a.stpt (
    echo File igr_001_a.stpt is missing from the current folder
    GOTO END
)
IF NOT EXIST igr_001_b.stpt (
    echo File igr_001_b.stpt is missing from the current folder
    GOTO END
)
IF NOT EXIST igr_001_c.stpt (
    echo File igr_001_c.stpt is missing from the current folder
    GOTO END
)

IF NOT EXIST igr_002_a.stpt (
    echo File igr_002_a.stpt is missing from the current folder
    GOTO END
)
IF NOT EXIST igr_002_b.stpt (
    echo File igr_002_b.stpt is missing from the current folder
    GOTO END
)
IF NOT EXIST igr_002_c.stpt (
    echo File igr_002_c.stpt is missing from the current folder
    GOTO END
)

IF NOT EXIST mgr_001_a.stpt (
    echo File mgr_001_2.stpt is missing from the current folder
    GOTO END
)
IF NOT EXIST mgr_001_b.stpt (
    echo File mgr_001_b.stpt is missing from the current folder
    GOTO END
)
IF NOT EXIST mgr_001_c.stpt (
    echo File mgr_001_c.stpt is missing from the current folder
    GOTO END
)

IF NOT EXIST igr_001_a.csv (
    echo File igr_001_a.csv is missing from the current folder
    GOTO END
)
IF NOT EXIST igr_001_b.csv (
    echo File igr_001_b.csv is missing from the current folder
    GOTO END
)
IF NOT EXIST igr_001_c.csv (
    echo File igr_001_c.csv is missing from the current folder
    GOTO END
)

IF NOT EXIST igr_002_a.csv (
    echo File igr_002_a.csv is missing from the current folder
    GOTO END
)
IF NOT EXIST igr_002_b.csv (
    echo File igr_002_b.csv is missing from the current folder
    GOTO END
)
IF NOT EXIST igr_002_c.csv (
    echo File igr_002_c.csv is missing from the current folder
    GOTO END
)

IF NOT EXIST mgr_001_a.csv (
    echo File mgr_001_2.csv is missing from the current folder
    GOTO END
)
IF NOT EXIST mgr_001_b.csv (
    echo File mgr_001_b.csv is missing from the current folder
    GOTO END
)
IF NOT EXIST mgr_001_c.csv (
    echo File mgr_001_c.csv is missing from the current folder
    GOTO END
)

REM =============================================================================
REM Now build all the sailtable files from template
REM =============================================================================

start /W /B "" SailTablePackagerForCsv.exe --template igr_001_a.stpt --sourcecsv igr_001_a.csv --destinationfile igr_001_a.sailtable
if %ERRORLEVEL% NEQ 0 GOTO BADEND
start /W /B "" SailTablePackagerForCsv.exe --template igr_001_b.stpt --sourcecsv igr_001_b.csv --destinationfile igr_001_b.sailtable
if %ERRORLEVEL% NEQ 0 GOTO BADEND
start /W /B "" SailTablePackagerForCsv.exe --template igr_001_c.stpt --sourcecsv igr_001_c.csv --destinationfile igr_001_c.sailtable
if %ERRORLEVEL% NEQ 0 GOTO BADEND
start /W /B "" SailTablePackagerForCsv.exe --template igr_002_a.stpt --sourcecsv igr_002_a.csv --destinationfile igr_002_a.sailtable
if %ERRORLEVEL% NEQ 0 GOTO BADEND
start /W /B "" SailTablePackagerForCsv.exe --template igr_002_b.stpt --sourcecsv igr_002_b.csv --destinationfile igr_002_b.sailtable
if %ERRORLEVEL% NEQ 0 GOTO BADEND
start /W /B "" SailTablePackagerForCsv.exe --template igr_002_c.stpt --sourcecsv igr_002_c.csv --destinationfile igr_002_c.sailtable
if %ERRORLEVEL% NEQ 0 GOTO BADEND
start /W /B "" SailTablePackagerForCsv.exe --template mgr_001_a.stpt --sourcecsv mgr_001_a.csv --destinationfile mgr_001_a.sailtable
if %ERRORLEVEL% NEQ 0 GOTO BADEND
start /W /B "" SailTablePackagerForCsv.exe --template mgr_001_b.stpt --sourcecsv mgr_001_b.csv --destinationfile mgr_001_b.sailtable
if %ERRORLEVEL% NEQ 0 GOTO BADEND
start /W /B "" SailTablePackagerForCsv.exe --template mgr_001_c.stpt --sourcecsv mgr_001_c.csv --destinationfile mgr_001_c.sailtable
if %ERRORLEVEL% NEQ 0 GOTO BADEND

GOTO END

:BADEND

@echo SailTablePackaterForCsv has exited abnormally with %ERRORLEVEL%

:END
@echo on