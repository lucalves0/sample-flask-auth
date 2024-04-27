from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCREMY_DATABASE_URI'] = 'sqlite:///database.db' # caminho da conexão com o banco de dados

db = SQLAlchemy(app)    # conexão com API 

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
