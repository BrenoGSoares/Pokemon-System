from flask import Flask, request, render_template, render_template, request, redirect, url_for, make_response
import csv
app = Flask(__name__)
app.secret_key = "123456"


def create_user(name, token):
    arquivo = 'users.txt'
    value_name = name
    value_token = token
    with open(arquivo, 'w') as arquivo:
        arquivo.write(f'{value_name}:{value_token}\n')

def apagar_dados():
    arquivo= 'users.txt'
    with open(arquivo, 'w') as arquivo:
        arquivo.write('')
            
def frescura(value):
    if value == 'Bulbasaur':
        return '../static/img/pb.jpg'
    elif value == 'Charmander':
        return '../static/img/pc.jpg'
    elif value == 'Pikachu':
        return '../static/img/pp.png'
    elif value == 'Squirtle':
        return '../static/img/ps.jpg'
    elif value == 'Gengar':
        return '../static/img/pg.jpg'

@app.route('/', methods=["POST","GET"])
def index():
    cor_cookie = request.cookies.get('cor_principal')
    cor_hover_cookie = request.cookies.get('cor_principal_hover')
    username_cookie = request.cookies.get('username_cookie')
    if username_cookie == None:
        username_cookie = ''
    return render_template('voto.html', username= username_cookie, cor_cookie=cor_cookie, cor_hover_cookie=cor_hover_cookie )

@app.route('/config', methods=['POST', 'GET'])
def config():
    cor_cookie = request.cookies.get('cor_principal')
    cor_hover_cookie = request.cookies.get('cor_principal_hover')
    if request.method == "POST":
        cor_site = request.form.get('cor')
        if cor_site == "red":
            cor_ = "--color-red"
            cor_hover =  "--color-red-hover"
            response = make_response(redirect('/'))
            response.set_cookie('cor_principal', cor_)
            response.set_cookie('cor_principal_hover', cor_hover)
            return response
        if cor_site == "blue":
            cor_ = "--color-blue"
            cor_hover =  "--color-blue-hover"
            response = make_response(redirect('/'))
            response.set_cookie('cor_principal', cor_)
            response.set_cookie('cor_principal_hover', cor_hover)
            return response
        if cor_site == "green":
            cor_ = "--color-green"
            cor_hover =  "--color-green-hover"
            response = make_response(redirect('/'))
            response.set_cookie('cor_principal', cor_)
            response.set_cookie('cor_principal_hover', cor_hover)
            return response
        if cor_site == "purple":
            cor_ = "--color-purple"
            cor_hover =  "--color-black-hover"
            response = make_response(redirect('/'))
            response.set_cookie('cor_principal', cor_)
            response.set_cookie('cor_principal_hover', cor_hover)
            return response
        if cor_site == "black":
            cor_ = "--color-black"
            cor_hover =  "--color-black-hover"
            response = make_response(redirect('/'))
            response.set_cookie('cor_principal', cor_)
            response.set_cookie('cor_principal_hover', cor_hover)
            return response
    return render_template('config.html',  cor_cookie=cor_cookie, cor_hover_cookie=cor_hover_cookie)

@app.route('/login', methods=["POST","GET"])
def login():
    cor_cookie = request.cookies.get('cor_principal')
    cor_hover_cookie = request.cookies.get('cor_principal_hover')
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == "POST" and username != "" and password != "":
        username = request.form['username']
        password = request.form['password']
        create_user(username,password)
        arquivo = 'users.txt'
        with open(arquivo, 'r') as file:
            for linha in file:
                dado_username, dado_password = linha.strip().split(':')
                if username == dado_username and password ==dado_password:
                    response = make_response(redirect('/'))
                    response.set_cookie('username_cookie', username)
                    response.set_cookie('password_cookie', password)
                    return response
        return redirect(url_for('index'))
    return render_template('login.html', cor_cookie=cor_cookie, cor_hover_cookie=cor_hover_cookie)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('username_cookie', '')
    response.delete_cookie('password_cookie')
    response.delete_cookie('cor_principal')
    response.delete_cookie('cor_principal_hover')
    apagar_dados()
    return response


@app.route('/registrado', methods=["POST", "GET"])
def vote():
    cor_cookie = request.cookies.get('cor_principal')
    cor_hover_cookie = request.cookies.get('cor_principal_hover')
    if request.method == 'POST':
        arquivo = 'votos.csv'
        value = request.form.get('escolhido')
        img = frescura(value)
        with open(arquivo, 'a', newline='') as dados_csv:
            campo = ['Pokemon']
            writer = csv.DictWriter(dados_csv, fieldnames=campo)
            if (dados_csv.tell() == 0):
                writer.writeheader()
                select = {'Pokemon': value }
                writer.writerow(select)
            else:
                select = {'Pokemon': value }
                writer.writerow(select)
        return render_template('registrado.html', pokemon = value, imagem = img, cor_cookie=cor_cookie, cor_hover_cookie=cor_hover_cookie)

@app.route('/resultado', methods=["POST", "GET"])
def resultado():
    cor_cookie = request.cookies.get('cor_principal')
    cor_hover_cookie = request.cookies.get('cor_principal_hover')
    arquivo = 'votos.csv'
    Bulbasaur = Charmander = Pikachu = Squirtle = Gengar = 0
    with open(arquivo,'r') as dados_csv:
        votos = csv.DictReader(dados_csv)
        for linha in votos:
            if linha['Pokemon'] == 'Bulbasaur':
                Bulbasaur +=1
            elif linha['Pokemon'] == 'Charmander':
                Charmander +=1
            elif linha['Pokemon'] == 'Pikachu':
                Pikachu +=1
            elif linha['Pokemon'] == 'Squirtle':
                Squirtle +=1
            if linha['Pokemon'] == 'Gengar': 
                Gengar +=1
    return render_template('resultado.html', 
    Bulbasaur_value = Bulbasaur,
    Charmander_value = Charmander,
    Pikachu_value = Pikachu,
    Squirtle_value = Squirtle,
    Gengar_value = Gengar, 
    cor_cookie=cor_cookie, cor_hover_cookie=cor_hover_cookie)

if __name__ == "__main__":
    app.run(debug=True)