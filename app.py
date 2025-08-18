from flask import Flask, render_template, request, redirect, url_for
import requests
import random
from pymongo import MongoClient

app = Flask(__name__)

# --- Configurações ---
# MongoDB
try:
    client = MongoClient("mongodb+srv://ecoquiz:hackathon@cluster0.pbhclmb.mongodb.net/")
    db = client.quiz_db
    users_collection = db.users
    print("Conexão com MongoDB estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar com MongoDB: {e}")
    client = None

# Temas da Wikipedia relacionados à sustentabilidade (agora em português)
topics = [
    "Desenvolvimento_sustentável",
    "Energia_renovável",
    "Reciclagem",
    "Mitigação_das_mudanças_climáticas",
    "Sustentabilidade_ambiental",
    "Economia_circular",
    "Desflorestamento",
    "Tecnologia_verde",
    "Conservação_da_água",
    "Biodiversidade"
]

# --- Funções Auxiliares ---

def get_summary(topic):
    """Busca o resumo de uma página da Wikipedia em português e trata erros."""
    try:
        url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{topic}"
        res = requests.get(url, timeout=5).json()
        return res.get("extract", "")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar na Wikipedia: {e}")
        return ""

def generate_question(text, topic):
    """Gera uma pergunta a partir do texto em português e trata as opções."""
    # Remove o texto entre parênteses para evitar respostas confusas
    import re
    clean_text = re.sub(r'\s*\(.*?\)\s*', '', text)
    
    # Define a pergunta e a resposta correta
    question = f"Sobre o tema '{topic.replace('_',' ')}', qual alternativa está correta?"
    correct = clean_text.split(".")[0].strip() + "."
    
    # Define as respostas incorretas
    wrongs = [
        "Não tem relação com sustentabilidade.",
        "Significa apenas crescimento econômico sem preocupações ambientais.",
        "É o uso ilimitado de recursos naturais."
    ]
    
    options = wrongs + [correct]
    random.shuffle(options)
    
    return {
        "question": question,
        "options": options,
        "answer": correct
    }

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    questions = []
    for topic in topics:
        text = get_summary(topic)
        if text:
            questions.append(generate_question(text, topic))
    return render_template('quiz.html', questions=questions[:10])

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    # Trata o erro se 'score' não for enviado
    score_str = request.form.get('score')
    score = int(score_str) if score_str else 0
    
    if client and name:
        users_collection.insert_one({"name": name, "score": score})
    
    return redirect(url_for('ranking'))

@app.route('/ranking')
def ranking():
    top_scores = []
    if client:
        top_scores = users_collection.find().sort("score", -1).limit(10)
    return render_template('ranking.html', top_scores=top_scores)

if __name__ == '__main__':
    app.run(debug=True)