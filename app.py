from flask import Flask, request, render_template
import csv
app = Flask(__name__)

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
    return render_template('voto.html')

@app.route('/registrado', methods=["POST", "GET"])
def vote():
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
        return render_template('registrado.html', pokemon = value, imagem = img)

@app.route('/resultado', methods=["POST", "GET"])
def resultado():
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
    Gengar_value = Gengar)




if __name__ == "__main__":
    app.run(debug=True)