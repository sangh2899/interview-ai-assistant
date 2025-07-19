#!/bin/bash

echo "Setting up Interview Co-Pilot API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env .env.local
    echo "Please update .env.local with your PostgreSQL credentials"
fi

# Initialize database (only if migrations don't exist)
if [ ! -d "migrations" ]; then
    echo "Initializing database..."
    export FLASK_APP=run.py
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
else
    echo "Database already initialized. Running migrations..."
    export FLASK_APP=run.py
    flask db upgrade
fi

echo "Setup complete!"
echo "To start the server, run:"
echo "source venv/bin/activate && python run.py"
echo ""
echo "API will be available at: http://localhost:5000"
echo "Swagger documentation at: http://localhost:5000/swagger/"
