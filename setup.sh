#!/bin/bash

# HOA Chatbot Setup Script

set -e

echo "=================================="
echo "HOA Chatbot Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠ IMPORTANT: Edit .env file and add your OPENAI_API_KEY"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Check if documents exist
echo "Checking documents directory..."
if [ -d "documents" ] && [ "$(ls -A documents)" ]; then
    echo "✓ Documents directory exists with files"
    echo ""
else
    echo "⚠ Documents directory is empty"
    echo "  Add your PDF or text documents to the documents/ directory"
    echo ""
fi

echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENAI_API_KEY"
echo "2. Add documents to the documents/ directory"
echo "3. Run: python main.py ingest"
echo "4. Run: python main.py serve"
echo ""
echo "For Docker deployment:"
echo "  docker-compose up --build"
echo ""
