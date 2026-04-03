#!/bin/bash

echo "🚀 Starting AutoML Platform Development Server"
echo "=============================================="
echo ""

# Check if Docker is available
if command -v docker &> /dev/null && docker-compose --version &> /dev/null; then
    echo "✅ Docker found!"
    echo ""
    echo "Starting all services with Docker Compose..."
    echo ""
    docker-compose up -d
    
    echo ""
    echo "✅ Services started successfully!"
    echo ""
    echo "📊 Access points:"
    echo "   Frontend:  http://localhost:5173"
    echo "   Backend:   http://localhost:8000"
    echo "   API Docs:  http://localhost:8000/docs"
    echo ""
    echo "To stop services: docker-compose down"
    echo ""
else
    echo "⚠️  Docker not found. Starting manual setup..."
    echo ""
    
    # Start backend
    echo "📦 Starting Backend..."
    cd backend
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python -m venv venv
    fi
    
    source venv/bin/activate || source venv/Scripts/activate
    pip install -r requirements.txt > /dev/null 2>&1
    
    echo "Backend starting on http://localhost:8000"
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..
    
    # Start frontend
    echo "🎨 Starting Frontend..."
    cd frontend
    npm install > /dev/null 2>&1
    echo "Frontend starting on http://localhost:5173"
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    echo ""
    echo "✅ Services started!"
    echo ""
    echo "📊 Access points:"
    echo "   Frontend:  http://localhost:5173"
    echo "   Backend:   http://localhost:8000"
    echo "   API Docs:  http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop all services"
    
    wait
fi
