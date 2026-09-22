import os
from huggingface_hub import hf_hub_download

MODEL_PATH = os.getenv("MODEL_PATH", "./models/qwen2.5-1.5b-instruct-q4_k_m.gguf")
REPO_ID = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
MODEL_FILENAME = "qwen2.5-1.5b-instruct-q4_k_m.gguf"

def download_model():
    model_dir = os.path.dirname(MODEL_PATH)
    os.makedirs(model_dir, exist_ok=True)

    if os.path.exists(MODEL_PATH):
        print(f"El modelo ya existe en: {MODEL_PATH}")
        return MODEL_PATH

    print(f"Descargando {MODEL_FILENAME} desde Hugging Face ({REPO_ID})...")
    path = hf_hub_download(
        repo_id=REPO_ID,
        filename=MODEL_FILENAME,
        local_dir=model_dir
    )
    print("Descarga completada con éxito.")
    return path

if __name__ == "__main__":
    download_model()