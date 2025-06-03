# Use official Python image
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Use Render's dynamic PORT environment variable
CMD bash -c 'uvicorn app.main:app --host 0.0.0.0 --port $PORT'
