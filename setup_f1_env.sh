#!/bin/bash

echo "🚀 Updating system..."
sudo apt update && sudo apt upgrade -y

echo "🐍 Installing Python + tools..."
sudo apt install -y python3 python3-pip python3-venv build-essential git

echo "📁 Creating project folder..."
mkdir -p f1-exp
cd f1-exp

echo "🐍 Creating virtual environment..."
python3 -m venv venv

echo "⚡ Activating venv..."
source venv/bin/activate

echo "⬆️ Upgrading pip..."
pip install --upgrade pip

echo "📦 Installing Python libraries..."
pip install fastapi uvicorn
pip install fastf1
pip install sqlalchemy
pip install pandas
pip install psycopg2-binary
pip install openai

echo "🗄 Installing PostgreSQL (optional backend support)..."
sudo apt install -y postgresql postgresql-contrib

echo "🔥 Enabling PostgreSQL service..."
sudo systemctl enable postgresql

echo "🧪 Verifying installations..."
python3 -c "import fastapi, fastf1, sqlalchemy, pandas; print('✔ Core libraries installed')"

echo "✅ Setup complete!"
echo "👉 Next step: run uvicorn main:app --host 0.0.0.0 --port 8000"
