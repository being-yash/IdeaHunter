FINAL FIX

Render Fix:
1. Go to Render Dashboard > Your Service > Environment
2. ADD NEW VARIABLE: Key=PYTHON_VERSION Value=3.11.11
3. Build Command: pip install --upgrade pip && pip install -r requirements.txt
4. Start Command: python bot.py
5. Save -> Clear Build Cache & Deploy

This requirements.txt uses >= so it will find latest available version (2.18.1) and won't fail on yanked versions.
