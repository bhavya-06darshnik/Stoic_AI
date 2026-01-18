import re

from flask import Flask, request, render_template

from utils.constants import DATA_PATH, DB_PATH
from utils.chat import invoke_rag

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat_with_bot', methods=['POST'])
def answer():
    user_input = request.form['user_input']
    bot_message = invoke_rag(user_input)
    print("Bot message:", bot_message)

    pattern = r"(Answer:|StoicBot:|Marc Still:)\s*(.*)" #r"StoicBot:\s*(.*)"
    # Search for the pattern in the text
    match = re.search(pattern, bot_message, re.DOTALL)

    if match:
        answer = match.group(2).strip()
        if 'Question:' in answer:
            answer = answer.split('Question:')[0].strip()
        return {'response': answer}
    else:
        return {'response': "Can't answer that question. Please ask another one."}

if __name__ == '__main__':
    app.run()

