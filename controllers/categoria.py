# CREATE CATEGORIA
# READ ALL CATEGORIA

from flask_restful import Resource, reqparse
from models.categoria import CategoriaModel

serializer = reqparse.RequestParser()
serializer.add_argument(
    'categoria_descripcion',
    type=str,
    required=True,
    help='Falta la categoria_descripcion',
    location='json' #Por defecto intenta buscar en todos los campos posibles y si lo encuentra no dará error pero si queremos indicar exactamente porque medio me lo tiene que pasar, debemos indicar el location.
)

class CategoriaController(Resource):
    def get(self):
        categorias = CategoriaModel.query.all()
        resultado = []
        for categoria in categorias:
            resultado.append(categoria.json())
        return {
            'success': True,
            'content': resultado,
            'message': None
        }
   
    def post(self):
        data = serializer.parse_args()
        nuevaCategoria = CategoriaModel(data['categoria_descripcion'])
        nuevaCategoria.save()
        return { 
            'success':True,
            'content': nuevaCategoria.json(),
            'message':'Categoria creada exitosamente'
        }, 201