import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from llama_cpp import Llama
from knowledge import SYSTEM_PROMPT

app = FastAPI(title="Francisco Tabares - TinyLM API")

# Habilitar CORS para que tu frontend en GitHub Pages pueda conectarse sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción puedes reemplazar '*' por 'https://tu-usuario.github.io'
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.getenv("MODEL_PATH", "./models/qwen2.5-1.5b-instruct-q4_k_m.gguf")

# Inicialización del modelo Llama.cpp con Qwen2.5-1.5B
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"No se encontró el modelo en {MODEL_PATH}. Ejecuta 'python download_model.py' primero.")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,       # Context window seguro para ~1.5 GB RAM
    n_threads=2,      # Optimizado para 2 vCPUs típicas en la nube
    verbose=False
)

class ChatRequest(BaseModel):
    message: str
    stream: bool = True

@app.get("/health")
def health_check():
    return {"status": "ok", "model": "Qwen2.5-1.5B-Instruct-Q4_K_M"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request.message}
    ]

    # Respuesta mediante Streaming (SSE)
    if request.stream:
        def stream_generator():
            response_stream = llm.create_chat_completion(
                messages=messages,
                temperature=0.3,
                max_tokens=300,
                stream=True
            )
            for chunk in response_stream:
                if "choices" in chunk and len(chunk["choices"]) > 0:
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        yield f"data: {json.dumps({'text': content})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_generator(), media_type="text/event-stream")

    # Respuesta normal (JSON completo)
    try:
        response = llm.create_chat_completion(
            messages=messages,
            temperature=0.3,
            max_tokens=300,
            stream=False
        )
        reply = response["choices"][0]["message"]["content"]
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))