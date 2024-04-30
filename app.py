from flask import Flask
from models.user import User
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # caminho da conexão com o banco de dados

db.init_app(app)

"""
Comando para se usar na criação do banco e dentro do banco para realizar as operações

- flask shell -> comando para entrar para realizar a criação do banco
- db.create_all() -> cria o banco de dados
- db.session -> cria uma sessão dentro do banco (cada usuario tem o seu próprio)
- db.session.commit()-> pega tudo que foi realizado na sessão e executa o comando no banco da dados

-- Banco Relacional -- 

"""
@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
