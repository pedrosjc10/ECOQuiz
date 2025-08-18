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
    # ... (código existente)
    
    # Exemplo 1: Pergunta sobre "O que é..."
    question = f"Qual das seguintes afirmações sobre '{topic.replace('_',' ')}' está correta?"
    
    # Exemplo 2: Pergunta de Verdadeiro ou Falso
    
    # Pegue uma frase aleatória do texto
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    if len(sentences) > 0:
        correct_sentence = random.choice(sentences)
        
        # Crie uma resposta incorreta "desviada" da correta
        incorrect_options = [
            "Não tem relação com sustentabilidade.",
            "É o uso ilimitado de recursos naturais."
        ]
        
        # Adicione uma opção falsa baseada na resposta correta
        # Por exemplo, se a correta fala sobre "energia renovável", a falsa pode falar sobre "energia não renovável"
        falsa_option = correct_sentence.replace("renovável", "não renovável").replace("sustentável", "insustentável")
        
        # Garanta que a falsa não seja igual à correta
        if falsa_option == correct_sentence:
            falsa_option = "Não se aplica à questão."
            
        options = [correct_sentence, falsa_option] + incorrect_options
        random.shuffle(options)
        
        return {
            "question": question,
            "options": options,
            "answer": correct_sentence
        }
    return None

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    # Se o método for POST, o nome do usuário será enviado do index.html
    if request.method == 'POST':
        name = request.form.get('name')
    else:
        name = "Anônimo" # ou pode redirecionar para a página inicial
    
    questions = []
    # ... (sua lógica para gerar as perguntas)
    
    return render_template('quiz.html', questions=questions[:10], name=name)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    score_str = request.form.get('score')
    score = int(score_str) if score_str else 0

    # Adicione este print para depuração
    print(f"Recebendo dados do formulário: Nome={name}, Pontuação={score}")

    if client and name:
        users_collection.insert_one({"name": name, "score": score})
        # Adicione este print para verificação
        print("Dados inseridos no MongoDB!")

    return redirect(url_for('ranking'))

@app.route('/ranking')
def ranking():
    top_scores = []
    if client:
        top_scores = list(users_collection.find().sort("score", -1).limit(10))
        # Adicione este print para verificação
        print(f"Resultados do ranking: {top_scores}")
    return render_template('ranking.html', top_scores=top_scores)

if __name__ == '__main__':
    app.run(debug=True)