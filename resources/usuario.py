from flask_restful import Resource, reqparse
from models.usuario import UserModel

class User(Resource):
        # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()       
        return {'message': 'user not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
              user.delete_user()
            except:
                return {'message': 'Erro ocurred to delete user'}, 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404


class UserRegister(Resource):
    # /cadastro
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help="The field 'login',cannot be left")
        atributos.add_argument('senha', type=str, required=True, help="The field 'senha',cannot be left")
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': "The login '{}' already exists".format(dados['login'])}


        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created sucessfully!'}, 201 #Created