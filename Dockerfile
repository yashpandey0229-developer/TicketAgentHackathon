FROM python:3.13-slim

WORKDIR /app

# System dependencies agar zaroori ho
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Project files copy karo
COPY . .

# Port ko 7860 kar do (Hugging Face ka favorite)
EXPOSE 7860

# --- YEH LINE UPDATE KARO ---
# Ab hum uvicorn direct nahi, balki python se server/app.py chalaenge 
# taaki validator ko wahi mile jo wo dhoond raha hai.
CMD ["python", "server/app.py"]