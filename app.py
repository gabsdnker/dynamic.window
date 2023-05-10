from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    idade = db.Column(db.Integer)

@app.route('/')
def index():

    dados = db.session.query(User).all() 
    return render_template('index.html', listagem = dados)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    name = request.form['nome']
    idade = request.form['idade']
    user = User(name=name, idade=idade)
    db.session.add(user)
    db.session.commit()
    return redirect("/")
    #return 'Cadastro realizado com sucesso!'



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


'''
a) ver como ler os nomes da tabela que existem em um banco de dados sqlite
https://www.geeksforgeeks.org/how-to-list-tables-using-sqlite3-in-python/
b) listar os nomes das tabelas
c) ao clicar em um nome de tabela..... thcaram....
d) verifica quais campos existem na tabela

https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite
e) faz um "for" nesses campos
f) cria uma caixa de texto (input) para cada campo
assim eu montei o formulário genérico

'''