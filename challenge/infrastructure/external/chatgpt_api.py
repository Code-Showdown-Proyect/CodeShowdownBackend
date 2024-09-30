import openai
import os


class ChatGPTClient:
    def __init__(self):
        # Configuración inicial con la API key
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_challenge(self, difficulty: str, topic: str) -> (str, str):
        # Mensaje de prompt para generar un desafío de programación
        prompt = f"Genera un desafío de programación en el tema {topic} con dificultad {difficulty}.\nIncluye una descripción del problema y proporciona un ejemplo del output esperado."

        response = openai.Completion.create(
            engine="text-davinci-004",  # O el modelo específico de ChatGPT-4
            prompt=prompt,
            max_tokens=400,
            temperature=0.7
        )

        # Suponiendo que la respuesta tiene la descripción y luego el ejemplo, separados por algún delimitador o formato específico.
        challenge_text, output_example = response.choices[0].text.strip().split("\nEjemplo de salida:")

        return challenge_text.strip(), output_example.strip()