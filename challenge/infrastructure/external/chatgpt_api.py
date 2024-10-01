import openai
import os
import re

class ChatGPTClient:
    def __init__(self):
    # Configuración inicial con la API key
        openai.api_key = "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"

    def generate_challenge(self, difficulty: str, topic: str) -> (str, str):
        # Mensaje de prompt para generar un desafío de programación
        prompt = f"Genera un desafío de programación en el tema {topic} con dificultad {difficulty}.\nIncluye una descripción del problema y proporciona un ejemplo del output esperado(al pasar al ejemplo de output esperado se tiene que empezar con 'CASOS DE PRUEBA:'), Tener en cuenta que solo se pide el problema y 2 ejemplos de inputs y outputs esperados, más no posibles soluciones. Asegúrate de que la respuesta esté dentro de los 400 tokens."
        messages = [{"role": "system",
                     "content": "Eres un modelo de generación de desafios de programación en el lenguaje python"},
                    {"role": "user", "content": prompt}]
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # O el modelo específico de ChatGPT-4
            messages=messages,
            max_tokens=400,
            temperature=0.7
        )
        print("Respuesta generada por el modelo:\n", response.choices[0].message.content)
        # Suponiendo que la respuesta tiene la descripción y luego el ejemplo, separados por algún delimitador o formato específico.
        #challenge_text, output_example = response.choices[0].message.content.strip().split("\nEjemplo de salida:")
        example_match = re.search(r"(?i)(CASOS DE PRUEBA:.*)", response.choices[0].message.content, re.DOTALL)

        if example_match:
            # Si se encuentra "Ejemplo de salida", extraer el texto anterior como descripción y el ejemplo
            output_example = example_match.group(1).strip()
            challenge_text = response.choices[0].message.content[:example_match.start()].strip()
        else:
            # Si no se encuentra el patrón, asumimos que no hay ejemplo claro
            challenge_text = response.choices[0].message.content.strip()
            output_example = "No se proporcionó un ejemplo de salida."

        return challenge_text.strip(), output_example.strip()