from flask import Flask, render_template, request, redirect, url_for
import requests
import random
import re
from pymongo import MongoClient
from bs4 import BeautifulSoup

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

# Temas da Wikipedia relacionados à sustentabilidade (em português)
# Lista expandida para garantir mais perguntas
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
    "Biodiversidade",
    "Poluição_da_água", # Novo tópico
    "Agricultura_sustentável", # Novo tópico
    "Efeito_estufa", # Novo tópico
    "Pegada_de_carbono", # Novo tópico
    "Consumo_consciente" # Novo tópico
]

# --- Funções Auxiliares ---

def get_summary(topic):
    """Busca o resumo de uma página da Wikipedia em português e trata erros."""
    try:
        url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{topic}"
        res = requests.get(url, timeout=5).json()
        text = res.get("extract", "")
        if not text:
            print(f"❌ Erro: Não foi possível obter o resumo para '{topic}'")
        else:
            print(f"✅ Sucesso: Resumo obtido para '{topic}'")
        return text
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao buscar na Wikipedia: {e}")
        return ""

def generate_question(text, topic):
    """Gera uma pergunta com 4 opções a partir do texto em português."""
    # Remove o texto entre parênteses para evitar respostas confusas
    clean_text = re.sub(r'\s*\(.*?\)\s*', '', text)
    
    # Remove tags HTML que podem vir no texto
    soup = BeautifulSoup(clean_text, 'html.parser')
    clean_text = soup.get_text()

    # Separa o texto em frases e remove frases muito curtas ou vazias
    sentences = [s.strip() for s in clean_text.split('.') if s.strip() and len(s) > 20]
    
    # Se não houver frases suficientes para 4 opções, retorne None
    if len(sentences) < 4:
        print(f"❌ Aviso: Texto muito curto para gerar pergunta para '{topic}'")
        return None
    
    # Escolhe uma frase aleatória como a resposta correta
    correct_sentence = random.choice(sentences)
    
    # Cria uma lista de opções, removendo a correta da lista de frases
    wrong_options = [s for s in sentences if s != correct_sentence]
    
    # Escolhe 3 opções incorretas aleatórias
    random.shuffle(wrong_options)
    selected_wrong_options = wrong_options[:3]

    # Cria a lista final de opções, com 4 itens
    options = [correct_sentence] + selected_wrong_options
    random.shuffle(options)
    
    # Cria a pergunta
    question = f"Qual das seguintes afirmações sobre '{topic.replace('_',' ')}' está correta?"
    
    # Retorna o dicionário de pergunta
    return {
        "question": question,
        "options": options,
        "answer": correct_sentence
    }

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    if request.method == 'POST':
        name = request.form.