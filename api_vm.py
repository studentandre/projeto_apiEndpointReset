from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine, text
from flask import jsonify
from sqlalchemy import text
from flask import make_response

# Conexão com o banco de dados SQLite
db_connect = create_engine('sqlite:///exemplo.db')

# Script SQL para criar a tabela 'user'
create_table_sql = """
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
"""

# Executar o script SQL para criar a tabela 'user'
with db_connect.connect() as conn:
    conn.execute(text(create_table_sql))


# Inicialização do aplicativo Flask e da API
app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        # Método GET: Retorna todos os usuários do banco de dados
        conn = db_connect.connect()
        # Criar a consulta SQL como um objeto TextClause
        query = conn.execute(text("select * from user"))
        # Formatar o resultado como um dicionário e retornar como JSON
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        try:
            conn = db_connect.connect()
            name = request.json['name']
            email = request.json['email']

            # Criar a instrução SQL compilada com SQLAlchemy
            stmt = text("INSERT INTO user (name, email) VALUES (:name, :email)")

            # Executar a instrução SQL compilada passando os parâmetros como um dicionário
            conn.execute(stmt, {"name": name, "email": email})

            # Consulta para obter o registro recém-inserido
            query = conn.execute(text('SELECT * FROM user ORDER BY id DESC LIMIT 1'))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            response = make_response(jsonify(result), 201)  # Return HTTP status code 201 for resource creation
            return response
        except Exception as e:
            # Registrar o erro para debug
            app.logger.error(f"Erro durante a operação: {str(e)}")
            response = make_response(jsonify({'message': 'Ocorreu um erro durante a operação.'}), 500)
            return response

    def put(self):
        try:
            # Método PUT: Atualiza um usuário existente no banco de dados
            conn = db_connect.connect()
            id = request.json['id']
            name = request.json['name']
            email = request.json['email']
            # Corrigindo a chamada execute para passar uma lista de tuplas como parâmetro
            conn.execute("update user set name = ?, email = ? where id = ?", [(name, email, id)])
            query = conn.execute("select * from user where id = ?", (id,))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            response = make_response(jsonify(result), 201)
            return response
        except Exception as e:
            app.logger.error(f"Erro durante a operação: {str(e)}")
            response = make_response(jsonify({'message': 'Ocorreu um erro durante a operação.'}), 500)
            return response

class UserById(Resource):
    def delete(self, id):
        # Método DELETE: Remove um usuário específico do banco de dados
        conn = db_connect.connect()
        conn.execute("delete from user where id = ?", (id,))
        return {"status": "success"}

    def get(self, id):
        # Método GET: Retorna um usuário específico do banco de dados
        conn = db_connect.connect()
        query = conn.execute("select * from user where id = ?", (id,))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]


        return jsonify(result)

class Reset(Resource):
    def post(self):
        # Implemente aqui a lógica para redefinir o estado da sua aplicação
        return jsonify({'message': 'O estado da aplicação foi redefinido.'})

# Adiciona os endpoints da API
api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<id>')
api.add_resource(Reset, '/reset')

# Executa o aplicativo Flask
if __name__ == '__main__':
    app.run()