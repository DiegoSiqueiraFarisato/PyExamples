<#
Verifies Python (3.10+), installs it with winget if missing, creates .venv,
installs requirements and starts the server.
Usage:  .\setup.ps1            # setup + run
        .\setup.ps1 -NoRun     # setup only
#>
param([switch]$NoRun)

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$MinMajor = 3; $MinMinor = 10

function Test-PythonCmd([string[]]$Cmd) {
    # Runs the candidate for real: the Microsoft Store "python.exe" alias sits on PATH but does not work.
    try {
        $exe = $Cmd[0]; $rest = @($Cmd | Select-Object -Skip 1)
        $out = & $exe @rest -c "import sys; print(str(sys.version_info[0]) + '.' + str(sys.version_info[1]))" 2>$null
        if ($LASTEXITCODE -ne 0 -or -not $out) { return $false }
        $v = [version]($out | Select-Object -First 1)
        return ($v.Major -gt $MinMajor -or ($v.Major -eq $MinMajor -and $v.Minor -ge $MinMinor))
    } catch { return $false }
}

function Find-Python {
    foreach ($c in @(@('py','-3'), @('python'), @('python3'))) {
        if ((Get-Command $c[0] -ErrorAction SilentlyContinue) -and (Test-PythonCmd $c)) { return $c }
    }
    return $null
}

$py = Find-Python
if (-not $py) {
    Write-Host "Python $MinMajor.$MinMinor+ not found. Installing with winget..."
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "winget is not available. Install Python from https://www.python.org/downloads/ and re-run."
    }
    winget install --id Python.Python.3.12 -e --silent --accept-package-agreements --accept-source-agreements
    # Refresh PATH for this session
    $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
    $py = Find-Python
    if (-not $py) { throw "Python was installed but is not visible yet. Open a new terminal and re-run setup.ps1." }
}
$pyExe = $py[0]; $pyArgs = @($py | Select-Object -Skip 1)
Write-Host ("Using Python: " + (& $pyExe @pyArgs --version))

if (-not (Test-Path .venv\Scripts\python.exe)) {
    Write-Host "Creating virtual environment..."
    & $pyExe @pyArgs -m venv .venv
}
$venvPy = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
& $venvPy -m pip install --quiet --upgrade pip
& $venvPy -m pip install --quiet -r requirements.txt
Write-Host "Dependencies installed."

if (-not $NoRun) {
    Write-Host "Starting server on http://127.0.0.1:8000  (docs: /docs)"
    & $venvPy -m app.main
}
