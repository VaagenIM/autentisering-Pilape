FROM python:3.11-slim

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ /app/
WORKDIR /app
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
