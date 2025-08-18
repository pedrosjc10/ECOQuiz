from flask import Flask, render_template, request, redirect, url_for
import requests
import random
import re
from pymongo import MongoClient
from bs4 import BeautifulSoup

app = Flask(__name__)

# --- Configurações ---
# Conexão com MongoDB
try:
    client = MongoClient("mongodb+srv://ecoquiz:hackathon@cluster0.pbhclmb.mongodb.net/")
    db = client.quiz_db
    users_collection = db.users
    print("Conexão com MongoDB estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar com MongoDB: {e}")
    client = None

# Perguntas pré-definidas sobre sustentabilidade
SUSTAINABILITY_QUESTIONS = [
    {
        "question": "O que significa o conceito de 'Desenvolvimento Sustentável'?",
        "options": [
            "Desenvolvimento que atende às necessidades do presente sem comprometer a capacidade das gerações futuras de atenderem às suas próprias necessidades",
            "Desenvolvimento que prioriza apenas o crescimento econômico",
            "Desenvolvimento que ignora completamente os aspectos ambientais",
            "Desenvolvimento que foca apenas no lucro imediato"
        ],
        "answer": "Desenvolvimento que atende às necessidades do presente sem comprometer a capacidade das gerações futuras de atenderem às suas próprias necessidades"
    },
    {
        "question": "Qual é a principal fonte de energia renovável mais utilizada no mundo?",
        "options": [
            "Energia nuclear",
            "Energia hidrelétrica",
            "Energia solar",
            "Energia eólica"
        ],
        "answer": "Energia hidrelétrica"
    },
    {
        "question": "O que é a 'Pegada de Carbono'?",
        "options": [
            "A quantidade de CO2 que uma pessoa ou organização emite na atmosfera",
            "O tamanho do sapato de uma pessoa",
            "A quantidade de lixo que uma pessoa produz",
            "O consumo de água de uma pessoa"
        ],
        "answer": "A quantidade de CO2 que uma pessoa ou organização emite na atmosfera"
    },
    {
        "question": "Qual é o principal gás responsável pelo efeito estufa?",
        "options": [
            "Oxigênio (O2)",
            "Nitrogênio (N2)",
            "Dióxido de Carbono (CO2)",
            "Hidrogênio (H2)"
        ],
        "answer": "Dióxido de Carbono (CO2)"
    },
    {
        "question": "O que significa 'Economia Circular'?",
        "options": [
            "Um sistema econômico que mantém produtos e materiais em uso pelo maior tempo possível",
            "Uma economia que gira em torno do dinheiro",
            "Um sistema que prioriza apenas o consumo",
            "Uma economia baseada apenas em recursos não renováveis"
        ],
        "answer": "Um sistema econômico que mantém produtos e materiais em uso pelo maior tempo possível"
    },
    {
        "question": "Qual é a prática mais eficaz para reduzir o impacto ambiental do lixo doméstico?",
        "options": [
            "Queimar o lixo",
            "Jogar tudo no aterro sanitário",
            "Reduzir, reutilizar e reciclar",
            "Ignorar o problema"
        ],
        "answer": "Reduzir, reutilizar e reciclar"
    },
    {
        "question": "O que é 'Biodiversidade'?",
        "options": [
            "A variedade de vida na Terra, incluindo plantas, animais e microrganismos",
            "Apenas a quantidade de árvores em uma floresta",
            "O número de pessoas em uma cidade",
            "A quantidade de dinheiro em um banco"
        ],
        "answer": "A variedade de vida na Terra, incluindo plantas, animais e microrganismos"
    },
    {
        "question": "Qual é o principal objetivo do Acordo de Paris?",
        "options": [
            "Manter o aumento da temperatura média global abaixo de 2°C em relação aos níveis pré-industriais",
            "Aumentar a produção de combustíveis fósseis",
            "Reduzir a população mundial",
            "Aumentar o consumo de energia"
        ],
        "answer": "Manter o aumento da temperatura média global abaixo de 2°C em relação aos níveis pré-industriais"
    },
    {
        "question": "O que é 'Agricultura Sustentável'?",
        "options": [
            "Práticas agrícolas que protegem o meio ambiente e a saúde humana",
            "Agricultura que usa apenas produtos químicos",
            "Agricultura que destrói o solo",
            "Agricultura que ignora a conservação da água"
        ],
        "answer": "Práticas agrícolas que protegem o meio ambiente e a saúde humana"
    },
    {
        "question": "Qual é o impacto mais significativo do desmatamento?",
        "options": [
            "Perda de biodiversidade e aumento das emissões de CO2",
            "Aumento da produção de oxigênio",
            "Melhoria da qualidade do ar",
            "Redução do efeito estufa"
        ],
        "answer": "Perda de biodiversidade e aumento das emissões de CO2"
    }
]

# --- Funções Auxiliares ---

def get_summary(topic):
    """Busca o resumo de uma página da Wikipedia em português."""
    try:
        url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{topic}"
        res = requests.get(url, timeout=5).json()
        text = res.get("extract", "")
        return text
    except requests.exceptions.RequestException:
        return ""

def generate_question(text, topic):
    """Gera uma pergunta com 4 opções a partir do texto."""
    # Remove texto entre parênteses e tags HTML para evitar confusão
    clean_text = re.sub(r'\s*\(.*?\)\s*', '', text)
    soup = BeautifulSoup(clean_text, 'html.parser')
    clean_text = soup.get_text()
    
    # Separa o texto em frases
    sentences = [s.strip() for s in clean_text.split('.') if s.strip() and len(s) > 20]
    
    if len(sentences) < 2:
        return None
    
    # Escolhe uma frase aleatória como a resposta correta
    correct_sentence = random.choice(sentences)
    
    # Cria opções incorretas de forma genérica para não serem óbvias
    wrong_options = [
        f"A afirmação 'Não se relaciona com o tema de {topic.replace('_', ' ')}' está correta.",
        f"A afirmação 'É o oposto do conceito de {topic.replace('_', ' ')}' está correta.",
        "A principal característica é a destruição da natureza para lucro.",
        "É um conceito puramente econômico, sem preocupações sociais ou ambientais."
    ]
    random.shuffle(wrong_options)
    
    # Pega 3 opções incorretas e garante que a lista final tenha 4 itens
    options = [correct_sentence] + wrong_options[:3]
    random.shuffle(options)
    
    # Cria a pergunta
    question = f"Qual das seguintes afirmações sobre '{topic.replace('_', ' ')}' está correta?"
    
    return {
        "question": question,
        "options": options,
        "answer": correct_sentence
    }

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    """Rota para a página inicial."""
    return render_template('index.html')

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    """Rota para a página do quiz."""
    name = request.form.get('name', 'Anônimo')
    
    # Usa as perguntas pré-definidas sobre sustentabilidade
    questions = SUSTAINABILITY_QUESTIONS.copy()
    
    # Embaralha as perguntas para que apareçam em ordem diferente a cada vez
    random.shuffle(questions)
    
    print(f"✅ Total de perguntas geradas: {len(questions)}")
    
    return render_template('quiz.html', questions=questions, name=name)

@app.route('/submit', methods=['POST'])
def submit():
    """Rota para receber o resultado do quiz e salvar no ranking."""
    score = 0
    name = request.form.get('name')
    
    if not name or name == "Anônimo":
        return redirect(url_for('ranking'))

    # Itera sobre todas as perguntas (até 10) 
    for i in range(1, 11): 
        user_answer = request.form.get(f'q{i}')
        correct_answer = request.form.get(f'correct{i}')

        # Garante que a comparação seja exata e sem espaços extras
        if user_answer and correct_answer and user_answer.strip() == correct_answer.strip():
            score += 1
            print(f"Pergunta {i}: CORRETA - Usuário: '{user_answer.strip()}' | Correta: '{correct_answer.strip()}'")
        else:
            print(f"Pergunta {i}: INCORRETA - Usuário: '{user_answer}' | Correta: '{correct_answer}'")
    
    print(f"Recebendo dados do formulário: Nome={name}, Pontuação={score}")
    
    if client:
        try:
            users_collection.insert_one({"name": name, "score": score})
            print("Dados inseridos no MongoDB!")
        except Exception as e:
            print(f"Erro ao inserir no MongoDB: {e}")
    
    return redirect(url_for('ranking'))

@app.route('/ranking')
def ranking():
    """Rota para exibir a página de ranking."""
    top_scores = []
    if client:
        top_scores = list(users_collection.find().sort("score", -1).limit(10))
        print(f"Resultados do ranking: {top_scores}")
    return render_template('ranking.html', top_scores=top_scores)

if __name__ == '__main__':
    app.run(debug=True)
