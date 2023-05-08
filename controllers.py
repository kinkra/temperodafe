from flask import render_template, request
from app import app


@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/confirmacao',methods=["POST"])
def confirmacao():
    dados={"nome":request.form.get('nome'),
        "email":request.form.get('email')}
    return render_template('confirmacao.html',**dados)