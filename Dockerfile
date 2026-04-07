FROM python:3.10-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Dependencies install karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Saara code copy karo
COPY . .

# Environment variable set karo taaki imports sahi chalein
ENV PYTHONPATH=/app

# Port expose karo
EXPOSE 7860

# Validator ki demand ke mutabiq server/app.py chalao
CMD ["python", "server/app.py"]