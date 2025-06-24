#!/bin/bash

# Business Card Extractor - Deployment Script
# This script helps prepare and deploy the application

set -e  # Exit on any error

echo "🚀 Business Card Extractor - Deployment Preparation"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Python is available
if ! command -v python &> /dev/null; then
    print_error "Python is not installed or not in PATH"
    exit 1
fi

print_status "Python found: $(python --version)"

# Check if required files exist
required_files=("requirements.txt" "packages.txt" "runtime.txt" "app.py")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "Found $file"
    else
        print_error "Missing required file: $file"
        exit 1
    fi
done

# Run deployment test
echo ""
echo "🔍 Running deployment tests..."
if python deployment_test.py; then
    print_status "All deployment tests passed!"
else
    print_error "Deployment tests failed. Please fix issues before deploying."
    exit 1
fi

# Check git status
echo ""
echo "📋 Checking git status..."
if [ -d ".git" ]; then
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "You have uncommitted changes. Consider committing them before deployment."
        git status --short
    else
        print_status "Working directory is clean"
    fi
    
    # Show current branch
    current_branch=$(git branch --show-current)
    print_status "Current branch: $current_branch"
else
    print_warning "Not a git repository. Consider initializing git for version control."
fi

# Check for environment variables
echo ""
echo "🌍 Checking environment variables..."
if [ -n "$DATABASE_URL" ]; then
    print_status "DATABASE_URL is set"
else
    print_warning "DATABASE_URL not set (will use SQLite)"
fi

# Deployment platform detection
echo ""
echo "🚀 Deployment Platform Detection:"

# Check for Streamlit Cloud
if [ -f ".streamlit/config.toml" ]; then
    print_status "Streamlit Cloud configuration found"
fi

# Check for Heroku
if [ -f "Procfile" ] || [ -f "app.json" ]; then
    print_status "Heroku configuration found"
fi

# Check for Docker
if [ -f "Dockerfile" ]; then
    print_status "Docker configuration found"
fi

# Provide deployment instructions
echo ""
echo "📋 Deployment Instructions:"
echo "=========================="

if [ -f ".streamlit/config.toml" ]; then
    echo "🌐 Streamlit Cloud:"
    echo "   1. Push to GitHub: git push origin main"
    echo "   2. Go to https://share.streamlit.io"
    echo "   3. Connect your repository"
    echo "   4. Set main file path to: app.py"
    echo "   5. Deploy!"
elif [ -f "Procfile" ]; then
    echo "🦊 Heroku:"
    echo "   1. Install Heroku CLI"
    echo "   2. Run: heroku create your-app-name"
    echo "   3. Run: git push heroku main"
    echo "   4. Set environment variables if needed"
elif [ -f "Dockerfile" ]; then
    echo "🐳 Docker:"
    echo "   1. Build: docker build -t business-card-extractor ."
    echo "   2. Run: docker run -p 8501:8501 business-card-extractor"
    echo "   3. Deploy to your preferred container platform"
else
    echo "📦 Generic Deployment:"
    echo "   1. Ensure all dependencies are installed"
    echo "   2. Set up your deployment platform"
    echo "   3. Configure environment variables"
    echo "   4. Deploy the application"
fi

echo ""
echo "🔧 Post-Deployment Checklist:"
echo "   ✅ App loads without errors"
echo "   ✅ Image upload works"
echo "   ✅ OCR extraction functions"
echo "   ✅ Database operations work"
echo "   ✅ All features accessible"

echo ""
print_status "Deployment preparation complete!"
echo ""
echo "📚 For troubleshooting, see: DEPLOYMENT_TROUBLESHOOTING.md"
echo "🧪 For testing, run: python deployment_test.py" 