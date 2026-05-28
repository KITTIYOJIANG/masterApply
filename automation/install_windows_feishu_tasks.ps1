param(
    [string]$TaskPrefix = "RoboticsSupervisor"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Script = Join-Path $Root "automation\run_feishu_card.ps1"

Write-Host "Installing local Windows scheduled tasks for Feishu supervision..."
Write-Host "Root: $Root"

$MorningAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Script`" -Mode morning"
$EveningAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Script`" -Mode evening"
$SundayAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Script`" -Mode sunday"

$MorningTrigger = New-ScheduledTaskTrigger -Daily -At 08:00
$EveningTrigger = New-ScheduledTaskTrigger -Daily -At 22:00
$SundayTrigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 21:00

Register-ScheduledTask -TaskName "$TaskPrefix-Morning" -Action $MorningAction -Trigger $MorningTrigger -Description "Send morning robotics execution card to Feishu." -Force | Out-Null
Register-ScheduledTask -TaskName "$TaskPrefix-Evening" -Action $EveningAction -Trigger $EveningTrigger -Description "Send evening robotics accountability card to Feishu." -Force | Out-Null
Register-ScheduledTask -TaskName "$TaskPrefix-Sunday" -Action $SundayAction -Trigger $SundayTrigger -Description "Send Sunday robotics review card to Feishu." -Force | Out-Null

Write-Host "Done. Make sure FEISHU_WEBHOOK_URL is available to the scheduled task environment."
