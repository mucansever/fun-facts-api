FROM python:3.13-slim

WORKDIR /app

RUN python3 -m ensurepip && python3 -m pip install --upgrade uv

COPY requirements.txt .

RUN uv pip install --system -r requirements.txt

COPY . .

CMD ["python", "main.py"]
