#!/bin/bash

# AutoML Platform - Railway Deployment Script
# Run this after logging in to Railway

echo "🚀 Starting AutoML Platform Deployment..."
echo ""

# Check if Railway is logged in
echo "Checking Railway login status..."
railway whoami 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Not logged in to Railway!"
    echo "Please run: railway login"
    echo "Or visit: https://railway.app and login with GitHub"
    exit 1
fi

echo "✅ Logged in as: $(railway whoami)"
echo ""

# Initialize project
echo "📦 Initializing Railway project..."
cd "$(dirname "$0")"
railway init --name auto-ml-platform 2>/dev/null || true

# Add PostgreSQL
echo "🗄️  Adding PostgreSQL database..."
railway add postgresql

# Get DATABASE_URL
echo "⏳ Waiting for database provisioning..."
sleep 5
DATABASE_URL=$(railway variables get DATABASE_URL 2>/dev/null)

if [ -z "$DATABASE_URL" ]; then
    echo "❌ Database not provisioned yet!"
    echo "Please wait and run this script again."
    exit 1
fi

echo "✅ Database ready!"
echo ""

# Set environment variables for backend
echo "⚙️  Setting environment variables..."
railway variables set UPLOAD_DIR="./uploads"
railway variables set MODELS_DIR="./models"
railway variables set PYTHON_VERSION="3.11"

echo "✅ Environment variables set!"
echo ""

# Deploy backend
echo "🔧 Deploying backend service..."
cd backend
railway up --detach

if [ $? -eq 0 ]; then
    echo "✅ Backend deployed!"
else
    echo "❌ Backend deployment failed!"
    exit 1
fi

# Get deployment URL
echo "⏳ Getting deployment URL..."
sleep 10
BACKEND_URL=$(railway domain 2>/dev/null | grep -oP 'https://\S+')

if [ -z "$BACKEND_URL" ]; then
    BACKEND_URL="https://auto-ml-backend-production.up.railway.app"
fi

echo "✅ Backend URL: $BACKEND_URL"
echo ""

# Update frontend environment
echo "🎨 Updating frontend configuration..."
cd ../frontend

cat > .env << EOF
VITE_API_URL=$BACKEND_URL
EOF

echo "✅ Frontend configured!"
echo ""

# Deploy frontend to Vercel
echo "🌐 Deploying frontend to Vercel..."
vercel --prod --yes 2>/dev/null || {
    echo "⚠️  Vercel deployment skipped (not logged in or error)"
    echo "Manual step: cd frontend && vercel"
}

echo ""
echo "=========================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "Backend API:  $BACKEND_URL"
echo "Frontend:     https://auto-ml.vercel.app (after Vercel deploy)"
echo "Database:     PostgreSQL (Railway managed)"
echo ""
echo "Test upload:"
echo "  curl -X POST ${BACKEND_URL}/api/v1/projects/upload -F 'file=@sample_dataset.csv'"
echo ""
echo "=========================================="
echo ""
