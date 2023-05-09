from flask import Flask, render_template, request
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
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    name = request.form['nome']
    idade = request.form['idade']
    user = User(name=name, idade=idade)
    db.session.add(user)
    db.session.commit()
    return 'Cadastro realizado com sucesso!'

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
