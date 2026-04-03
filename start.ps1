Write-Host "🚀 Starting AutoML Platform Development Server" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is available
$dockerExists = Get-Command docker -ErrorAction SilentlyContinue
$dockerComposeExists = Get-Command docker-compose -ErrorAction SilentlyContinue

if ($dockerExists -and $dockerComposeExists) {
    Write-Host "✅ Docker found!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Starting all services with Docker Compose..." -ForegroundColor Yellow
    Write-Host ""
    
    docker-compose up -d
    
    Write-Host ""
    Write-Host "✅ Services started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Access points:" -ForegroundColor Cyan
    Write-Host "   Frontend:  http://localhost:5173"
    Write-Host "   Backend:   http://localhost:8000"
    Write-Host "   API Docs:  http://localhost:8000/docs"
    Write-Host ""
    Write-Host "To stop services: docker-compose down" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "⚠️  Docker not found. Starting manual setup..." -ForegroundColor Yellow
    Write-Host ""
    
    # Start backend in new window
    Write-Host "📦 Starting Backend..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
        cd '$PSScriptRoot\backend'
        if (!(Test-Path 'venv')) {
            Write-Host 'Creating virtual environment...'
            python -m venv venv
        }
        .\venv\Scripts\Activate.ps1
        pip install -r requirements.txt
        Write-Host 'Backend starting on http://localhost:8000' -ForegroundColor Green
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"@
    
    # Wait a moment for backend to start
    Start-Sleep -Seconds 3
    
    # Start frontend in new window
    Write-Host "🎨 Starting Frontend..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
        cd '$PSScriptRoot\frontend'
        npm install
        Write-Host 'Frontend starting on http://localhost:5173' -ForegroundColor Green
        npm run dev
"@
    
    Write-Host ""
    Write-Host "✅ Services started in new windows!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Access points:" -ForegroundColor Cyan
    Write-Host "   Frontend:  http://localhost:5173"
    Write-Host "   Backend:   http://localhost:8000"
    Write-Host "   API Docs:  http://localhost:8000/docs"
    Write-Host ""
    Write-Host "Close the terminal windows to stop the services" -ForegroundColor Yellow
    Write-Host ""
}
