from flask import render_template, request, session, redirect, url_for, make_response
from uuid import uuid1
from app import app


# ------------------------------------------------ AC3 --------------------------------------------- #
@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/confirmacao', methods=["POST"])
def confirmacao():
    dados = {"nome": request.form.get('nome'),
             "email": request.form.get('email')}
    return render_template('confirmacao.html', **dados)


# --------------------------------------------- AC4 ---------------------------------------------- #
session = {'usuarios': {}, 'sessoes': {}}


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    if request.method == 'GET':
        return render_template('cadastro.html')
    
    elif request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha = request.form.get('senha')

		#verifica se já é cadastrado
        if email not in session['usuarios']:
            session['usuarios'][email] = {'nome': nome, 'email': email, 'senha': senha}
            print(session)
            return redirect(url_for('login'))
        else:return redirect(url_for('cadastro'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        
        #verifica se já está logado e redireciona caso positivo
        if request.cookies.get('id_sessao') in session['sessoes'].keys():
            return redirect(url_for('area_logada'))     
        else:return render_template('login.html')
        
    elif request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

		#verifica integridade do login e cria sessao 
        if email not in session['usuarios'].keys() or senha != session['usuarios'][email]['senha']:
            return redirect(url_for('login'))
        
        else:
            id_sessao = str(uuid1())
            session['sessoes'][id_sessao] = email
            print(session)  
            resp = make_response(redirect(url_for('area_logada')))
            resp.set_cookie('id_sessao', id_sessao)
            return resp


@app.route('/logout')
def logout():
    id_sessao = request.cookies.get('id_sessao')
    session['sessoes'].pop(id_sessao, None)
    print(session)  
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('id_sessao')
    return resp


@app.route('/area_logada')
def area_logada():
    # verifica se está logado e redireciona caso positivo
    if request.cookies.get('id_sessao') in session['sessoes'].keys():
        return render_template('area_logada.html')
    else:
        return redirect(url_for('login'))