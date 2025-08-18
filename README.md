# EcoQuiz - Quiz de Sustentabilidade 🌱

Um quiz interativo sobre sustentabilidade e meio ambiente desenvolvido em Flask.

## 🚀 Funcionalidades

- **10 perguntas específicas** sobre sustentabilidade
- **4 opções por pergunta** com apenas uma resposta correta
- **Sistema de ranking** com MongoDB
- **Interface responsiva** e moderna
- **Validação de respostas** em tempo real

## 📋 Perguntas do Quiz

O quiz inclui perguntas sobre:
- Desenvolvimento Sustentável
- Energias Renováveis
- Pegada de Carbono
- Efeito Estufa
- Economia Circular
- Reciclagem e Resíduos
- Biodiversidade
- Acordo de Paris
- Agricultura Sustentável
- Desmatamento

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Banco de Dados**: MongoDB
- **Estilização**: CSS personalizado com tema verde

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/ECOQuiz.git
cd ECOQuiz
```

2. Instale as dependências:
```bash
pip install flask requests pymongo beautifulsoup4
```

3. Execute o aplicativo:
```bash
python app.py
```

4. Acesse no navegador: `http://localhost:5000`

## 🎯 Como Jogar

1. Digite seu nome na página inicial
2. Responda as 10 perguntas sobre sustentabilidade
3. Selecione apenas uma opção por pergunta
4. Clique em "Finalizar Quiz"
5. Veja sua pontuação no ranking

## 🏆 Sistema de Pontuação

- Cada resposta correta vale 1 ponto
- Pontuação máxima: 10/10
- Ranking ordenado por pontuação (maior para menor)

## 🔧 Melhorias Implementadas

- ✅ Perguntas específicas sobre sustentabilidade
- ✅ Seleção única por pergunta (radio buttons)
- ✅ Validação JavaScript em tempo real
- ✅ Cálculo correto de pontuação
- ✅ Sistema de ranking funcional
- ✅ Interface moderna e responsiva
- ✅ Feedback visual para o usuário

## 📁 Estrutura do Projeto

```
ECOQuiz/
├── app.py              # Aplicação Flask principal
├── static/
│   └── styles.css      # Estilos CSS
├── templates/
│   ├── index.html      # Página inicial
│   ├── quiz.html       # Página do quiz
│   └── ranking.html    # Página do ranking
└── README.md           # Documentação
```

## 🌍 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:
- Adicionar novas perguntas
- Melhorar a interface
- Corrigir bugs
- Adicionar novas funcionalidades

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
