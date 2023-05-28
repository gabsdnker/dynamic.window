from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    columns = db.relationship('Column', backref='table', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Table {self.name}>"


class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))

    def __repr__(self):
        return f"<Column {self.name}>"


@app.route('/')
def index():
    tables = Table.query.all()
    return render_template('index.html', tables=tables)


@app.route('/create_table', methods=['GET', 'POST'])
def create_table():
    if request.method == 'POST':
        name = request.form['name']
        table = Table(name=name)
        db.session.add(table)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_table.html')


@app.route('/edit_table/<int:table_id>', methods=['GET', 'POST'])
def edit_table(table_id):
    table = Table.query.get_or_404(table_id)
    if request.method == 'POST':
        table.name = request.form['name']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_table.html', table=table)


@app.route('/delete_table/<int:table_id>', methods=['POST'])
def delete_table(table_id):
    table = Table.query.get_or_404(table_id)
    db.session.delete(table)
    db.session.commit()
    return redirect(url_for('index'))


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


@app.route('/delete_column/<int:column_id>', methods=['POST'])
def delete_column(column_id):
    column = Column.query.get_or_404(column_id)
    table_id = column.table.id
    db.session.delete(column)
    db.session.commit()
    return redirect(url_for('edit_table', table_id=table_id))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
