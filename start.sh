#!/bin/bash
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Training and saving new model..."
python train_model.py

echo "Starting server..."
export PORT=10000
gunicorn --bind 0.0.0.0:$PORT app:app --workers 1 --timeout 120 --log-level info