import os
from openai import AzureOpenAI
from datetime import datetime

# Configura tus variables de entorno
#AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "EizxzeMgs69egX3XEWttQ744lzPuYD204ERsXn9dKYJmoSgUxoTdJQQJ99BEAC4f1cMXJ3w3AAABACOGDkfY")
###AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "9OvJ5fgalUlYClcgEuunGEypjZR7DAbZs49LTG2B8F1R5hh2y0toJQQJ99BEACHrzpqXJ3w3AAAAACOGPa9q")
#AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://freeplan.openai.azure.com/")
###AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://gbert-mave4hju-northcentralus.cognitiveservices.azure.com/")
###AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4-ansv")  # Asegúrate de que exista en Azure

# Cliente compatible con openai>=1.0.0
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-12-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def generar_comunicado(prompt: str, tono: str = "formal", audiencia: str = "público general"):
    system_message = (
        f"Eres un redactor oficial del departamento de prensa de un organismo estatal. "
        f"Redacta el contenido solicitado con tono {tono}, dirigido al {audiencia}. "
        f"Asegúrate de que el mensaje sea claro, institucional, empático y socialmente responsable."
    )

    try:
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        texto_generado = response.choices[0].message.content
        return texto_generado

    except Exception as e:
        print(f"❌ Error al generar contenido: {e}")
        return None

def guardar_comunicado(texto: str, nombre_archivo: str = None):
    if not nombre_archivo:
        nombre_archivo = f"comunicado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"✅ Comunicado guardado en: {nombre_archivo}")

# if __name__ == "__main__":
#     # prompt = (
#     #     "Redacta un comunicado oficial (para ser publicado en el sitio web y redes sociales) "
#     #     "ante un siniestro vial grave con múltiples víctimas. Expresa las condolencias de la ANSV, "
#     #     "informa sobre las acciones en curso y brinda un mensaje de prevención."
#     # )
    
#     prompt = (
#         "Desarrolla un correo electrónico informativo para enviar a municipios y organizaciones de la sociedad civil"
#         "invitándolos a participar en la Semana de la Seguridad Vial y proponiendo ideas para actividades conjuntas"
#     )
#     # texto = generar_comunicado(prompt)
#     # if texto:
#     #     print("\n📝 Comunicado generado:\n")
#     #     print(texto)
#     #     guardar_comunicado(texto)
        
def menu_interactivo():
    print("=== Generador de Contenidos - ANSV ===")
    print("1. Comunicado Oficial")
    print("2. Correo Institucional")
    print("3. Posteo para redes")
    print("4. Boletín Interno")
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        prompt = input("Escribe el tema del comunicado: ")
        tono = "formal"
        audiencia = "público general"
    elif opcion == "2":
        prompt = input("Tema del correo: ")
        tono = "institucional"
        audiencia = "autoridades"
    elif opcion == "3":
        prompt = input("Tema del posteo: ")
        tono = "informal"
        audiencia = "usuarios de redes sociales"
    else:
        print("Opción inválida")
        return

    texto = generar_comunicado(prompt, tono, audiencia)
    if texto:
        print("\n📝 Resultado:\n", texto)
        guardar_comunicado(texto)

if __name__ == "__main__":
    menu_interactivo()
        
