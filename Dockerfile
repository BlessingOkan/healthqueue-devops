FROM python:3.12.7-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd --system --no-create-home appuser
USER appuser

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]
