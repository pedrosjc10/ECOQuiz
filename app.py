from flask import Flask, render_template, request, redirect, url_for
import requests
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.quiz_db
users_collection = db.users

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página do quiz
@app.route('/quiz')
def quiz():
    # Pega 5 perguntas sobre sustentabilidade
    url = "https://opentdb.com/api.php?amount=5&category=17&type=multiple"
    response = requests.get(url).json()
    questions = response['results']
    return render_template('quiz.html', questions=questions)

# Recebe resultado do quiz
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    score = int(request.form.get('score'))
    users_collection.insert_one({"name": name, "score": score})
    return redirect(url_for('ranking'))

# Página de ranking
@app.route('/ranking')
def ranking():
    top_scores = users_collection.find().sort("score", -1).limit(10)
    return render_template('ranking.html', top_scores=top_scores)

if __name__ == '__main__':
    app.run(debug=True)
