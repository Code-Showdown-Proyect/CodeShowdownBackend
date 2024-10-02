import openai
import os
import re


class ChatGPTClient:
    def __init__(self):
        # Configuración inicial con la API key
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_feedback(self, answer: str) -> str:
        if not answer.strip():
            # Caso en el que no se envió respuesta
            return "No se proporcionó ninguna respuesta. Recuerda que participar y enviar tu solución es importante para recibir retroalimentación."

        # Mensaje para generar retroalimentación del código enviado por el usuario
        prompt = (f"Evalúa el siguiente código y proporciona un feedback detallado para mejorarlo: {answer}\nIncluye refactorizaciones y mejores prácticas de Python, además de evaluar si la solución es correcta, "
                  f"en caso sea correcta, procura incluir palabras como correcto, bien hecho, solución valida, resolución correcta.")
        messages = [
            {"role": "system", "content": "Eres un experto en Python y en la evaluación de código."},
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=400,
            temperature=0.7
        )

        # Imprimir la respuesta generada para propósitos de depuración
        print("Respuesta generada por el modelo:\n", response.choices[0].message.content)

        # Extraer la retroalimentación generada por el modelo
        feedback = response.choices[0].message.content.strip()

        return feedback

    def determine_correctness(self, feedback: str) -> (bool, str):
        """
        Determina si la respuesta proporcionada es correcta en base al contenido del feedback.
        Retorna un valor booleano y un mensaje que explique la evaluación.
        """
        # Evaluar si la respuesta fue correcta con base en las frases encontradas en el feedback.
        correctness_indicators = ["correcto", "bien hecho", "solución válida", "resolución correcta"]
        if any(indicator in feedback.lower() for indicator in correctness_indicators):
            return True, "La respuesta es correcta. ¡Buen trabajo!"

        # En caso de que la respuesta no sea correcta, generar un mensaje adicional
        return False, "La respuesta no es correcta. Revisa las siguientes recomendaciones para mejorar tu solución."

    def provide_suggestions(self, feedback: str) -> str:
        """
        Proporciona sugerencias adicionales basadas en el feedback.
        """
        if not feedback or feedback.lower() == "no se proporcionó ninguna respuesta.":
            return "No se pudo proporcionar feedback adicional porque no se envió ninguna respuesta."

        # Buscar puntos específicos de mejora dentro del feedback proporcionado
        suggestions = re.findall(r"mejorar (.+?)\.|refactorización (.+?)\.", feedback, re.IGNORECASE)

        if suggestions:
            return "Algunas recomendaciones para mejorar tu código son: " + ', '.join([s for s in suggestions if s])
        return "Sigue las recomendaciones dadas para mejorar el rendimiento y la calidad de tu código."