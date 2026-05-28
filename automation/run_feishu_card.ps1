param(
    [ValidateSet("morning", "evening", "sunday", "auto")]
    [string]$Mode = "auto"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\automation\feishu_supervisor.py --mode $Mode
