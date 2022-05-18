from flask_restful import Resource, reqparse
from models.hotel import HotelModel


hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': '4.3',
        'diaria': '420.34',
        'cidade': 'Rio de janeiro'
    },{
        'hotel_id': 'bravo',
        'nome': 'Amanda Hotel',
        'estrelas': '4.5',
        'diaria': '420.34',
        'cidade': 'Santa Catarina'
    },{
        'hotel_id': 'charlie',
        'nome': 'Luiz Hotel',
        'estrelas': '4.3',
        'diaria': '420.34',
        'cidade': 'SP'
    }
]



class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} # selec * from hoteis


class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot left white")
    atributos.add_argument('estrelas', type=float, required=True, help="Nao deixe em branco")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()       
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists".format(hotel_id)}

        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Houve um erro ao salvar hotel.'}, 500
        return hotel.json()

    def put(self, hotel_id):      
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Houve um erro ao salvar hotel.'}, 500
        return hotel.json(), 201 #created
            
            
        
        
        

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
              hotel.delete_hotel()
            except:
                return {'message': 'Erro ocurred to delete hotel'}, 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404