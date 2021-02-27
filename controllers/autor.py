from flask_restful import Resource, reqparse
from models.autor import AutorModel

serializer = reqparse.RequestParser()
serializer.add_argument(
    'autor_nombre',
    type=str,
    required= True,
    help="Falta el autor_nombre"
)

class AutoresController(Resource):
    def post(self):
        informacion = serializer.parse_args()
        "INSERT INTO T_AUTOR(AUTOR_NOMBRE) VALUES (INFORMACION['AUTOR_NOMBRE'])"
        #Creamos una nueva instancia de nuestro modelo del autor pero aun no se ha creado en la bd, esto sirve para 
        #validar que los campos ingresados cumplan con las definiciones de las columnas.
        nuevoAutor = AutorModel(informacion['autor_nombre'])
        #Ahora si se guarda en la BD, si hubiese algun problema dará el error de la BD pero ese indice (pk) si es autoincrementable salta una posición.
        nuevoAutor.save()
        print(nuevoAutor)
        return{
            'success':True,
            'content':nuevoAutor.json(),
            'message':'Autor creado exitosamente'
        }, 201

    def get(self):
        #SELECT * FROM T_AUTOR
        lista_autores = AutorModel.query.all()
        resultado = []
        for autor in lista_autores:
            resultado.append(autor.json())
            print(autor.json())
        print(AutorModel.query.all())
        return{
            'success': True,
            'content': resultado,
            'message': None
        }

class AutorController(Resource):
    def get(self, id):
        # .all() -> Retorna todas las coincidencias -> retorna una lista de instancias
        # .first() -> retorna el primer registro de las coindicencias -> retorna una instancia
        autorEncontrado = AutorModel.query.filter_by(autorId=id).first()
        print(autorEncontrado)
        # Si el autor se encontró retorna en el content su contenido pero si no se halló dicho autor indicar que el ID no existe con un estatus 404
        if autorEncontrado: #no se vacñia o no sea false
            return{
                'success': True,
                'content':  autorEncontrado.json(),
                'message':None
            }
        else:
            return{
                'success':False,
                'content':None,
                'message': 'El autor no existe'
            },404
    
    def put(self,id):
        autorEncontrado = AutorModel.query.filter_by(autorId=id).first()
        # No siempre es necesaria hacer la validación que el objeto exista puesto que el front se debe encargar de hacer esta validación.
        if autorEncontrado:
            data = serializer.parse_args()
            autorEncontrado.autorNombre = data['autor_nombre']
            autorEncontrado.save()
            return{
                'success': True,
                'content': autorEncontrado.json(),
                'message': 'Se actualizó el autor con éxito'
            }
        
        return {
            'success': False,
            'content': None,
            'message': 'No se encontró el autor a actualziar'
        }
    
    def delete(self,id):
        autorEncontrado = AutorModel.query.filter_by(autorId=id).first()
        if autorEncontrado:
            autorEncontrado.delete()
            return{
                'success': True,
                'content': None,
                'message':'Se eliminó exitosamente el autor de la BD'
            }
        else:
            return{
                'success':True,
                'content':None,
                'message':'No se encontró el autor a eliminar'
            },404

 