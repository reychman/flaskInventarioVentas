import requests
from flask import current_app

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SISTEMA = (
    "Eres redactor de catálogo para una tienda de barrio. Escribe en español "
    "una descripción comercial atractiva de 2 a 3 oraciones (máximo 60 palabras). "
    "Usa solo la información de las especificaciones: no inventes características, "
    "no menciones precios ni uses emojis. Responde únicamente con el texto de la descripción."
)


class IAError(Exception):
    """Error al generar la descripción con la IA."""


def generar_descripcion(nombre: str, categoria: str, especificaciones: str) -> str:
    api_key = current_app.config.get("GROQ_API_KEY")
    modelo = current_app.config.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    if not api_key:
        raise IAError("Falta GROQ_API_KEY en el archivo .env")

    payload = {
        "model": modelo,
        "temperature": 0.7,
        "max_tokens": 1024,
        "reasoning_effort": "low", 
        "messages": [
            {"role": "system", "content": SISTEMA},
            {"role": "user", "content": (
                f"Producto: {nombre}\n"
                f"Categoría: {categoria}\n"
                f"Especificaciones técnicas: {especificaciones}"
            )},
        ],
    }
    try:
        resp = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
    except requests.RequestException:
        raise IAError("No se pudo conectar con Groq. Revisa tu conexión a internet.")

    if resp.status_code == 401:
        raise IAError("La API key de Groq no es válida. Revisa GROQ_API_KEY en el .env.")
    if resp.status_code == 429:
        raise IAError("Se alcanzó el límite de uso de Groq. Espera un momento e intenta de nuevo.")
    if resp.status_code != 200:
        try:
            detalle = resp.json()["error"]["message"]
        except Exception:
            detalle = resp.text[:200]
        raise IAError(f"Groq respondió con error {resp.status_code}: {detalle}")

    try:
        texto = resp.json()["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, ValueError):
        raise IAError("Respuesta inesperada de Groq.")
    if not texto:
        raise IAError("Groq devolvió una respuesta vacía.")
    return texto