FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
