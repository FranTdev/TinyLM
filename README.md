# TinyLM Core

Microservicio de inferencia local enfocado en alto rendimiento y bajo consumo de memoria. Expone una API REST construida con **FastAPI** que ejecuta modelos de lenguaje cuantizados en formato GGUF sobre una arquitectura **CPU-bound** optimizada mediante **llama-cpp-python**.

---

## 🛠️ Arquitectura y Optimizaciones

El contenedor está diseñado sobre una imagen base ultraligera de **Linux Alpine**, utilizando compilación multietapa (*multi-stage build*) para reducir el tamaño final y mitigar la superficie de ataque.

* **Motor de Inferencia:** `llama-cpp-python` sobre `Qwen/Qwen2.5-1.5B-Instruct-GGUF` (Cuantización Q4_K_M).
* **Consumo de Memoria:** Límite explícito de RAM estipulado a **2 GB**.
* **Estrategia de Carga:** Carga perezosa (*lazy loading*) e inyección del binario `.gguf` dentro de la imagen en fase de compilación, eliminando problemas de montaje de volúmenes en entornos locales o nubes serverless.

---

## 📁 Estructura del Proyecto

```text
.
├── Dockerfile               # Build multietapa en Alpine Linux
├── docker-compose.yml       # Orquestación de contenedores y límites de recursos
├── download_model.py        # Script de descarga idempotente desde Hugging Face
├── main.py                  # API REST con FastAPI y endpoints de inferencia
├── requirements.txt         # Dependencias compiladas para Python 3.12
└── .gitignore               # Exclusión estricta de binarios .gguf y entornos

```

---

## 🚀 Despliegue Rápido

### Prerrequisitos

* Docker Engine 20.10+
* Docker Compose V2

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tinylm-core.git
cd tinylm-core

```

### 2. Construir y levantar el contenedor

```bash
docker compose up -d --build

```

El script de construcción descargará automáticamente el modelo desde Hugging Face (~980 MB) si no detecta una copia previa en la fase de build.

---

## 📡 Endpoints de la API

La API estará disponible en `http://localhost:8000`. Puedes acceder a la documentación interactiva OpenAPI en `http://localhost:8000/docs`.

### Check de Salud (`GET /health`)

Verifica si la API está arriba y si el modelo está correctamente cargado en memoria.

```bash
curl -X GET "http://localhost:8000/health"

```

### Generación de Texto (`POST /v1/chat/completions`)

Consumo del modelo con sintaxis estándar estilo OpenAI:

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "Eres un asistente técnico conciso."},
      {"role": "user", "content": "¿Qué es la cuantización de modelos?"}
    ],
    "temperature": 0.7,
    "max_tokens": 256
  }'

```

---

## ⚙️ Variables de Entorno

| Variable | Descripción | Valor por Defecto |
| --- | --- | --- |
| `MODEL_PATH` | Ruta absoluta al binario `.gguf` dentro del contenedor | `/app/models/qwen2.5-1.5b-instruct-q4_k_m.gguf` |
| `HOST` | Interfaz de red de Uvicorn | `0.0.0.0` |
| `PORT` | Puerto de exposición | `8000` |

---

## ⚡ Desarrollo Local (Sin Docker)

Si deseas depurar el backend de forma nativa en tu entorno local:

1. Crea y activa un entorno virtual de Python:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

```


2. Instala las dependencias (requiere compilador C++ compatible en el sistema):
```bash
pip install -r requirements.txt

```


3. Descarga el modelo:
```bash
python download_model.py

```


4. Ejecuta el servidor Uvicorn:
```bash
uvicorn main:app --reload --port 8000

```