#!/bin/bash

# Streamify Flask Backend - Quick Start Script
# This script helps you start the Flask backend server

echo "🚀 Starting Streamify Flask Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/bin/flask" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL..."
if ! pg_isready -q; then
    echo "⚠️  PostgreSQL is not running"
    echo "Starting PostgreSQL..."
    brew services start postgresql
    sleep 2
fi

# Check if database exists
DB_EXISTS=$(psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='streamify_flask'")
if [ "$DB_EXISTS" != "1" ]; then
    echo "📝 Creating database..."
    createdb -U postgres streamify_flask
    echo "✅ Database created"
    
    echo "🔄 Running migrations..."
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    echo "✅ Migrations completed"
fi

# Start the server
echo ""
echo "✅ All checks passed!"
echo "🚀 Starting Flask server on http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

python run.py
