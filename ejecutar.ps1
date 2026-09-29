param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Archivo
)
& (Join-Path $PSScriptRoot '.venv\Scripts\python.exe') (Join-Path $PSScriptRoot 'ejecutar.py') $Archivo
exit $LASTEXITCODE
