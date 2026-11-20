
# 1. Start with Python on a lightweight Linux image
FROM python:3.14-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Configure Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Copy dependency list
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy project files into the container
COPY . .

# 7. Train the ML model inside the image
RUN python ml/train_model.py

# 8. Document the application port
EXPOSE 8000

# 9. Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
