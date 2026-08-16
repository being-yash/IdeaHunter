# Fixed Build

## Why previous build failed?
Render defaulted to Python 3.14.3 + PyPI had a 502.

## Fix applied:
1. Added .python-version = 3.11.11
2. Pinned requirements.txt to known working versions
3. Use new Build Command (see below)

## Render Settings:
Build Command: pip install --upgrade pip && pip install -r requirements.txt
Start Command: python bot.py
Python Version env var: PYTHON_VERSION=3.11.11 (add in Render > Environment)

Add your 4 env vars as before.
