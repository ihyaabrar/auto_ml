# AutoML Platform - Railway Deployment Script (PowerShell)
# Run this after logging in to Railway

Write-Host "Starting AutoML Platform Deployment..." -ForegroundColor Green
Write-Host ""

# Check if Railway is logged in
Write-Host "Checking Railway login status..."
$railwayStatus = railway whoami 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Not logged in to Railway!" -ForegroundColor Red
    Write-Host "Please run: railway login"
    Write-Host "Or visit: https://railway.app and login with GitHub"
    exit 1
}

Write-Host "Logged in as: $railwayStatus"
Write-Host ""

# Initialize project
Write-Host "Initializing Railway project..."
Set-Location $PSScriptRoot
railway init --name auto-ml-platform 2>$null | Out-Null

# Link to the project
Write-Host "Linking to Railway project..."
railway link 2>$null | Out-Null

# Add PostgreSQL
Write-Host "Adding PostgreSQL database..."
railway add --database postgres

# Get DATABASE_URL
Write-Host "Waiting for database provisioning..."
Start-Sleep -Seconds 5
$DATABASE_URL = railway variables get DATABASE_URL 2>$null

# Use provided PostgreSQL URL if available
if ([string]::IsNullOrEmpty($DATABASE_URL)) {
    Write-Host "Database not found in Railway variables." -ForegroundColor Yellow
    Write-Host "Using manually provided DATABASE_URL..." -ForegroundColor Cyan
    $DATABASE_URL = "postgresql://postgres:PcIPBCirhhyGQHjerMOjzGUgcedqeZxa@junction.proxy.rlwy.net:23565/railway"
}

if ([string]::IsNullOrEmpty($DATABASE_URL)) {
    Write-Host "Database not provisioned yet!" -ForegroundColor Red
    Write-Host "Please wait and run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host "Database ready!"
Write-Host ""

# Set environment variables for backend
Write-Host "Setting environment variables..."
railway variables set UPLOAD_DIR="./uploads"
railway variables set MODELS_DIR="./models"
railway variables set PYTHON_VERSION="3.11"

Write-Host "Environment variables set!"
Write-Host ""

# Deploy backend
Write-Host "Deploying backend service..."
Set-Location backend
railway up --detach

if ($LASTEXITCODE -eq 0) {
    Write-Host "Backend deployed!" -ForegroundColor Green
} else {
    Write-Host "Backend deployment failed!" -ForegroundColor Red
    exit 1
}

# Get deployment URL
Write-Host "Getting deployment URL..."
Start-Sleep -Seconds 10
$BACKEND_URL = railway domain 2>$null | Select-String -Pattern 'https://\S+' | ForEach-Object { $_.Matches.Value }

if ([string]::IsNullOrEmpty($BACKEND_URL)) {
    $BACKEND_URL = "https://auto-ml-backend-production.up.railway.app"
}

Write-Host "Backend URL: $BACKEND_URL"
Write-Host ""

# Update frontend environment
Write-Host "Updating frontend configuration..."
Set-Location ..\frontend

$envContent = "VITE_API_URL=$BACKEND_URL`n"
$envContent | Out-File -FilePath .env -Encoding UTF8

Write-Host "Frontend configured!"
Write-Host ""

# Deploy frontend to Vercel
Write-Host "Deploying frontend to Vercel..."
vercel --prod --yes 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Vercel deployment skipped (not logged in or error)" -ForegroundColor Yellow
    Write-Host "Manual step: cd frontend; vercel"
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend API:  $BACKEND_URL" -ForegroundColor Cyan
Write-Host "Frontend:     https://auto-ml.vercel.app (after Vercel deploy)" -ForegroundColor Cyan
Write-Host "Database:     PostgreSQL (Railway managed)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Test upload:" -ForegroundColor Yellow
Write-Host "  curl -X POST ${BACKEND_URL}/api/v1/projects/upload -F 'file=@sample_dataset.csv'"
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
