import openai
import os


class ChatGPTClient:
    def __init__(self):
        # Configuración inicial con la API key
        openai.api_key = "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"

    def generate_challenge(self, difficulty: str, topic: str) -> (str, str):
        # Mensaje de prompt para generar un desafío de programación
        prompt = f"Genera un desafío de programación en el tema {topic} con dificultad {difficulty}.\nIncluye una descripción del problema y proporciona un ejemplo del output esperado."
        messages = [{"role": "system",
                     "content": "Eres un modelo de generación de desafios de programación en el lenguaje python"},
                    {"role": "user", "content": prompt}]
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # O el modelo específico de ChatGPT-4
            messages=messages,
            max_tokens=400,
            temperature=1
        )
        print("Respuesta generada por el modelo:\n", response)
        # Suponiendo que la respuesta tiene la descripción y luego el ejemplo, separados por algún delimitador o formato específico.
        challenge_text, output_example = response.choices[0].message.content.strip().split("\nEjemplo de salida:")

        return challenge_text.strip(), output_example.strip()