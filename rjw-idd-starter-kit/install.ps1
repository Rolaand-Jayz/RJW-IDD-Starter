# RJW-IDD Installation Script for Windows PowerShell
# Cross-platform, safe, beginner-friendly setup

$ErrorActionPreference = "Stop"

# Configuration
$PythonMinVersion = "3.9"
$VenvDir = ".venv"
$Requirements = "rjw-idd-starter-kit\requirements-dev.txt"

Write-Host "RJW-IDD Installation Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

function Write-Success { param($msg) Write-Host "✔ $msg" -ForegroundColor Green }
function Write-Warning { param($msg) Write-Host "⚠ $msg" -ForegroundColor Yellow }
function Write-ErrorMsg { param($msg) Write-Host "✖ $msg" -ForegroundColor Red }

# Check Python version
function Test-Python {
    Write-Host "Checking Python installation..."
    
    try {
        $pythonVersion = & python --version 2>&1
        Write-Success "Found $pythonVersion"
        
        $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
        if (-not $versionMatch) {
            Write-ErrorMsg "Could not parse Python version"
            exit 1
        }
        
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 9)) {
            Write-ErrorMsg "Python 3.9+ required, found $pythonVersion"
            exit 1
        }
    }
    catch {
        Write-ErrorMsg "Python not found. Please install Python 3.9 or higher."
        Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
}

# Create virtual environment
function New-VirtualEnv {
    if (Test-Path $VenvDir) {
        Write-Warning "Virtual environment already exists at $VenvDir"
        $response = Read-Host "Remove and recreate? [y/N]"
        if ($response -eq 'y' -or $response -eq 'Y') {
            Remove-Item -Recurse -Force $VenvDir
        }
        else {
            Write-Success "Skipping venv creation"
            return
        }
    }
    
    Write-Host "Creating virtual environment..."
    & python -m venv $VenvDir
    Write-Success "Virtual environment created at $VenvDir"
}

# Install dependencies
function Install-Dependencies {
    if (-not (Test-Path $Requirements)) {
        Write-ErrorMsg "Requirements file not found: $Requirements"
        exit 1
    }
    
    Write-Host "Installing dependencies from $Requirements..."
    
    # Activate venv
    $activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
    if (-not (Test-Path $activateScript)) {
        Write-ErrorMsg "Virtual environment activation script not found"
        exit 1
    }
    
    & $activateScript
    
    # Upgrade pip
    & python -m pip install --upgrade pip --quiet
    
    # Install requirements
    & pip install -r $Requirements --quiet
    
    Write-Success "Dependencies installed successfully"
}

# Setup CLI tool
function Set-CLITool {
    $cliPath = "rjw-idd-starter-kit\bin\rjw"
    
    if (-not (Test-Path $cliPath)) {
        Write-ErrorMsg "CLI tool not found at $cliPath"
        exit 1
    }
    
    Write-Success "CLI tool configured at $cliPath"
    Write-Warning "To use 'rjw' command, add to PATH or use full path:"
    Write-Host "    python $cliPath --help" -ForegroundColor Yellow
}

# Create requirements.txt if missing
function New-Requirements {
    if (-not (Test-Path "requirements.txt")) {
        Write-Host "Creating requirements.txt..."
        
        $reqContent = @"
# RJW-IDD Core Dependencies
pytest>=8.0
pyyaml>=6.0
"@
        Set-Content -Path "requirements.txt" -Value $reqContent
        Write-Success "Created requirements.txt"
    }
}

# Verify installation
function Test-Installation {
    Write-Host "Verifying installation..."
    
    # Activate venv
    $activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
    & $activateScript
    
    # Check Python
    $pythonVersion = & python --version
    Write-Success "Python: $pythonVersion"
    
    # Check pytest
    try {
        $pytestVersion = & pytest --version 2>&1 | Select-Object -First 1
        Write-Success "pytest: $pytestVersion"
    }
    catch {
        Write-Warning "pytest not found in environment"
    }
    
    # Check CLI
    if (Test-Path "rjw-idd-starter-kit\bin\rjw") {
        Write-Success "CLI tool: Ready"
    }
    else {
        Write-Warning "CLI tool not found"
    }
    
    Write-Success "Installation verification complete"
}

# Main installation flow
function Main {
    Write-Host "Step 1: Checking Python..." -ForegroundColor Cyan
    Test-Python
    Write-Host ""
    
    Write-Host "Step 2: Creating virtual environment..." -ForegroundColor Cyan
    New-VirtualEnv
    Write-Host ""
    
    Write-Host "Step 3: Creating project files..." -ForegroundColor Cyan
    New-Requirements
    Write-Host ""
    
    Write-Host "Step 4: Installing dependencies..." -ForegroundColor Cyan
    Install-Dependencies
    Write-Host ""
    
    Write-Host "Step 5: Configuring CLI..." -ForegroundColor Cyan
    Set-CLITool
    Write-Host ""
    
    Write-Host "Step 6: Verifying installation..." -ForegroundColor Cyan
    Test-Installation
    Write-Host ""
    
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "Installation complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Activate environment: .\.venv\Scripts\Activate.ps1"
    Write-Host "  2. Initialize project: python rjw-idd-starter-kit\bin\rjw init"
    Write-Host "  3. Read quickstart: cat rjw-idd-starter-kit\docs\quickstart.md"
    Write-Host ""
}

# Run installation
try {
    Main
}
catch {
    Write-ErrorMsg "Installation failed: $_"
    exit 1
}
