@echo off

rem This script runs the island-counter application inside a Docker container on Windows.
rem It takes a single argument: the path to the input file.

if "%~1"=="" (
    echo Error: No input file specified. >&2
    echo Usage: run.bat <path_to_the_file> >&2
    docker run --rm island-counter:latest
    exit /b 1
)

set "INPUT_FILE_PATH=%~f1"
set "INPUT_FILE_DIR=%~dp1"

if not exist "%INPUT_FILE_PATH%" (
    echo Error: File not found at '%INPUT_FILE_PATH%' >&2
    exit /b 1
)

docker run --rm -v "%INPUT_FILE_DIR%:/data" island-counter:latest "/data/%~nx1"