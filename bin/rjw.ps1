#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-Python {
    if ($env:PYTHON) { return $env:PYTHON }
    foreach ($candidate in @('python3', 'python')) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) {
            return $candidate
        }
    }
    throw 'Python interpreter not found. Set $env:PYTHON to override.'
}

function Get-ProjectRoot {
    param([string]$Start = (Get-Location).Path)
    $dir = (Resolve-Path $Start).Path
    $fallback = $null
    while ($true) {
        if (Test-Path (Join-Path $dir 'method' 'config' 'features.yml')) { return $dir }
        if (-not $fallback -and (Test-Path (Join-Path $dir '.git'))) { $fallback = $dir }
        $parent = Split-Path $dir -Parent
        if ($parent -eq $dir -or [string]::IsNullOrEmpty($parent)) { break }
        $dir = $parent
    }
    $kitRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
    if (Test-Path (Join-Path $kitRoot 'method' 'config' 'features.yml')) { return $kitRoot }
    if ($fallback) { return $fallback }
    return $kitRoot
}

function Update-Mode {
    param([string]$Lane)
    $python = Get-Python
    $projectRoot = Get-ProjectRoot
    $featuresFile = Join-Path $projectRoot 'method' 'config' 'features.yml'
    New-Item -ItemType Directory -Force -Path (Split-Path $featuresFile) | Out-Null

    $script = @"
import sys
from pathlib import Path
import yaml

lane = sys.argv[1]
features_path = Path(sys.argv[2])
if features_path.exists():
    data = yaml.safe_load(features_path.read_text()) or {}
else:
    data = {}

features = dict(data.get('features') or {})
mode = dict(data.get('mode') or {})

if lane == 'turbo':
    features['turbo_mode'] = True
    features['yolo_mode'] = False
    mode['name'] = 'turbo'
    mode['turbo'] = True
elif lane == 'yolo':
    features['yolo_mode'] = True
    features['turbo_mode'] = False
    mode['name'] = 'yolo'
    mode['turbo'] = False
elif lane == 'standard':
    features['yolo_mode'] = False
    features['turbo_mode'] = False
    mode['name'] = 'standard'
    mode['turbo'] = False
else:
    sys.stderr.write(f"Unsupported mode: {lane}\n")
    sys.exit(1)

data['features'] = features
if data.get('mode') != mode:
    data['mode'] = mode

features_path.write_text(yaml.safe_dump(data, sort_keys=False))
"@

    & $python -c $script $Lane $featuresFile
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "✓ Updated $featuresFile"
    Write-Host '→ Enforcing configuration drift checks'
    Push-Location $projectRoot
    & $python (Join-Path (Resolve-Path (Join-Path $PSScriptRoot '..')).Path 'scripts' 'config_enforce.py')
    $exitCode = $LASTEXITCODE
    Pop-Location
    if ($exitCode -ne 0) { exit $exitCode }
}

function Show-Plan {
    $projectRoot = Get-ProjectRoot
    $queueFile = Join-Path $projectRoot 'docs' 'status' 'next-steps.md'
    if (-not (Test-Path $queueFile)) {
        $template = @"
# Next-Steps Queue

## Do Now (≤3)
-
-
-

## Do Next (≤5)
-
-
-
-
-

## Backlog
-
"@
        $template | Set-Content -Path $queueFile -Encoding utf8
        Write-Warning "Created template at $queueFile"
    }
    Get-Content -Path $queueFile
}

function Show-Usage {
    @'
Usage: rjw <command>

Built-ins:
  rjw mode <turbo|yolo|standard>   Toggle the learning lane in method/config/features.yml
  rjw plan                         Print docs/status/next-steps.md (creates a stub if missing)

Other commands are delegated to the Python CLI (guard, init, prompts, ...).
'@
}

if ($args.Count -eq 0) {
    Show-Usage
    exit 0
}

switch ($args[0].ToLowerInvariant()) {
    'mode' {
        if ($args.Count -lt 2) { Write-Error 'Missing mode name (turbo, yolo, standard).'; exit 1 }
        Update-Mode -Lane $args[1].ToLowerInvariant()
    }
    'plan' {
        Show-Plan
    }
    'help' { Show-Usage }
    '--help' { Show-Usage }
    '-h' { Show-Usage }
    Default {
        $python = Get-Python
        & $python (Join-Path $PSScriptRoot 'rjw.py') @args
        exit $LASTEXITCODE
    }
}
