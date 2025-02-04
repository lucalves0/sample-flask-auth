import bcrypt
from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # caminho da conexão com o banco de dados

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'  # view login

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(user_id)

@app.route("/login", methods=["POST"])  # usamos o 'post' para enviar senha
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password: 
        # Login
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
                login_user(user)
                print(current_user.is_authenticated)
                return jsonify({"message" : "Autenticação realizada com sucesso"})
    
    return jsonify({"message" : "Credenciais inválidas"}), 400

# criando rota para tirar desautenticação do usuario
@app.route('/logout', methods=["GET"])
@login_required # -> verifica se o usuário está autenticado
def logout():
     logout_user()
     return jsonify({"message" : "Logout realizada com sucesso"})

# criação de usuário
@app.route('/user', methods=["POST"])
@login_required
def create_user():
     data = request.json
     username = data.get("username")
     password = data.get("password")

     if username and password:
          hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
          user = User(username=username, password=hashed_password, role='user')
          db.session.add(user)
          db.session.commit()
          return jsonify({"messagem" : "Usuario cadastrado com sucesso !"})
     
     return jsonify({"messagem" : "Dados inválidos. "}), 400

# busca usuário cadastrado no sistema
@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user): 
     user = User.query.get(id_user)
     if user:
          return ({"username": user.username})
    
     return jsonify({"messagem" : "Usuario não encontrado. "}), 404

# altera informação de usuário
@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user): 
     data = request.json
     user = User.query.get(id_user)

     if id_user != current_user.id and current_user.role == "user":
          return jsonify({"message" : "Operação não permitida. "}), 403
     
     if user and data.get("password"):
          user.passoword = data.get("password")
          db.session.commit()
          return jsonify({"messagem": f"Usuário {id_user} atualizado com sucesso. "})
    
     return jsonify({"messagem" : "Usuario não encontrado. "}), 404   

# deleta o usuário do banco
@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user): 
     user = User.query.get(id_user)

     if current_user.role != 'admin':
          return jsonify({"message" : "Operação não permitida. "}), 403
     if id_user == current_user.id:
          return jsonify({"messagem" : "Deleção não permitida. "}), 403
     
     if user:
          db.session.delete(user)
          db.session.commit()
          return jsonify({"message": f"Usuário {id_user} deletado com sucesso !"})
    
     return jsonify({"messagem" : "Usuario não encontrado. "}), 404

if __name__ == '__main__':
    app.run(debug=True)

"""
usaremos a biblioteca 'bcrypt' para criptografar as senhas dos usuários, para
fins de segurança, caso alguém tenha acesso ao nosso banco de dados . 

exemplo: 

import bcrypt 
>>> password = b"1234" 
>>> password
b'1234'
>>> hashed = bcrypt.hashpw(password, bcrypt.gensalt()) 
>>> hashed
b'$2b$12$12Y/KSlBu2gzBl.tA362puvC1/bzijisXk1Arvu3QCymzWXf4WVeK'

Exemplo abaixo para comparar se uma senha é igual ao hashed criado :

>>> bcrypt.checkpw(b"12345", hashed) 

"""
"""
Comando para se usar na criação do banco e dentro do banco para realizar as operações

- flask shell -> comando para entrar para realizar a criação do banco
- db.create_all() -> cria o banco de dados
- db.session -> cria uma sessão dentro do banco (cada usuario tem o seu próprio)
- db.session.commit()-> pega tudo que foi realizado na sessão e executa o comando no banco da dados

-- Banco Relacional -- 

"""