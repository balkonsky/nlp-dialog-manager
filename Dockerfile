FROM python:3.7

WORKDIR /app

RUN mkdir -p /app/logs

COPY core core
COPY .env base_models.py main.py packages.txt ./

EXPOSE 8080

RUN pip install -r packages.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]