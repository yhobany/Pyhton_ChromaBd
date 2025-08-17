from flask import Flask, render_template, request
import requests

app = Flask(__name__)
conversation = [] # Guardar preguntas y respuestas

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:1.5b"

@app.route("/", methods=["GET","POST"])
def index():
    global conversation
    if request.method == "POST":
        user_input = request.form["user_input"]
        
        contexto = cargar_contenido()
        
           
        payload ={
            "model": MODEL_NAME,
            "prompt": f"""
            Responde solo basado en el siguiente texto y siempre en idioma español. Si no conoces la respuesta, indica que no esta en el documento:
            \"\"\"{contexto}\"\"\" 
            Pregunta: {user_input}""",
            "stream": False    
            
        }
        
        response = requests.post(OLLAMA_URL, json=payload)
        result = response.json()
        
        conversation.append(("Tu", user_input))
        conversation.append(("IA", result["response"]))
        
        
    return render_template("index.html", conversation=conversation)
        
def cargar_contenido():
    
    with open("info.txt", encoding="utf-8") as  file:
        return file.read()
          
if __name__ == "main":
    app.run(debug=True)