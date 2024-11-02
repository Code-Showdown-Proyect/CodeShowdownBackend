import openai
import os
import re

from dotenv import load_dotenv


class ChatGPTClient:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_feedback(self, answer: str, question: str) -> dict:
        if not answer.strip():
            # Caso en el que no se envió respuesta
            feedback =  "No se proporcionó ninguna respuesta. Recuerda que participar y enviar tu solución es importante para recibir retroalimentación."
            return {"feedback": feedback, "score": 0, "conclusion": ""}
        print("respuesta enviada: ", answer)
        print("pregunta enviada: ", question)
        prompt = (f"Evalúa el siguiente código enviado como respuesta al desafío de Python: {answer}\n"
                  f"Basado en la pregunta: {question}, proporciona un análisis detallado.\n"
                  "Si el código es correcto, concluye con 'Conclusion: Problema resuelto correctamente'. Si es incorrecto, utiliza 'Conclusion:' seguido de una explicación breve del error y añade una puntuación con el prefijo 'Score:' y el valor correspondiente de 1 a 100.\n"
                  "Si no se detecta código Python, indica que no se proporcionó una respuesta válida y agrega 'Conclusion:' y 'Score' con un puntaje de 0.\n"
                  "El feedback debe ser conciso, sin frases como 'Respuesta generada por el modelo', y no debe exceder los 400 tokens. Siempre incluye 'Conclusion:' y 'Score:' sin símbolos adicionales.")
        messages = [
            {"role": "system", "content": "Eres un experto en Python y en la evaluación de código."},
            {"role": "user", "content": prompt}
        ]
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=400,
            temperature=0.7
        )
        #print("Respuesta generada por el modelo:\n", response.choices[0].message.content)
        feedback = response.choices[0].message.content.strip()
        print("Respuesta generada por el modelo:\n", feedback)

        #feedback ="Respuesta generada por el modelo: El texto proporcionado parece no ser código Python, sino una serie de caracteres aleatorios. Por lo tanto, no hay ningún código que evaluar. Conclusion: No se proporcionó ninguna respuesta. Score: 5"

        score = int(re.search(r'Score:\s*(\d+)', feedback).group(1)) if re.search(r'Score:\s*(\d+)', feedback) else 0
        conclusion_match = re.search(r'Conclusion:\s*(.*?)(?:\s*Score:|\s*$)', feedback) or re.search(
            r'Conclusión:\s*(.*?)(?:\s*Score:|\s*$)', feedback)
        conclusion = conclusion_match.group(1).strip() if conclusion_match else ""

        print("score: ", score)
        print("conclusion: ", conclusion)

        # Limpiar el feedback de las secciones "Score" y "Conclusion"
        feedback_cleaned = re.sub(r'(Score:\s*\d+|Conclusion:.*|Conclusión:.*)', '', feedback).strip()
        print("feedback_cleaned: ", feedback_cleaned)
        return {"feedback": feedback_cleaned, "score": score, "conclusion": conclusion}

    def determine_correctness(self, feedback: str) -> (bool, str):
        correctness_indicators = ["correcto", "bien hecho", "solución válida", "resolución correcta"]
        if any(indicator in feedback.lower() for indicator in correctness_indicators):
            return True, "La respuesta es correcta. ¡Buen trabajo!"

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