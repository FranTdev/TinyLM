FROM python:3.12-alpine AS builder

RUN apk add --no-cache build-base cmake git linux-headers
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-alpine
RUN apk add --no-cache libstdc++ libgomp
WORKDIR /app

COPY --from=builder /install /usr/local
COPY . /app

EXPOSE 8000
ENV MODEL_PATH="/app/models/qwen2.5-1.5b-instruct-q4_k_m.gguf"

# Descarga el modelo dentro de la imagen
RUN python download_model.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]