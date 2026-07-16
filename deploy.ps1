param(
    [Parameter(Position = 0)]
    [string]$Message = "update",

    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$RemoteUrl = "https://github.com/thiennv57/attendance_system_lyhoa.git"

function Step($text) {
    Write-Host "`n==> $text" -ForegroundColor Cyan
}

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Step "Kiem tra git repository"
try {
    git rev-parse --is-inside-work-tree | Out-Null
} catch {
    Write-Error @"
Thu muc nay chua la git repository hop le.

Hay khoi tao truoc:
  git init
  git add .
  git commit -m "Initial commit"
  git branch -M main
  git remote add origin $RemoteUrl

Sau do chay lai:
  .\deploy.ps1 "Noi dung cap nhat"
"@
}

$remoteUrl = git remote get-url origin 2>$null
if (-not $remoteUrl) {
    Write-Error @"
Chua cau hinh remote 'origin'.

Hay them remote truoc:
  git remote add origin $RemoteUrl

Sau do chay lai:
  .\deploy.ps1 "Noi dung cap nhat"
"@
}

Step "Kiem tra thay doi"
$status = git status --porcelain
if (-not $status) {
    Write-Host "Khong co thay doi moi. Dang push de dong bo nhanh..." -ForegroundColor Yellow
    git push origin $Branch
    exit $LASTEXITCODE
}

Step "Stage file"
git add .

Step "Commit"
git commit -m $Message

Step "Push len remote"
git push origin $Branch

Write-Host "`nDeploy code len remote thanh cong." -ForegroundColor Green
Write-Host "PythonAnywhere: vao project va chay ./update_pythonanywhere.sh" -ForegroundColor Green
