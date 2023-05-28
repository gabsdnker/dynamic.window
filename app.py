from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)



"""A classe Table representa uma tabela no banco de dados. 
Ela possui os seguintes atributos e propriedades:

id:         ==> Identificador único da tabela (chave primária).
name:       ==> Nome da tabela, armazenado como uma string.
columns:    ==> Relacionamento um-para-muitos com a classe Column. 
Essa propriedade define uma lista de colunas associadas à tabela.

__repr__(): ==> Método especial que retorna uma representação textual da tabela, 
no caso, a representação é uma string que contém o nome da tabela.

Essa classe também é definida como um modelo no SQLAlchemy, permitindo que 
seja mapeada para uma tabela no banco de dados. A relação entre a classe Table 
e a classe Column é estabelecida por meio do atributo columns, que define um 
relacionamento de um-para-muitos. Isso significa que uma tabela pode ter várias 
colunas relacionadas a ela.

A propriedade backref='table' especifica que cada objeto Column terá um atributo 
adicional chamado table, que permite acessar a tabela à qual a coluna pertence.

A propriedade lazy='dynamic' indica que o relacionamento será carregado de forma 
dinâmica, permitindo que consultas adicionais sejam feitas na relação. Isso permite 
que você consulte apenas as colunas de uma tabela conforme necessário, 
em vez de carregá-las todas de uma vez.

A propriedade cascade='all, delete-orphan' indica que a exclusão de uma tabela também 
resultará na exclusão em cascata das colunas associadas. Ou seja, quando uma tabela é 
excluída, todas as colunas relacionadas a ela também serão excluídas automaticamente.

A classe Table é usada para representar as tabelas do banco de dados. Cada objeto Table 
contém informações sobre o nome da tabela e as colunas associadas a ela. Essa estrutura 
permite criar, editar e excluir tabelas, bem como manipular suas colunas e relacionamentos 
com outras tabelas."""
class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    columns = db.relationship('Column', backref='table', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Table {self.name}>"



"""A classe 'Column' representa uma coluna em uma tabela do banco de dados. 
Ela possui os seguintes atributos e propriedades:

id:         ==> Identificador único da coluna (chave primária).
name:       ==> Nome da coluna, armazenado como uma string.
table_id:   ==> Chave estrangeira que faz referência à tabela à qual a coluna pertence.
__repr__(): ==> Método especial que retorna uma representação textual da coluna, 
no caso, a representação é uma string que contém o nome da coluna.

Essa classe também é definida como um modelo no SQLAlchemy, 
permitindo que seja mapeada para uma tabela no banco de dados. 
A relação entre a classe Column e a classe Table é estabelecida 
por meio da chave estrangeira table_id, que faz referência à 
chave primária da tabela relacionada.

A classe Column é usada para representar as colunas de uma tabela. 
Cada objeto Column contém informações sobre o nome da coluna e a tabela 
à qual pertence. Essa estrutura permite que as colunas sejam adicionadas, 
editadas e excluídas de uma tabela, mantendo a integridade dos dados e as 
relações entre as tabelas."""
class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))

    def __repr__(self):
        return f"<Column {self.name}>"
    



"""As classes "Row" e "Cell" são definidas como modelos no SQLAlchemy, permitindo que sejam 
mapeadas para tabelas no banco de dados. A relação entre as classes Row e Cell é 
estabelecida por meio das chaves estrangeiras row_id na classe Cell e table_id na 
classe Row, que referenciam as respectivas chaves primárias nas tabelas relacionadas.

Essas classes são usadas para representar a estrutura de uma tabela com linhas e células, 
permitindo que os dados sejam armazenados e consultados de forma organizada."""

"""A classe Row possui os seguintes atributos e propriedades:

id: Identificador único da linha (chave primária).
table_id: Chave estrangeira que faz referência à tabela à qual a linha pertence.
cells: Relacionamento um-para-muitos com a classe Cell. 
Essa propriedade define uma lista de células associadas à linha.
__repr__(): Método especial que retorna uma representação textual da linha, 
no caso, a representação é uma string que contém o ID da linha."""
class Row(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    cells = db.relationship('Cell', backref='row', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Row {self.id}>"

"""A classe Cell possui os seguintes atributos e propriedades:

id: Identificador único da célula (chave primária).
row_id: Chave estrangeira que faz referência à linha à qual a célula pertence.
column_id: Chave estrangeira que faz referência à coluna à qual a célula pertence.
value: Valor da célula, armazenado como uma string.
__repr__(): Método especial que retorna uma representação textual da célula, 
no caso, a representação é uma string que contém o valor da célula."""
class Cell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    row_id = db.Column(db.Integer, db.ForeignKey('row.id'))
    column_id = db.Column(db.Integer, db.ForeignKey('column.id'))
    value = db.Column(db.String(255))

    def __repr__(self):
        return f"<Cell {self.value}>"
    


"""Descrição: Adiciona uma nova linha a uma tabela específica.
Funcionalidade:
Obtém o objeto Table correspondente ao ID fornecido.
Cria uma nova instância de Row relacionada à tabela.
Adiciona a nova linha à sessão do banco de dados.
Salva a sessão do banco de dados.
Retorna os dados da nova linha em formato JSON."""
@app.route('/add_row/<int:table_id>', methods=['POST'])
def add_row(table_id):
    table = Table.query.get_or_404(table_id)
    row = Row(table=table)
    db.session.add(row)
    db.session.commit()

    row_data = {
        'rowId': row.id,
        'rowNumber': len(table.rows)
    }
    return jsonify(row_data)


"""Renderiza a página inicial com a lista de tabelas existentes.
Funcionalidade:
Recupera todas as tabelas do banco de dados.
Renderiza o modelo de template index.html, passando a lista de tabelas como argumento."""
@app.route('/')
def index():
    tables = Table.query.all()
    return render_template('index.html', tables=tables)




"""Cria uma nova tabela.
Funcionalidade:
Se a solicitação for do tipo POST, obtém o nome da tabela do formulário.
Cria uma nova instância de Table com o nome fornecido.
Adiciona a nova tabela à sessão do banco de dados.
Salva a sessão do banco de dados.
Redireciona para a página inicial.
Se a solicitação for do tipo GET, renderiza o modelo de template """
@app.route('/create_table', methods=['GET', 'POST'])
def create_table():
    if request.method == 'POST':
        name = request.form['name']
        table = Table(name=name)
        db.session.add(table)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_table.html')




"""Permite editar o nome de uma tabela existente.
Funcionalidade:
Obtém o objeto Table correspondente ao ID fornecido.
Se a solicitação for do tipo POST, atualiza o nome da tabela com o valor do formulário.
Salva a sessão do banco de dados.
Redireciona para a página inicial.
Se a solicitação for do tipo GET, renderiza o modelo de template edit_table.html, 
passando a tabela como argumento."""
@app.route('/edit_table/<int:table_id>', methods=['GET', 'POST'])
def edit_table(table_id):
    table = Table.query.get_or_404(table_id)
    if request.method == 'POST':
        table.name = request.form['name']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_table.html', table=table)


"""Exclui uma tabela específica.
Funcionalidade:
Obtém o objeto Table correspondente ao ID fornecido.
Remove a tabela da sessão do banco de dados.
Salva a sessão do banco de dados.
Redireciona para a página inicial."""
@app.route('/delete_table/<int:table_id>', methods=['POST'])
def delete_table(table_id):
    table = Table.query.get_or_404(table_id)
    db.session.delete(table)
    db.session.commit()
    return redirect(url_for('index'))



"""Adiciona uma nova coluna a uma tabela específica.
Funcionalidade:
Obtém o objeto Table correspondente ao ID fornecido.
Se a solicitação for do tipo POST, obtém o nome da coluna do formulário.
Cria uma nova instância de Column relacionada à tabela com o nome fornecido.
Adiciona a nova coluna à sessão do banco de dados.
Salva a sessão do banco de dados.
Redireciona para a página de edição da tabela.
Se a solicitação for do tipo GET, renderiza o modelo de template add_column.html, 
passando a tabela como argumento."""
@app.route('/add_column/<int:table_id>', methods=['GET', 'POST'])
def add_column(table_id):
    table = Table.query.get_or_404(table_id)
    if request.method == 'POST':
        name = request.form['name']
        column = Column(name=name, table=table)
        db.session.add(column)
        db.session.commit()
        return redirect(url_for('edit_table', table_id=table_id))
    return render_template('add_column.html', table=table)



"""Exclui uma coluna específica de uma tabela.
Funcionalidade:
Obtém o objeto Column correspondente ao ID fornecido.
Obtém o ID da tabela à qual a coluna pertence.
Remove a coluna da sessão do banco de dados.
Salva a sessão do banco de dados.
Redireciona para a página de edição da tabela."""
@app.route('/delete_column/<int:column_id>', methods=['POST'])
def delete_column(column_id):
    column = Column.query.get_or_404(column_id)
    table_id = column.table.id
    db.session.delete(column)
    db.session.commit()
    return redirect(url_for('edit_table', table_id=table_id))



"""Renderiza uma página com uma lista de todas as tabelas existentes.
Funcionalidade:
Recupera todas as tabelas do banco de dados.
Renderiza o modelo de template show_tables.html, 
passando a lista de tabelas como argumento."""
@app.route('/show_tables')
def show_tables():
    tables = Table.query.all()
    return render_template('show_tables.html', tables=tables)



"""Retorna os dados de uma tabela específica em formato JSON.
Funcionalidade:
Obtém o objeto Table correspondente ao ID fornecido.
Obtém todas as colunas da tabela.
Cria um dicionário com o nome da tabela e uma lista dos nomes das colunas.
Retorna os dados em formato JSON."""
@app.route('/get_table_data/<int:table_id>', methods=['GET'])
def get_table_data(table_id):
    table = Table.query.get_or_404(table_id)
    columns = table.columns
    data = {
        'table_name': table.name,
        'columns': [column.name for column in columns]
    }
    return jsonify(data)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
