$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendPath = Join-Path $projectRoot "frontend"
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$frontendEnvExample = Join-Path $frontendPath ".env.example"
$frontendEnvLocal = Join-Path $frontendPath ".env.local"

Set-Location $projectRoot

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    python -m venv .venv
}

Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
& $venvPython -m pip install -r requirements-dev.txt

if (-not (Test-Path $frontendEnvLocal) -and (Test-Path $frontendEnvExample)) {
    Copy-Item $frontendEnvExample $frontendEnvLocal
}

Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
Set-Location $frontendPath
npm install

Write-Host "Starting frontend in a new PowerShell window..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$frontendPath'; npm run dev"
)

Set-Location $projectRoot
Write-Host "Starting backend in this window..." -ForegroundColor Green
& $venvPython backend\app.py
