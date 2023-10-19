# Use a lightweight python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy files and folders
COPY model model
COPY schema schema
COPY functions functions
COPY prediction_service.py .
COPY requirements.txt .
COPY config.py .

# Expose the port that FastAPI will run on
EXPOSE 80

RUN pip install -r requirements.txt

CMD ["uvicorn", "prediction_service:app","--reload", "--host", "0.0.0.0", "--port", "80"]




