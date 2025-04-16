#!/bin/bash

if [ -d "venv" ]; then
  source venv/bin/activate
fi

uvicorn main:app --reload --host 0.0.0.0 --port 8000
