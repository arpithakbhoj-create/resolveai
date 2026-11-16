
import httpx


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def generate_llm_response(prompt: str):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                OLLAMA_URL,
                json=payload
            )

            response.raise_for_status()

            result = response.json()

            return result["response"]

    except httpx.RequestError as error:
        raise RuntimeError(
            f"Unable to connect to Ollama: {error}"
        ) from error

    except httpx.HTTPStatusError as error:
        raise RuntimeError(
            f"Ollama returned an HTTP error: {error}"
        ) from error
  

import json


def generate_structured_llm_response(prompt: str):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0
        }
    }

    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                OLLAMA_URL,
                json=payload
            )

            response.raise_for_status()

            result = response.json()

            return json.loads(result["response"])

    except httpx.RequestError as error:
        raise RuntimeError(
            f"Unable to connect to Ollama: {error}"
        ) from error

    except httpx.HTTPStatusError as error:
        raise RuntimeError(
            f"Ollama returned an HTTP error: {error}"
        ) from error

    except (json.JSONDecodeError, KeyError) as error:
        raise RuntimeError(
            f"Ollama returned an invalid JSON response: {error}"
        ) from error
