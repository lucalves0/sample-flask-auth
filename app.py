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

        if user and user.password == password:
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

@app.route('/user', methods=["POST"])
@login_required
def create_user():
     data = request.json
     username = data.get("username")
     password = data.get("password")

     if username and password:
          user = User(username=username, password=password)
          db.session.add(user)
          db.session.commit()
          return jsonify({"messagem" : "Usuario cadastrado com sucesso !"})
     
     return jsonify({"messagem" : "Dados inválidos. "}), 400

@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user): 
     user = User.query.get(id_user)
     if user:
          return ({"username": user.username})
    
     return jsonify({"messagem" : "Usuario não encontrado. "}), 404

@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user): 
     data = request.json
     user = User.query.get(id_user)
     
     if user and data.get("password"):
          user.passoword = data.get("password")
          db.session.commit()
          return jsonify({"messagem": f"Usuário {id_user} atualizado com sucesso. "})
    
     return jsonify({"messagem" : "Usuario não encontrado. "}), 404   

@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user): 
     user = User.query.get(id_user)

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
Comando para se usar na criação do banco e dentro do banco para realizar as operações

- flask shell -> comando para entrar para realizar a criação do banco
- db.create_all() -> cria o banco de dados
- db.session -> cria uma sessão dentro do banco (cada usuario tem o seu próprio)
- db.session.commit()-> pega tudo que foi realizado na sessão e executa o comando no banco da dados

-- Banco Relacional -- 

"""