FROM python:3.9-slim

WORKDIR /app

COPY ./chat/.env ./chat/.env

COPY ./chat/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./chat/ ./chat/

CMD ["sh", "-c", "python -m chat.main"]